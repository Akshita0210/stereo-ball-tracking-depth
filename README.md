# Stereo Ball Tracking and Depth Estimation

Real-time object tracking and distance measurement using two webcams, OpenCV and stereo triangulation.

The system detects a coloured object (a tennis ball by default) in the left and right camera feeds, finds its centre in each frame, and computes its distance from the cameras using the disparity between the two views.

## Demo

[▶ Watch the demonstration video](demonstration-video.mp4)


## How It Works

1. **Camera calibration**: Chessboard images are used to compute each camera's intrinsic matrix and distortion coefficients (`calibration.py`).
2. **Colour segmentation**: Each frame is blurred, converted to HSV, and thresholded to isolate the target object. Morphological erosion and dilation remove noise (`HSV_filter.py`).
3. **Object localisation**: The largest contour in the mask is taken as the object. Its centroid is found using image moments, and its minimum enclosing circle is drawn on the frame (`shape_recognition.py`).
4. **Depth by triangulation**: The focal length is converted from mm to pixels using the camera's field of view. Depth is then computed from the horizontal disparity between the two centroids (`triangulation.py`):

   ```
   f_pixel   = (image_width / 2) / tan(FOV / 2)
   disparity = x_left - x_right
   depth     = (baseline × f_pixel) / disparity
   ```

5. **Live display**: Both feeds show tracking status and the measured distance in cm. Both masks are also displayed for debugging (`main.py`).

## Project Structure

```
├── main.py               # Entry point: runs live stereo tracking and depth estimation
├── HSV_filter.py         # Colour-based segmentation in HSV space
├── shape_recognition.py  # Contour detection, centroid and enclosing circle
├── triangulation.py      # Disparity and depth calculation
├── calibration.py        # Chessboard camera calibration and undistortion
├── getImages.py          # Capture chessboard images for calibration (press 's' to save)
├── index.py              # Find which camera indices are available
└── requirements.txt
```

## Setup

**Requirements:** Python 3.8+ and two USB webcams mounted side by side, parallel, at a fixed distance apart.

```bash
git clone https://github.com/<your-username>/stereo-vision-depth-estimation.git
cd stereo-ball-tracking-depth
pip install -r requirements.txt
```

## Usage

**1. Find your camera indices**

```bash
python index.py
```

Update the indices in `cv2.VideoCapture(...)` in `main.py` to match your left and right cameras.

**2. (Optional) Calibrate the cameras**

```bash
python getImages.py      # press 's' to save a chessboard image, Esc to quit
python calibration.py
```

Move the captured images into `cameraCalibration/images/` before running `calibration.py`. It uses a 10×7 inner-corner chessboard with 20 mm squares; edit `chessboardSize` and `size_of_chessboard_squares_mm` if yours differs. The script prints the mean reprojection error and saves the results as `.pkl` files.

**3. Run depth estimation**

```bash
python main.py
```

Hold the object in view of both cameras. Press `q` to quit.

## Configuration

Set these in `main.py` to match your hardware:

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `B` | 10 | Baseline: distance between the two cameras (cm) |
| `f` | 4 | Lens focal length (mm) |
| `alpha` | 60 | Horizontal field of view (degrees) |
| `scale` | 2.52 | Empirical correction factor to convert computed depth to real-world cm |

To track a different object, change the HSV ranges in `HSV_filter.py`. The defaults target a yellow-green tennis ball.

## Tech Stack

Python · OpenCV · NumPy · imutils

## Limitations and Future Work

- Colour-based detection is sensitive to lighting and similar-coloured backgrounds.
- Only the largest detected object is tracked.
- The `scale` factor was tuned manually; full stereo calibration and rectification would remove the need for it.
- Possible extensions: deep-learning detection (e.g. YOLO) for arbitrary objects, multi-object matching, and stereo rectification with `cv2.stereoCalibrate`.