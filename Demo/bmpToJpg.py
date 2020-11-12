import cv2
import os


def bmpToJpg(path):
    img = cv2.imread(path)
    new_file_name = path.replace(".bmp",".png")
    new_file_name = path.replace("ku","ku2")
    cv2.imwrite(new_file_name, img)


if __name__ == '__main__':
    # file_name = "a"
    # begin_num = 1
    # base_path = "Demo\ku"
    # for file in os.listdir(base_path):
    #     if os.path.splitext(file)[1] == '.bmp':
    #         # new_path = os.path.join(base_path,file_name+str(begin_num)+".bmp") 
    #         # os.rename(os.path.join(base_path,file), new_path)
    #         # begin_num += 1
    #         file_path = os.path.join(base_path,file)
    #         bmpToJpg(file_path)
    img = cv2.imread("a.bmp")
    print(img)