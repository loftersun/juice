#Internet Crawling Notes

##1. The Simple Http Request

###1.1 Header

为了完全模拟浏览器的工作，我们需要设置一些Headers 的属性。

    User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
    Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
    application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
    application/json ： 在 JSON RPC 调用时使用
    application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
    在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务

###1.2 DebugLog

    import urllib2
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    opener = urllib2.build_opener(httpHandler, httpsHandler)
    urllib2.install_opener(opener)
    response = urllib2.urlopen('http://www.baidu.com')

###1.3 Http Error

    req = urllib2.Request('http://blog.csdn.net/cqcre')
    try:
        urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"

###1.4 Http Proxy

    enable_proxy = True
    proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
    else:
    opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)

##2. Using Cookie to Login

###2.1 The 1st object - opener

+ Derived from urllib2.OpenerDirector, an opener is the object that we use to request an URL.
+ `urllib2.urlopen` is a simple and special opener which accepts only url, data and timeout
+ We need to build another opener to use cookie

###2.2 The 2nd module - cookielib

+ CookieJar
+ FileCookieJar
+ MozillaCookieJar
+ LWPCookieJar

Relationship:

    	         +-----------+
                | CookieJar |
                +-----+-----+
                      |
                      |
               +------v-------+
               | FileCookieJar|
               +-+----------+-+
                 |          |
                 |          |
	+----------------v-+    +v---------------+
	| MozillaCookieJar |    | LWPCookieJar   |
	+------------------+    +----------------+
	
	
###2.3 Step1: Save cookie

	import cookielib
	#声明一个CookieJar对象实例来保存cookie
	cookie = cookielib.CookieJar()
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler=urllib2.HTTPCookieProcessor(cookie)
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	#此处的open方法同urllib2的urlopen方法，也可以传入request
	response = opener.open('http://www.baidu.com')
	for item in cookie:
	    print 'Name = '+item.name
	    print 'Value = '+item.value
	   
###2.4 Step2: Save cookie to file

	import urllib2
 
	#设置保存cookie的文件，同级目录下的cookie.txt
	filename = 'cookie.txt'
	#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cookie = cookielib.MozillaCookieJar(filename)
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler = urllib2.HTTPCookieProcessor(cookie)
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	#创建一个请求，原理同urllib2的urlopen
	response = opener.open("http://www.baidu.com")
	#保存cookie到文件
	cookie.save(ignore_discard=True, ignore_expires=True)

###2.5 Step3: Read cookie from file


	import cookielib
	import urllib2
	 
	#创建MozillaCookieJar实例对象
	cookie = cookielib.MozillaCookieJar()
	#从文件中读取cookie内容到变量
	cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
	#创建请求的request
	req = urllib2.Request("http://www.baidu.com")
	#利用urllib2的build_opener方法创建一个opener
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open(req)
	print response.read()

###2.6 Step4: Login using cookie

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
    
#3. 实战 —— 糗事百科

 