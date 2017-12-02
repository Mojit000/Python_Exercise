import requests
import json
import os
import time
from multiprocessing import Pool


def getHtml(url):
    """
    获取页面内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
    req = requests.get(url, headers=headers)
    return req


def getHeroID(jsonFile):
    """
    获取英雄ID（其实就是获取英雄的英文名称）
    """
    with open(jsonFile, mode='r') as f:
        heroDataDict = json.load(f)
        heroKeysDict = heroDataDict['keys']
        return heroKeysDict.values()


def getHeroURL(heroID):
    """
    构造英雄的详情页面的URL
    """
    return 'http://lol.qq.com/web201310/info-defail.shtml?id={}'.format(heroID)


def getHeroSkinJSUrl(heroID):
    """
    构造英雄皮肤JS文件的URL
    """
    return 'http://lol.qq.com/biz/hero/{}.js'.format(heroID)


def parseJSFile(heroID):
    """
    解析获取到的JS文件，并保存为JSON格式
    """
    heroSkinJS = getHtml(getHeroSkinJSUrl(heroID))
    return heroSkinJS.text[len('if(!LOLherojs)var LOLherojs={champion:{}};LOLherojs.champion.' + heroID + '='):][:-1]


def getHeroSkin(heroID):
    """
    获取英雄皮肤，并按英雄名称保存到本地
    """
    if not os.path.exists(heroID):
        os.mkdir(heroID)
    heroSkinJsonData = json.loads(parseJSFile(heroID))
    heroSkinsInfo = heroSkinJsonData['data']['skins']
    for heroSkinInfo in heroSkinsInfo:
        heroSkinName = heroSkinInfo['name']
        heroSkinID = heroSkinInfo['id']
        saveSkinImage(heroID, heroSkinID, heroSkinName)
        time.sleep(2)
    print(heroID + '皮肤下载完成')


def getSkinURL(heroSkinID):
    return 'http://ossweb-img.qq.com/images/lol/web201310/skin/big{}.jpg'.format(heroSkinID)


def saveSkinImage(path, heroSkinID, heroSkinName):
    """
    保存皮肤图片
    """
    req = requests.get(getSkinURL(heroSkinID))
    with open(path + '/' + heroSkinName + '.jpg', mode='wb') as f:
        f.write(req.content)


def main():
    # 初始化线程
    saveImagePpool = Pool(4)
    heroIDList = getHeroID('champion.json')
    saveImagePpool.map(getHeroSkin, heroIDList)
    # for heroID in getHeroID('champion.json'):
    #     getHeroSkin(heroID)
    print("皮肤下载完成")


if __name__ == '__main__':
    main()
