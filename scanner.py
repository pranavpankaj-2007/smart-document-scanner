
import cv2
import numpy as np
import os
from tkinter import Tk, filedialog


OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def resize_for_display(image, max_width=1000, max_height=750):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    display = cv2.resize(
        image, (int(w * scale), int(h * scale))
    )
    return display, scale


def order_points(points):
    points = np.array(points, dtype=np.float32)
    result = np.zeros((4, 2), dtype=np.float32)

    total = points.sum(axis=1)
    diff = np.diff(points, axis=1).flatten()

    result[0] = points[np.argmin(total)]  # top-left
    result[2] = points[np.argmax(total)]  # bottom-right
    result[1] = points[np.argmin(diff)]   # top-right
    result[3] = points[np.argmax(diff)]   # bottom-left

    return result




def find_document(image):
    """Try multiple methods to find a document automatically."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    image_area = h * w

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    kernel = np.ones((7, 7), np.uint8)

    edge_maps = []

    # Method 1: several edge-detection settings
    for low, high in [(20, 70), (40, 120), (70, 180)]:
        edges = cv2.Canny(blurred, low, high)
        edges = cv2.morphologyEx(
            edges, cv2.MORPH_CLOSE, kernel, iterations=2
        )
        edge_maps.append(edges)

    # Method 2: adaptive thresholding
    for block_size, constant in [(31, 8), (51, 12)]:
        binary = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size, constant
        )
        edge_maps.append(binary)
        edge_maps.append(cv2.bitwise_not(binary))

    candidates = []

    for edge_map in edge_maps:
        contours, _ = cv2.findContours(
            edge_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < image_area * 0.12:
                continue

            x, y, cw, ch = cv2.boundingRect(contour)

            # Ignore contours that are essentially the entire photo.
            if cw > w * 0.98 and ch > h * 0.98:
                continue

            perimeter = cv2.arcLength(contour, True)

            for epsilon in (0.01, 0.02, 0.035, 0.05):
                approx = cv2.approxPolyDP(
                    contour, epsilon * perimeter, True
                )

                if len(approx) == 4 and cv2.isContourConvex(approx):
                    points = order_points(approx.reshape(4, 2))
                    candidates.append((area, points))
                    break

    if candidates:
        # Prefer the largest plausible four-corner candidate.
        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]

    # Last fallback: estimate a page rectangle from strong edges.
    edges = cv2.Canny(blurred, 30, 100)
    edges = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE, kernel, iterations=3
    )

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(
        contours, key=cv2.contourArea, reverse=True
    )

    for contour in contours:
        if cv2.contourArea(contour) < image_area * 0.12:
            continue

        x, y, cw, ch = cv2.boundingRect(contour)

        if cw > w * 0.98 and ch > h * 0.98:
            continue

        rectangle = cv2.minAreaRect(contour)
        points = cv2.boxPoints(rectangle)
        points = order_points(points)

        # Reject implausibly small estimates.
        if abs(cv2.contourArea(points)) >= image_area * 0.12:
            return points

    return None


    # Return the largest plausible document candidate.
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]

def select_corners(image):
    """Manual fallback: click corners clockwise."""
    display, scale = resize_for_display(image)
    points = []
    window = "Select Page Corners"

    def mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
            # Convert displayed coordinates to original coordinates.
            points.append((x / scale, y / scale))

    cv2.namedWindow(window)
    cv2.setMouseCallback(window, mouse_click)

    labels = [
        "1. Top-left",
        "2. Top-right",
        "3. Bottom-right",
        "4. Bottom-left",
    ]

    while True:
        view = display.copy()

        for i, point in enumerate(points):
            x, y = int(point[0] * scale), int(point[1] * scale)
            cv2.circle(view, (x, y), 7, (0, 0, 255), -1)
            cv2.putText(
                view, str(i + 1), (x + 8, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
            )

        if len(points) >= 2:
            scaled = np.array(
                [(int(x * scale), int(y * scale)) for x, y in points],
                dtype=np.int32
            )
            cv2.polylines(
                view, [scaled], False, (0, 255, 0), 2
            )

        instruction = (
            "Click: TL, TR, BR, BL | R: reset | ENTER: finish"
        )
        cv2.putText(
            view, instruction, (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2
        )

        current = (
            labels[len(points)] if len(points) < 4
            else "Press ENTER to continue"
        )
        cv2.putText(
            view, current, (10, 55),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
        )

        cv2.imshow(window, view)
        key = cv2.waitKey(20) & 0xFF

        if key == ord("r"):
            points.clear()
        elif key in (10, 13) and len(points) == 4:
            break
        elif key == 27:
            points = []
            break

    cv2.destroyWindow(window)

    if len(points) != 4:
        return None

    return np.array(points, dtype=np.float32)


def correct_perspective(image, corners):
    tl, tr, br, bl = corners

    width = int(max(
        np.linalg.norm(tr - tl),
        np.linalg.norm(br - bl)
    ))
    height = int(max(
        np.linalg.norm(bl - tl),
        np.linalg.norm(br - tr)
    ))

    if width < 50 or height < 50:
        raise ValueError("Selected page is too small.")

    destination = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(corners, destination)

    return cv2.warpPerspective(image, matrix, (width, height))


def make_black_white(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.createCLAHE(
        clipLimit=2.0, tileGridSize=(8, 8)
    ).apply(gray)

    return cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 15
    )


def main():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Choose a document photo",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
            ("All files", "*.*")
        ]
    )
    root.destroy()

    if not file_path:
        print("No image selected.")
        return

    image = cv2.imread(file_path)

    if image is None:
        print("Could not open the image.")
        return

    print("Detecting page...")
    corners = find_document(image)

    if corners is not None:
        display, scale = resize_for_display(image)
        preview = display.copy()

        scaled_corners = np.array(
            [[int(x * scale), int(y * scale)] for x, y in corners],
            dtype=np.int32
        )
        cv2.polylines(
            preview, [scaled_corners], True, (0, 255, 0), 3
        )

        cv2.putText(
            preview, "Y: use detected page | M: select corners | ESC: quit",
            (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (0, 0, 255), 2
        )

        cv2.imshow("Check Detection", preview)
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyWindow("Check Detection")

        if key in (ord("m"), ord("M")):
            corners = select_corners(image)
        elif key in (ord("y"), ord("Y"), 13, 10):
            pass
        else:
            print("Cancelled.")
            cv2.destroyAllWindows()
            return
    else:
        print("Automatic detection failed. Select the four corners.")
        corners = select_corners(image)

    if corners is None:
        print("Corner selection cancelled.")
        cv2.destroyAllWindows()
        return

    try:
        scanned = correct_perspective(image, corners)
    except (ValueError, cv2.error) as error:
        print("Could not straighten the page:", error)
        cv2.destroyAllWindows()
        return

    bw = make_black_white(scanned)

    cv2.imshow("Color Scan - Press S to save, R to reselect, ESC to quit",
               scanned)
    print("Press S to save, R to reselect corners, or ESC to cancel.")
    key = cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

    if key in (ord("r"), ord("R")):
        corners = select_corners(image)
        if corners is None:
            print("Cancelled.")
            return
        scanned = correct_perspective(image, corners)
        bw = make_black_white(scanned)

        cv2.imshow("Color Scan - Press S to save", scanned)
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()

    if key not in (ord("s"), ord("S")):
        print("Scan not saved.")
        return

    color_path = os.path.join(OUTPUT_DIR, "scanned_color.jpg")
    bw_path = os.path.join(OUTPUT_DIR, "scanned_black_white.jpg")

    cv2.imwrite(color_path, scanned)
    cv2.imwrite(bw_path, bw)

    print("\nSUCCESS! Both scans saved:")
    print(os.path.abspath(color_path))
    print(os.path.abspath(bw_path))


if __name__ == "__main__":
    main()
