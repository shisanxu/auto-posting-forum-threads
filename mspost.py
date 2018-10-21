import requests
import json
from datetime import date, timedelta
import random


class Post():
    """提交表单"""
    def __init__(self):
        self.yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        self.yesterday_new = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        self.colors = ['colort', 'colorg', 'colorb', 'colorp', 'colory', 'coloro', 'colorr', 'colors']
        self.text = ''
        self.title = 'pixiv ' + self.yesterday_new + ' 综合排行前二十'

    def message(self):
        """组合文章内容"""
        all_data = open(r'./' + self.yesterday + '_data.json', 'r')
        all_url = open(r'./' + self.yesterday + '_url.json', 'r')
        data_dic = json.loads(all_data.read())
        url_dic = json.loads(all_url.read())
        all_data.close()
        all_url.close()
        for i in range(20):
            row1 = '[{color}][size4][center] **— No.{n} —** [/center][/size4][/{color}]\n'.format(n=i+1, color=random.choice(colors))
            i = str(i)
            row2 = '[size2]**【 标题/Pid 】：{}/{} **[/size2]\n'.format(data_dic[i]['title'], data_dic[i]['pid'])
            row3 = '[size2]**【 作者/Uid 】：{}/{} **[/size2]\n'.format(data_dic[i]['user_name'], data_dic[i]['uid'])
            row35 = '[size2]**【 上传时间 】：{} **[/size2]\n'.format(data_dic[i]['time'])
            row4 = '[size2]**【 插画张数 】：{} **[/size2]\n'.format(data_dic[i]['pic_num'])
            row45 = '[size2]**【点赞/收藏】：{}/{} **[/size2]\n'.format(data_dic[i]['likeCount'], data_dic[i]['bookmarkCount'])
            row5 = '[size2]**【 插画链接 】：[{url}]({url}) **[/size2]\n'.format(url='https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(self.data_dic[i]['pid']))
            row6 = '![{}]({})\n'.format(data_dic[i]['pid'], url_dic[i])
            self.text = self.text + row1 + row2 + row3 + row35 + row4 + row45 + row5 + row6

        print(self.title)
        print(self.text)

        requests.packages.urllib3.disable_warnings()

    def messagePost(self):
        """提交"""
        url = 'http://www.iacgzone.me/api/discussions'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Length': '317',
            'Content-Type': 'application/json; charset=UTF-8',
            'Cookie': 'flarum_remember=GpyUbw3xbiXyw3CBG1jEgLcMTDn4D5MeXcK0Q8pf; td_cookie=3137320916; flarum_session=b4d3crv67l89qmubsmmthj2u0g',
            'Host': 'www.iacgzone.me',
            'Origin': 'http://www.iacgzone.me',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.iacgzone.me/t/Teahouse',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'X-CSRF-Token': '5CluCNQKjwNOsB7HH8ttUd4SjZGAFtSdqRZXEOma',
        }

        data = {
            'data': {
                'type': 'discussions',
                'attributes': {'content': self.text, 'title': self.title},
                'relationships': {'tags': {'data': [{'type': 'tags', 'id': '4'}, {'type': "tags", 'id': "24"}]}}
            }
        }

        data_js = json.dumps(data)

        iacg_post = requests.post(url=url, headers=headers, data=data_js, verify=False)
        print(iacg_post)
