# -*- encoding=utf8 -*-
import urllib
import urllib2
import re
import cookielib

username = 'yyyyyyyy'
password = 'xxxxxxxx'

def save(text, file):
    f = open(file, 'w')
    f.write(text)
    f.close()

def requestXSRF():
    # 打开目标链接，获取Html
    url = 'http://www.zhihu.com'
    zhihu = urllib.urlopen(url)
    contents = zhihu.read()

    # 获取xsrf值
    reg = r'name="_xsrf" value="(.*)"/>'
    pattern = re.compile(reg)
    result = pattern.findall(contents)
    xsrf = result[0]
    print xsrf
    return xsrf

def login():
    xsrf = requestXSRF()

    lgurl = 'https://www.zhihu.com/login/email'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,pt;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer':'http://www.zhihu.com/',
        'User-Agent': user_agent
    }
    post_data = {
        '_xsrf':xsrf,
        'email':username,
        'password':password,
        'rememberme':'true',
        'captcha_type':'cn'
    }
    dt = urllib.urlencode(post_data)
    req = urllib2.Request(lgurl, dt, headers)

    cookie = cookielib.MozillaCookieJar('output/cookie.txt')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)

    response = opener.open(req)
    cookie.save(ignore_discard=True, ignore_expires=True)
    page = response.read()
    save(page, 'output/zhihu-login.html')

    #Test
    testPage = opener.open('http://www.zhihu.com/settings/account')
    save(testPage.read(), 'output/zhihu-account.html')

def main():
    login()

if __name__ == '__main__':
    main()
