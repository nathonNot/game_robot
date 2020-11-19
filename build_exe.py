import os
import shutil

def build():
    try:
        path = 'build'
        shutil.rmtree(path)
    except Exception as identifier:
        print("删除文件失败:"+str(identifier))
    try:
        path = 'dist\\main'
        shutil.rmtree(path)
    except Exception as identifier:
        print("删除文件失败:"+str(identifier))

    cmd = 'pyinstaller main.spec'
    res = os.popen(cmd)
    output_str = res.read()   # 获得输出字符串
    print(output_str)

if __name__ == '__main__':
    build()
    