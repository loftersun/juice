# -*- coding:utf-8 -*-
import urllib2
import re

def saveto(text, file):
    f = open(file, 'w')
    f.write(text)
    f.close()

def getHotpage(pageNum):
    url = 'http://www.qiushibaike.com/hot/' + str(pageNum)
    headers = {
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        #'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,pt;q=0.4'
    }
    try:
        req = urllib2.Request(url, None, headers)
        res = urllib2.urlopen(req)
        return res.read().decode('utf-8')
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print 'error code: {0}'.format(e.code)
        if hasattr(e, 'reason'):
            print 'error reason: {0}'.format(e.reason)
    except Exception as e:
        print e.message
        raise

def getJokeFromHotpage(pageNum):
    page = getHotpage(pageNum)
    if not page:
        print 'Sorry, fail to load page {0}'.format(pageNum)
        return

    # 1. .*? 是一个固定搭配：.*表示可以匹配任意字符，加上?表示非贪婪匹配
    # 2. (.*?) 是一个分组，
    # 3. rs.S 表示匹配为“点任意模式”，.可以匹配回车
    regex = '<div.*?author.*?<h2>(.*?)</h2>.*?\
content">(.*?)</div>.*?\
vote"><i class="number">(.*?)</i>.*?\
number">(.*?)</i>'
    print '\n\n{0}\n\n'.format(regex)
    pattern = re.compile(regex,re.S)
    matches = re.findall(pattern, page)
    jokes = []
    for m in matches:
        x = m[1].replace('<br/>', '\n')
        x = x.lstrip()
        y = re.sub("(.{20})", "\\1\n", x, 0, re.DOTALL)
        jokes.append([m[0], y, m[2], m[3]])

    return jokes

def main():
    jokes = getJokeFromHotpage(1)
    for joke in jokes:
        input_ = raw_input()
        if input_ == 'q' or input_ == 'Q':
            return

        print u'\n作者: {0}\n\n{1}{2}个赞\t{3}个评论\n'.format(joke[0], joke[1], joke[2], joke[3])

if __name__ == '__main__':
    main()
