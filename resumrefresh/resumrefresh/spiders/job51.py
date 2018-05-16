

from urllib.parse import urlencode
import time

import scrapy
from scrapy.http.cookies import CookieJar

class Job51Spider(scrapy.Spider):
    name='job51'

    def start_requests(self):
        username=input('Please input your username:')
        passwd=input('Please input your password:')
        data={}
        data['loginname']=username
        data['password']=passwd
        data['lang']='c'
        data['action']='save'
        data['from_domain']='i'
        data['verifycode']=''
        url='https://login.51job.com/login.php'
        cookiejar=CookieJar()
        yield scrapy.FormRequest(url,formdata=data,callback=self.parser,meta={'cookiejar':cookiejar})

    def parser(self,response):
        self.resumeid=response.xpath('//div[@class="btnbox"]/span[1]/@track-resumeid').extract_first()
        data={}
        data['ResumeID']=self.resumeid
        data['lang']='c'
        self.resumeid=urlencode(data)
        url='https://i.51job.com/resume/ajax/refresh_resume.php?'+self.resumeid
        yield scrapy.Request(url,meta={'cookiejar':response.meta['cookiejar']},callback=self.refreshResult,dont_filter=True)
        

    def refreshResult(self,response):
        print("<<<",response.text)
        if 'lastupdate' in response.text:
            time.sleep(600)
            url='https://i.51job.com/resume/ajax/refresh_resume.php?'+self.resumeid
            yield scrapy.Request(url,meta={'cookiejar':response.meta['cookiejar']},callback=self.refreshResult,dont_filter=True)
