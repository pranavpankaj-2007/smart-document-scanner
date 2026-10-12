# Smart Document Scanner

A Python-based document scanner built using OpenCV and NumPy.

## Features

- Automatic document boundary detection
- Perspective correction to straighten document images
- Color scan output
- Black-and-white image enhancement
- Manual corner selection when automatic detection fails

## Technologies Used

- Python
- OpenCV
- NumPy

## Installation

Install the required libraries:

```bash
pip install -r requirements.txt
```

## How to Run

Run the application from the project folder:

```bash
python scanner.py
```

Choose a document image when prompted. Check the detected page boundary, select corners manually if necessary, and save the processed scan.

## Output

The processed images are saved in the `output` folder:

- `scanned_color.jpg`
- `scanned_black_white.jpg`

## Project Objective

To demonstrate document detection, perspective transformation, and image enhancement using computer vision.
