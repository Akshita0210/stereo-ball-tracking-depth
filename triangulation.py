import sys
import cv2
import numpy as np
import time

# def find_depth(circle_right, circle_left, frame_right, frame_left, baseline, f, alpha):

#     # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
#     height_right, width_right, depth_right = frame_right.shape
#     height_left, width_left, depth_left = frame_left.shape

#     if width_right == width_left:
#         f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi / 180)
#     else:
#         print('Left and right camera frames do not have the same pixel width')

#     x_right = circle_right[0]
#     x_left = circle_left[0]

#     # CALCULATE THE DISPARITY:
#     disparity = x_left - x_right   # Displacement between Left and Right frames [pixels]

#     # CALCULATE DEPTH z:
#     zDepth = (baseline * f_pixel) / disparity   # Depth in [cm]

#     return abs(zDepth)





def find_depth(circle_right, circle_left, frame_right, frame_left, baseline, f, alpha):

    if circle_right is None or circle_left is None:
        return None

    height_right, width_right, _ = frame_right.shape
    height_left, width_left, _ = frame_left.shape

    if width_right != width_left:
        print("Frame width mismatch")
        return None

    f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi / 180)

    x_right = circle_right[0]
    x_left = circle_left[0]

    disparity = x_left - x_right

    if disparity == 0:
        return None

    zDepth = (baseline * f_pixel) / disparity

    return abs(zDepth)