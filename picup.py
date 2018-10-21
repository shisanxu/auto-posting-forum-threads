import requests
from datetime import date, timedelta
import os
import json
from time import sleep


class PicUp():
    """上传图片"""
    def __init__(self):

        self.url = 'https://sm.ms/api/upload'
        requests.packages.urllib3.disable_warnings()
        self.params = {'format': 'json', 'ssl': True}
        self.img_file = open(r'E:\下载\70048860_p0.jpg', 'rb')
        self.yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        self.img_url = {}

    def up(self):
        print(os.listdir(r'./'+self.yesterday))
        x = 0
        for i in os.listdir(r'./'+self.yesterday):
            with open(r'./' + self.yesterday + '/' + i, 'rb') as f:
                file = {'smfile': f}
                res = requests.post(url=self.url, files=file, params=self.params).text
            res_dic = json.loads(res)
            share_url = res_dic["data"]["url"]
            self.img_url[x] = share_url
            print(share_url)
            x += 1
            # 短时间最多提交10次
            if x % 8 == 0:
                sleep(10)

    def saveUpData(self):
        json_obj = json.dumps(self.img_url)
        with open(r'./'+self.yesterday+'_url.json', 'w') as f:
            f.write(json_obj)
