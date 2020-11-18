import os
import sys
import cv2 as cv

def ReadSaveAddr():
    path = "image"
    for file in os.listdir(path):
        if not file.endswith(".png"):
            continue
        file_path = os.path.join(path,file)
        img = cv.imread(file_path)
        if img is None:
            continue
        bmp_file_path = file_path.replace(".png",".bmp")
        cv.imwrite(bmp_file_path,img)

if __name__ == "__main__":
    ReadSaveAddr()