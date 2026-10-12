# Smart Document Scanner
## HackZen 2.0 – Computer Vision Project

**Project Title:** Smart Document Scanner  
**Technology Stack:** Python, OpenCV, NumPy  
**Programming Language:** Python  
**GitHub Repository:** https://github.com/pranavpankaj-2007/smart-document-scanner

---

## 1. Problem Statement

Scanning physical documents using a traditional scanner is not always convenient. Users may need to scan notes, assignments, receipts, forms, or other documents while away from a scanner. Taking a photograph using a mobile phone is easy, but the resulting image may contain unwanted background areas, tilted pages, shadows, and uneven lighting.

These issues can make documents difficult to read, store, print, or share.

The objective of this project is to develop a **Smart Document Scanner using computer vision** that detects a document in an image, corrects its perspective, and produces an enhanced scanned version.

## 2. Proposed Solution

The Smart Document Scanner is a Python-based application that uses OpenCV to identify the boundaries of a document in an image and transform it into a cleaner, scanner-like output.

The application provides the following features:

- **Image selection:** Allows users to choose an image from their computer.
- **Document detection:** Uses image-processing techniques and contour analysis to identify the document boundary.
- **Manual corner selection:** Allows users to select the four document corners if automatic detection is inaccurate.
- **Perspective correction:** Transforms a tilted document into a top-down rectangular view.
- **Image enhancement:** Produces both a color scan and a black-and-white version.
- **Output saving:** Saves the generated scans to an output folder.

The project aims to provide a simple, low-cost document-scanning solution that runs locally on a computer.

## 3. Technical Approach

The application follows a sequence of computer vision operations.

### Step 1: Image Input

The user selects an image through a file-selection dialog. OpenCV loads the image for processing.

### Step 2: Image Preprocessing

The image is converted to grayscale to simplify processing. Edge detection and thresholding techniques are applied to make document boundaries easier to identify.

### Step 3: Document Boundary Detection

The application uses Canny edge detection and thresholding to identify potential document edges. Contours are extracted from the processed image, and polygon approximation is used to search for a four-cornered document boundary.

Multiple detection attempts are used to improve the chances of finding the document. A minimum-area rectangle fallback is also used when a suitable four-corner contour is not found.

If automatic detection does not identify the correct boundary, the user can switch to manual mode and select the four corners of the document.

### Step 4: Corner Ordering

The four selected or detected points are arranged in a consistent order:

1. Top-left
2. Top-right
3. Bottom-right
4. Bottom-left

Correct ordering is necessary for the perspective transformation to work properly.

### Step 5: Perspective Transformation

A perspective transformation maps the four document corners to the corners of a rectangular output image. This reduces the visual distortion caused by photographing a document at an angle.

### Step 6: Image Enhancement

The corrected document is processed into two outputs:

- **Color scan:** Preserves the document's original colors.
- **Black-and-white scan:** Uses grayscale conversion and thresholding to create a high-contrast document image.

### Step 7: Saving the Results

The application allows the user to save the processed scans. The output files are:

- `output/scanned_color.jpg`
- `output/scanned_black_white.jpg`

## 4. Technologies and Models Used

### Python

Python is used to implement the application, manage the processing workflow, and connect the user interface with the computer vision operations.

### OpenCV

OpenCV is the primary computer vision library. It is used for image loading, grayscale conversion, edge detection, thresholding, contour extraction, perspective correction, and image enhancement.

### NumPy

NumPy is used for numerical operations and representing image coordinates and transformation points as arrays.

### Tkinter

Tkinter's file-selection dialog is used to let users select an image from their computer.

### Computer Vision Algorithms

The project uses the following techniques:

- Canny edge detection
- Adaptive thresholding
- Contour detection and polygon approximation
- Minimum-area rectangle fallback
- Perspective transformation
- Grayscale conversion and binary thresholding

**Machine learning or deep learning models are not used in the current implementation.** The application relies on traditional image-processing algorithms rather than a trained artificial intelligence model. This keeps the project lightweight and avoids the need for a model dataset or GPU.

## 5. Implementation

The application is implemented in Python in `scanner.py`.

The main processing workflow is:

1. Launch the application.
2. Select an image containing a document.
3. Run the document-boundary detection process.
4. Review the detected document outline.
5. Confirm the outline or switch to manual corner selection.
6. Apply perspective correction.
7. Generate the color and black-and-white scans.
8. Save the results in the output folder.

### Project Structure

```text
smart-document-scanner/
│
├── scanner.py
├── requirements.txt
├── README.md
└── output/
    ├── scanned_color.jpg
    └── scanned_black_white.jpg
```

The output images are generated when the application is run and saved; they do not need to exist in the repository beforehand.

### Dependencies

The `requirements.txt` file contains:

```text
opencv-python
numpy
```

The application can be run in a Python virtual environment after installing the required packages.

## 6. Results

The implemented application provides a basic end-to-end document-scanning workflow.

The expected results are:

- Identification and visualization of potential document boundaries.
- Manual correction of document corners when automatic detection fails.
- Conversion of a perspective-distorted document into a rectangular image.
- Generation of a color scan and a black-and-white scan.
- Saving of the processed images for later use.

The document-detection process has been tested on a sample image. However, detection accuracy depends on image quality, contrast, document shape, and background conditions. No formal accuracy percentage or large-scale benchmark has been established.

## 7. Limitations

The current implementation has several limitations:

1. **Image quality:** Blurry, noisy, or low-resolution images may reduce detection quality.
2. **Complex backgrounds:** Background patterns, nearby objects, or similar colors around the document may interfere with boundary detection.
3. **Lighting conditions:** Shadows, glare, and uneven illumination can affect edge detection and thresholding.
4. **Automatic detection:** The detected boundary may be inaccurate in some images, requiring manual corner selection.
5. **Document shape:** The current workflow is designed primarily for flat, approximately rectangular documents.
6. **Image enhancement:** Basic thresholding may remove fine details or make colored content and photographs less readable in black-and-white mode.
7. **Input requirements:** The current application processes user-selected images rather than capturing images directly from a camera.
8. **No trained model:** The project does not use machine learning for semantic document recognition, so it relies on image-processing heuristics.

## 8. Future Improvements

Potential future enhancements include:

- Adding live document detection through a webcam.
- Improving boundary detection for challenging backgrounds.
- Adding automatic shadow removal and illumination correction.
- Providing adjustable brightness, contrast, and threshold settings.
- Supporting PDF export and multi-page document scanning.
- Adding automatic image rotation and orientation correction.
- Developing a graphical interface with preview and editing controls.
- Evaluating performance on a larger collection of document images.

## 9. Conclusion

The Smart Document Scanner demonstrates how traditional computer vision techniques can be combined to create a practical document-scanning application. Using Python, OpenCV, and NumPy, it detects document boundaries, corrects perspective distortion, enhances the image, and generates color and black-and-white outputs.

The project also includes manual corner selection to help users recover when automatic detection is unsuccessful. Although further improvements are needed to handle difficult lighting and backgrounds reliably, the application provides a useful foundation for a lightweight, accessible document-scanning tool.

**GitHub Repository:** https://github.com/pranavpankaj-2007/smart-document-scanner
