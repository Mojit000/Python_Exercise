import requests
import os
from lxml import etree
# import csv

sdifen_url = 'http://www.sdifen.com/page/{page_num}/'


def get_html(url):
    resp = requests.get(url)
    html = resp.text
    if resp.status_code == 200:
        return html
    else:
        return None


def parse_html(html, db):
    root = etree.HTML(html)
    content = root.xpath('//div[@id="content"]')[0]
    articles = content.xpath('article')
    for article in articles:
        title = article.xpath(
            'header/*/*[@class="entry-title"]/a/text()|header/*[@class="entry-title"]/a/text()')[0]
        desc = os.linesep.join(article.xpath(
            'div[@class="entry-content"]/p/text()')).strip()
        app_data = {'title': title, 'desc': desc}
        save_data(db, app_data)
        # print(app_data)
        # print(title)
        # print(desc)


def init_sql():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    # 创建数据库sdifen
    db = client.sdifen
    return db


def save_data(db_name, app_data):
    db_name.app_data.insert(app_data)


def main():
    db = init_sql()
    for i in range(1, 500):
        html = get_html(sdifen_url.format(page_num=i))
        parse_html(html, db)


if __name__ == '__main__':
    main()
