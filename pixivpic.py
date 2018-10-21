import requests
import re
from datetime import date, timedelta
import json
from os.path import exists
from os import makedirs


class PicGet():
    """
    获取图片和一些文字信息
    """
    def __init__(self):
        """初始化"""
        requests.packages.urllib3.disable_warnings()
        self.res = re.compile(r'pixivAccount\.postKey":"(.+)","pixivAccount\.captchaType')
        self.session = requests.Session()
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        }
        self.url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.urlS = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.postKey = ''
        requests.packages.urllib3.disable_warnings()

    def Key(self):
        """获取postkey"""
        try:
            web_data = self.session.get(url=self.url, headers=self.headers, verify=False).content.decode('utf-8')
            keyurl = re.findall(self.res, web_data)
            self.postKey = keyurl[0]
            print('获取Key:', self.postKey)
        except requests.exceptions.ConnectionError:
            self.postKey = None
            print('链接pixiv失败，可能是网络原因')
        return self.postKey

    def login(self):
        """账户密码登陆"""
        get_user = input('请输入用户名/邮箱：')
        get_password = input('请输入密码：')
        # 组合登陆信息
        self.data = {
                'pixiv_id': get_user，
                'password': get_password，
                'post_key': self.postKey,
                'captcha:': '',
                'g_recaptcha_response': '',
                'source': 'pc',
                'return_to': 'www.pixiv.net',
                'ref': 'wwwtop_accounts_index',
            }

        self.content = self.session.post(self.urlS, headers=self.headers, data=self.data, verify=False)
        self.cookies = self.session.cookies.get_dict()
        return self.cookies

    def dailypic(self):
        rgx = re.compile(r'(png|jpg)')
        self.data_save = {}
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        url = 'https://www.pixiv.net/ranking.php?mode=daily&date='+yesterday+'&p=1&format=json'
        header = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://www.pixiv.net/ranking.php?mode=daily&date=20181015',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        data = requests.get(url=url, headers=header, cookies=self.cookies).text
        data_dic = json.loads(data)
        # 创建文件夹
        folder = exists(r'./' + yesterday)
        if not folder:
            makedirs(r'./' + yesterday)
            print('已创建文件夹', yesterday)
        else:
            print('已存在文件夹', yesterday)
        for i in range(20):
            d_url = 'https://www.pixiv.net/ajax/illust/' + str(data_dic['contents'][i]['illust_id'])
            d_headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+str(data_dic['contents'][i]['illust_id']),
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            d_data = requests.get(url=d_url, headers=d_headers, cookies=self.cookies, verify=False).text
            d_data_dic = json.loads(d_data)
            org_url = d_data_dic['body']['urls']['original']

            self.data_save[i] = {
                'title': data_dic['contents'][i]['title'],
                'pid': data_dic['contents'][i]['illust_id'],
                'pic_num': data_dic['contents'][i]['illust_page_count'],
                'uid': data_dic['contents'][i]['user_id'],
                'time': data_dic['contents'][i]['date'],
                'user_name': data_dic['contents'][i]['user_name'],
                'bookmarkCount': d_data_dic['body']['bookmarkCount'],
                'likeCount': d_data_dic['body']['likeCount']
            }
            org_headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                'X-DevTools-Emulate-Network-Conditions-Client-Id': 'A3BD4CDC56B8B0E33DF51F378B366089',
                'Referer': org_url
            }
            suffix = re.findall(rgx, org_url)[0]
            imgfile = requests.get(url=org_url, headers=org_headers, verify=False).content
            if i < 10:
                a = '0' + str(i)
            else:
                a = str(i)
            with open(r'./' + yesterday + '/' + a + '.' + suffix, 'wb') as f:
                f.write(imgfile)
            print('完成', i, org_url)
        json_obj = json.dumps(self.data_save)
        with open(r'./'+yesterday+'_data.json', 'w') as f:
            f.write(json_obj)
        print('已储存数据')

