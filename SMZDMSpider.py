import requests
from lxml import etree
import json
import time

url = 'https://m.smzdm.com/'
base_url = 'https://m.smzdm.com/ajax_home_list_show?time_sort='


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    else:
        return None


# 解析首页返回的数据
# xpath：//*[(@id = "post_list_preferential")]//li
def parse_html(html, db):
    root = etree.HTML(html)
    products = root.xpath('//*[(@id = "post_list_preferential")]//li')
    for product in products:
        URL = product.xpath('a/@href')[0]
        category = ''.join(product.xpath('*/span[@class="s_icon"]/text()'))
        message = product.xpath('h2/text()')[0]
        price = ''.join(product.xpath('div[@class="tips"]/em/text()'))
        commit = ''.join(product.xpath('div[@class="tips"]/span/text()'))
        time = product.xpath('address/span/text()')[0]
        data = {
            'URL': URL,
            '分类': category,
            '信息': message,
            '价格': price,
            '评论': commit,
            '发布时间': time
        }
        save_data(db, data)
        print(data)
    time_sort = root.xpath('//input[@id="time_sort"]/@value')[0]
    print(time_sort)
    return time_sort


# 解析其他页面返回的数据
def parse_json(json_data, db):
    root = json.loads(json_data)
    time_sort = root.get('time_sort')
    html = root.get('data').strip()
    nodes = etree.HTML(html)
    products = nodes.xpath('//li')
    for product in products:
        URL = product.xpath('a/@href')[0]
        category = product.xpath('*/span[@class="s_icon"]/text()')[0]
        message = product.xpath('h2/text()')[0]
        price = ''.join(product.xpath('div[@class="tips"]/em/text()'))
        commit = ''.join(product.xpath('div[@class="tips"]/span/text()'))
        time = product.xpath('address/span/text()')[0]
        data = {
            'URL': URL,
            '分类': category,
            '信息': message,
            '价格': price,
            '评论': commit,
            '发布时间': time
        }
        save_data(db, data)
        print(data)
        return time_sort


def test_parse_json():
    with open('smzdm.json') as f:
        json_data = ''.join(f.readlines())
        parse_json(json_data)


# 初始化数据库
def init_sql():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    # 创建数据库sdifen
    db = client.SMZDM
    return db


# 保存数据到数据库中
def save_data(db, data):
    db.SMZDM_INFO.insert(data)


# 发送邮件
def send_email(message_text):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    # 设置服务器
    mail_host = "smtp.qq.com"
    # 用户名
    mail_user = "631582864@qq.com"
    # 邮箱密码
    mail_pass = "zdugzwmxjbgvbcij"
    # 发送邮箱
    sender = '631582864@qq.com'
    # 接收邮箱
    receivers = ['a631582864@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(message_text, 'plain', 'utf-8')
    message['From'] = Header("weekly@newsletter.smzdm.com", 'utf-8')
    message['To'] = Header("a631582864@qq.com", 'utf-8')
    subject = 'SMZDM信息提醒'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def main():
    html = get_html(url)
    db = init_sql()
    time_sort = parse_html(html, db)
    while True:
        next_url = base_url + time_sort
        json_data = get_html(next_url)
        time_sort = parse_json(json_data, db)
        time.sleep(1)
    # send_email("张大妈爬虫")
    # test_parse_json()


if __name__ == '__main__':
    main()
