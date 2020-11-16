import lib.gui_controls as gui_controls
import requests 
import base64
import config

class BaiDuApi:

    client_id = config.client_id
    client_secret = config.client_secret
    access_token = ""

    def __init__(self):
        self.get_token()

    def get_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
        host = host.format(client_id=self.client_id,client_secret=self.client_secret)
        response = requests.get(host)
        if response:
            self.access_token = response.json()["access_token"]

    # 通用文字识别（标准版）
    def text_1(self):
        '''
        通用文字识别
        '''
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        # 二进制方式打开图片文件
        f = open('image\\奇遇.png', 'rb')
        img = base64.b64encode(f.read())
        f.close()
        params = {"image":img}
        request_url = request_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print (response.json())

if __name__ == '__main__':
    # gui_controls.left_click("image\\kaifuhuodong.png")
    bda = BaiDuApi()
    bda.text_1()