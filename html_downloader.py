# coding=utf-8
'''
Created on 2017/6/3
 @author: nwth
 description: 
'''
import urllib
from time import sleep
import http.cookiejar
#import cookielib  python2
import random
import winsound

class HtmlDownloader(object):
    useCookie1 = False #是否使用cookie
    changeCookie = False #是否需要更改cookie状态
    
    def __init__(self):
        pass

    def _set_cookie(self, fileName):
        cookie = http.cookiejar.MozillaCookieJar()
        cookie.load(fileName, ignore_discard=True, ignore_expires=True)
        opener = urllib.build_opener(urllib.HTTPCookieProcessor(cookie))
        urllib.install_opener(opener)
    
    def save_cookie(self, fileName, url): #不能在有别的实例运行时执行
        #声明一个MozillaCookieJar实例保存cookie
        cookie = http.cookiejar.MozillaCookieJar(fileName)
        #构建opener
        opener = urllib.build_opener(urllib.HTTPCookieProcessor(cookie))
        urllib.install_opener(opener)
        
        request = urllib.Request.open(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
        response = urllib.urlopen(request)
        print (response.getcode())
        cookie.save(ignore_discard=True, ignore_expires=True)
        print ('Successfully saved')
        
    def _download(self, url):
        #设置cookie信息
        if HtmlDownloader.changeCookie == True:
            HtmlDownloader.changeCookie = False
            if HtmlDownloader.useCookie1 == True: 
                print ('set cookie1')
                self._set_cookie('cookie1.txt')
            else:
                print ('set cookie2')
                self._set_cookie('cookie2.txt')        
        
        Header = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #浏览器头描述
        try:
            request = urllib.Request(url)
            request.add_header('User-Agent', Header)
            response = urllib.urlopen(request)

        #except urllib.URLError, e:
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print (e.code)
            if hasattr(e,"reason"):
                print (e.reason)
            if e.code == 403:
                winsound.Beep(600,1000) #蜂鸣发出警告，音量600， 时常1000ms
                return 403
            if e.code == 404:
                winsound.Beep(600,300) #蜂鸣发出警告，音量600， 时常300ms
                sleep(0.1)
                winsound.Beep(600,300) #蜂鸣发出警告，音量600， 时常300ms
                return 404

        if response.getcode() == 200: #200表示读取成功
                return response.read()
        
    def download(self, url):
        times = 1
        if url is None:
            return None
        while True:
            html_cont = self._download(url)
            if html_cont == 404: #404错误，返回404，然后将url放入404Urls
                return 404
            elif html_cont == 403: #如果出现403等错误，等待后继续爬取
                HtmlDownloader.changeCookie = True
                HtmlDownloader.useCookie1 = not HtmlDownloader.useCookie1
                
                sleeptime = random.randint(20, 30) * times #递增等待时间
                print ('sleeping %d times...') % times
                times += 1
                sleep(sleeptime)
            else:
                return html_cont