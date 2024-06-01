import numpy as np
import cv2

def detect_faces():
    # 加载Haar级联文件
    face_cascade = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/pi/haarcascade_eye.xml')

    # 检查文件是否加载成功
    if face_cascade.empty() or eye_cascade.empty():
        print("Error: Could not load Haar cascade files")
        return -1

    # 打开摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture")
        return -1

    # 读取一帧图像
    ret, img = cap.read()
    if not ret:
        print("Error: Could not read frame")
        return -1

    # 释放摄像头资源
    cap.release()

    # 镜像翻转图像
    img = cv2.flip(img, 1)

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)

    if len(faces) > 0:
        return 1
    else:
        return 0

# 调用函数测试
if __name__ == "__main__":
    result = detect_faces()
    print("Face detected" if result == 1 else "No face detected")
