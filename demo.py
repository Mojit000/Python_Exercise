from lxml import etree
import codecs

homepage_url = 'http://www.jianshu.com'

def get_html():
    with codecs.open('weekly_other.txt','r', encoding='utf-8') as f:
        return ''.join(f)

def parse_other_html(html):
    root = etree.HTML(html)
    articles = root.xpath('//li/div[@class="content"]')
    seen_snote_ids = root.xpath('//li/@data-note-id')
    print(seen_snote_ids)
    for article in articles:
        author = ''.join(article.xpath('div[@class="author"]/div[@class="name"]/a/text()'))
        author_url = homepage_url + ''.join(article.xpath('div[@class="author"]/div[@class="name"]/a/@href'))
        title = ''.join(article.xpath('a[@class="title"]/text()'))
        article_url = homepage_url + ''.join(article.xpath('a[@class="title"]/@href'))
        abstract = ''.join(article.xpath('p[@class="abstract"]/text()')).strip()
        read_and_comments = article.xpath('div[@class="meta"]/a/text()')
        like_and_pay = article.xpath('div[@class="meta"]/span/text()')
        # 数据处理
        read_and_comments = ''.join(read_and_comments).strip().split()
        like_and_pay = ''.join(like_and_pay).strip().split()
        # read_count = meta.xpath('a/text()')
        print(author, author_url, title, article_url, abstract, read_and_comments, like_and_pay)
        print('?seens_snote_ids%5B%5D=' + '?seens_snote_ids%5B%5D='.join(seen_snote_ids))

def main():
    html = get_html()
    parse_other_html(html)

if __name__ == '__main__':
    main()