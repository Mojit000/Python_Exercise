import requests
from lxml import etree

lolURL = 'http://lol.qq.com/web201310/info-heros.shtml#Navi'

championURL = 'http://lol.qq.com/biz/hero/champion.js'


def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
    req = requests.get(url, headers=headers)
    return req


def main():
    req = getHtml(championURL)
    with open('champion.json', mode='w') as f:
        f.write(
            req.text[len('if(!LOLherojs)var LOLherojs={};LOLherojs.champion='):][:-1])
    print(
        req.text[len('if(!LOLherojs)var LOLherojs={};LOLherojs.champion='):][:-1])


if __name__ == '__main__':
    main()