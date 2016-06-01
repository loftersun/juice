# -*- encoding=utf8 -*-

import urllib2

def httpGetAnswer(questionUrl, output):
    url = questionUrl
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,pt;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': user_agent
    }
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request, timeout = 10)
    page = response.read()

    f = open(output, 'w')
    f.write(page)
    f.close()

def main():
    httpGetAnswer('http://www.zhihu.com/question/30957011', 'zhihu-answer-30957011.html')

if __name__ == '__main__':
    main()
