import requests
import shutil,zipfile,os
import zlib

def build():
    try:
        path = 'build'
        shutil.rmtree(path)
    except Exception as identifier:
        print("del file fail:"+str(identifier))
    try:
        path = 'dist\\main'
        shutil.rmtree(path)
    except Exception as identifier:
        print("del file fail:"+str(identifier))

    cmd = 'pyinstaller main.spec'
    res = os.popen(cmd)
    output_str = res.read()   # 获得输出字符串
    print(output_str)


def listdir(path, list_name:list):  #传入存储的list
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        else:  
            list_name.append(file_path)  

def input_zip(input_path,out_path):
    #遍历要压缩目录
    file_name = []
    listdir(input_path,file_name)
    # 获取压缩目录名称
    # basename = os.path.basename(os.getcwd())
    #创建zip对象，
    fzip = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)
    for index, name in enumerate(file_name):
        path_name = name.replace("dist\\","")
        # print(path_name)
        # print("zip file:"+str(index)+"//"+str(len(file_name)))
        # arcname = os.path.join(basename, path_name)
        #写入要压缩文件，并添加归档文件名称
        index += 1
        fzip.write(name, arcname=path_name)
    #关闭
    fzip.close()

if __name__ == '__main__':
    build()
    # 标准编译包
    input_zip('dist','release/release.zip')
    # 更新包
    input_zip('dist/main','release/update/release.zip')
