import requests
import zipfile,os
import pyautogui
import json
from tqdm import tqdm
from urllib.request import urlopen

def get_version():
    with open("main\\config\\config.json") as f:
        config = json.loads(f.read())
    return config.get("version")

def update(url):
    res = requests.get(url)
    if res.status_code != 200:
        pyautogui.alert(text='更新出现异常，请重试', title='更新异常')
        return
    res_dc = res.json()
    this_version = get_version()
    if this_version >= res_dc.get("version"):
        start_exe()
        return
    pyautogui.alert(text=res_dc.get('version_log'), title='更新日志')
    file_name = res_dc.get('version')+'.zip'
    try:
        update_file_url = res_dc.get("download_url")
        download_from_url(update_file_url,file_name)
        unzip(file_name)
    except Exception as identifier:
        pyautogui.alert(text='更新出现异常，请重试', title='更新异常')
    finally:
        os.remove(file_name)
    start_exe()
    
def unzip(data):
    zipname = "release\\release.zip"
    out_path = "dist"
    frzip = zipfile.ZipFile(data, 'r', zipfile.ZIP_DEFLATED)
    frzip.extractall()
    frzip.close()

def start_exe():
    exe_path = "cd main && start main.exe"
    os.system(exe_path)

def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    :return: bool
    """
    # 获取文件长度
    try:
        file_size = int(urlopen(url).info().get('Content-Length', -1))
    except Exception as e:
        print(e)
        print("错误，访问url: %s 异常" % url)
        return False

    # 文件大小
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size

    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])

    # 访问url进行下载
    req = requests.get(url, headers=header, stream=True)
    try:
        with(open(dst, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
    except Exception as e:
        print(e)
        return False

    pbar.close()
    return True

if __name__ == '__main__':
    update("https://fuakorm.com/api/jiuyin/get_version")
    # unzip("0.0.0.2.zip")
    # exe_path = "start dist\\main\\main.exe"
    # os.system(exe_path)