import cv2

for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    ret, frame = cap.read()

    if ret:
        print(f"Camera index {i} is working")
        cv2.imshow(f"Camera {i}", frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

    cap.release()