#! /usr/bin/env python   
# -*- coding: utf-8 -*-
# PTS Script record tool v0.2.6.4
# PTS脚本SDK：框架API、常用HTTP请求/响应处理API
import uuid
import time

from util import PTS
from HTTPClient import NVPair
from HTTPClient import Cookie
from HTTPClient import HTTPRequest
from HTTPClient import CookieModule

# 脚本初始化段，可以设置压测引擎的常用HTTP属性
#PTS.HttpUtilities.setKeepAlive(False)
#PTS.HttpUtilities.setUrlEncoding('GBK')
#PTS.HttpUtilities.setFollowRedirects(False)
#PTS.HttpUtilities.setUseCookieModule(False)
PTS.HttpUtilities.setUseContentEncoding(True)
PTS.HttpUtilities.setUseTransferEncoding(True)

## 如想通过ECS内网IP进行压测，必须在下方“innerIp”备注行中输入ECS内网IP，如有多个请以英文逗号分隔，例如：127.0.0.1,127.0.0.2
# innerIp:

## 脚本执行单元类，每个VU/压测线程会创建一个TestRunner实例对象
class TestRunner:
    # TestRunner对象的初始化方法，每个线程在创建TestRunner后执行一次该方法
    def __init__(self):
        self.threadContext = PTS.Context.getThreadContext()
        self.init_cookies = CookieModule.listAllCookies(self.threadContext)
        self.dealApiURL = "https://deal-api.kuick.cn"
        
    # 主体压测方法，每个线程在测试生命周期内会循环调用该方法
    def __call__(self):
        PTS.Data.delayReports = 1
        for c in self.init_cookies:
            CookieModule.addCookie(c, self.threadContext)
            
        # DealUser注册
        result = self.registerDealUser()
        PTS.Framework.setExtraData(result["statusCode"])    
        dealUserId = result["dealUserId"]
        accessToken = result["accessToken"]

        # 开始访问网站
        result = self.startAccessSite(dealUserId, accessToken)
        PTS.Framework.setExtraData(result["statusCode"]) 
        logId = result["logId"]

        # 循环控制器
        for i in range(1, 5):
            pageNum = str(i)

            # 开始访问页面
            result = self.startViewPage(dealUserId, logId, pageNum, accessToken)
            PTS.Framework.setExtraData(result["statusCode"]) 
            viewLogId = result["viewLogId"]

            for j in range(5):
                # 线程睡眠1秒
                PTS.Thread.sleep(5000)

                # 定时更新页面访问结束时间
                statusCode = self.updateViewPageEndTime(dealUserId, logId, pageNum, viewLogId, accessToken)
                PTS.Framework.setExtraData(statusCode) 
                
                # 提交关键行为
                statusCode = self.submitKeyBehaviour(dealUserId, logId, pageNum, viewLogId, accessToken)
                PTS.Framework.setExtraData(statusCode) 
        
        PTS.Data.report()
        PTS.Data.delayReports = 0
        
    # TestRunner销毁方法，每个线程循环执行完成后执行一次该方法
    def __del__(self):
        for c in self.init_cookies:
            CookieModule.addCookie(c, self.threadContext)
    # 定义请求函数

    ## DealUser注册
    def registerDealUser(self):
        statusCode = [0L, 0L, 0L, 0L]        

        deviceId = str(uuid.uuid4())
        PTS.Logger.info("registerDealUser deviceId: " + deviceId)

        headers = [ 
            NVPair('Accept', '*/*'), 
            NVPair('X-DevTools-Emulate-Network-Conditions-Client-Id', 'b00fce11-e264-4396-8f10-7ad3c757b914'), 
            NVPair('Referer', 'https://deal-admin.kuick.cn'), 
            NVPair('Accept-Encoding', 'gzip, deflate, sdch, br'), 
            NVPair('Accept-Language', 'zh-CN,zh;q=0.8'), 
            NVPair('User-Agent', 'PTS-HTTP-CLIENT')
        ]
        PTS.Logger.info(headers)
        
        datas = [
            NVPair('appKey', 'eece093a-64cb-4857-a8c1-e2831452c8d5'),
            NVPair('appUserId', 'eece093a-64cb-4857-a8c1-e2831452c8d5'),
            NVPair('deviceId', deviceId),
            NVPair('fromType', 'PTS')
        ]
        PTS.Logger.info(datas)

        result = HTTPRequest().POST(self.dealApiURL + '/api/v1.0/deal-user/register', 
            datas, headers
        )
        PTS.Logger.info(result)
        PTS.Framework.addHttpCode(result.getStatusCode(), statusCode)

        ## statusCode[0]代表http code < 300 个数,    statusCode[1] 代表 300<=http code<400 个数
        # statusCode[2]代表400<=http code<500个数，  statusCode[3] 代表 http code >=500个数
        # 如果http code 300 到 400 之间是正常的
        # 那么判断事务失败，请将statusCode[1:3] 改为   statusCode[2:3] 即可
        if(sum(statusCode[2:3]) > 0):
            PTS.Data.forCurrentTest.success = False
            PTS.Logger.error(u'事务请求中http 返回状态大于300，请检查请求是否正确!')

        dealUserId = PTS.HttpUtilities.valueFromBodyBetween("id\":\"", "\"")
        accessToken = PTS.HttpUtilities.valueFromBodyBetween("access_token\":\"", "\"")

        PTS.Logger.info("registerDealUser return dealUserId: " + str(dealUserId))
        PTS.Logger.info("registerDealUser return accessToken: " + str(accessToken))

        return {
            "statusCode": statusCode,
            "dealUserId": dealUserId,
            "accessToken": accessToken
        }

    ## 开始访问网站
    def startAccessSite(self, dealUserId, accessToken):
        statusCode = [0L, 0L, 0L, 0L]

        PTS.Logger.info("startAccessSite dealUserId: " + dealUserId)
        PTS.Logger.info("startAccessSite accessToken: " + accessToken)

        headers = [ 
            NVPair('Accept', '*/*'), 
            NVPair('X-DevTools-Emulate-Network-Conditions-Client-Id', 'b00fce11-e264-4396-8f10-7ad3c757b914'), 
            NVPair('Referer', 'https://deal-admin.kuick.cn'), 
            NVPair('Accept-Encoding', 'gzip, deflate, sdch, br'), 
            NVPair('Accept-Language', 'zh-CN,zh;q=0.8'), 
            NVPair('User-Agent', 'PTS-HTTP-CLIENT'),
            NVPair('Authorization', 'Bearer ' + accessToken)
        ]
        
        datas = [
            NVPair('clientName', 'PTS'),
            NVPair('clientVersion', '3.1.0'),
            NVPair('os', 'Linux'),
            NVPair('osVersion', '2.6.0'),
            NVPair('net', 'WIFI'),
            NVPair('system', 'Linux 2.6.0'),
            NVPair('referrer', 'http://www.pts.client'),
            NVPair('site', 'www.pts.client')
        ]
         
        result = HTTPRequest().POST(self.dealApiURL + '/api/v1.0/deal-user/' + dealUserId + '/web-access-logs', 
            datas, headers
        )
        
        PTS.Framework.addHttpCode(result.getStatusCode(), statusCode)

        ## statusCode[0]代表http code < 300 个数,    statusCode[1] 代表 300<=http code<400 个数
        # statusCode[2]代表400<=http code<500个数，  statusCode[3] 代表 http code >=500个数
        # 如果http code 300 到 400 之间是正常的
        # 那么判断事务失败，请将statusCode[1:3] 改为   statusCode[2:3] 即可
        if(sum(statusCode[1:3]) > 0):
            PTS.Data.forCurrentTest.success = False
            PTS.Logger.error(u'事务请求中http 返回状态大于300，请检查请求是否正确!')

        logId = PTS.HttpUtilities.valueFromBodyBetween("id\":\"", "\"")
        PTS.Logger.info("startAccessSite return logId:" + str(logId))

        return {
            "statusCode": statusCode,
            "logId": logId
        }

    ## 开始访问网站
    def startViewPage(self, dealUserId, logId, pageNum, accessToken):
        statusCode = [0L, 0L, 0L, 0L]

        PTS.Logger.info("startViewPage dealUserId: " + dealUserId)
        PTS.Logger.info("startViewPage logId: " + logId)
        PTS.Logger.info("startViewPage pageNum: " + pageNum)
        PTS.Logger.info("startViewPage accessToken: " + accessToken)

        headers = [ 
            NVPair('Accept', '*/*'), 
            NVPair('X-DevTools-Emulate-Network-Conditions-Client-Id', 'b00fce11-e264-4396-8f10-7ad3c757b914'), 
            NVPair('Referer', 'https://deal-admin.kuick.cn'), 
            NVPair('Accept-Encoding', 'gzip, deflate, sdch, br'), 
            NVPair('Accept-Language', 'zh-CN,zh;q=0.8'), 
            NVPair('User-Agent', 'PTS-HTTP-CLIENT'),
            NVPair('Authorization', 'Bearer ' + accessToken)
        ]
        
        datas = [
            NVPair('title', 'Titie_' + pageNum),
            NVPair('url', 'http://www.jmeter.client/page_' + pageNum),
            NVPair('system', 'Windows7'),
            NVPair('client', 'JMeter 3.1.0'),
            NVPair('identity', 'page_' + pageNum)
        ]
         
        result = HTTPRequest().POST(self.dealApiURL + '/api/v1.0/deal-user/' + dealUserId + '/web-access-logs/' + logId + '/web-page-view-logs', 
            datas, headers
        )
        
        PTS.Framework.addHttpCode(result.getStatusCode(), statusCode)

        ## statusCode[0]代表http code < 300 个数,    statusCode[1] 代表 300<=http code<400 个数
        # statusCode[2]代表400<=http code<500个数，  statusCode[3] 代表 http code >=500个数
        # 如果http code 300 到 400 之间是正常的
        # 那么判断事务失败，请将statusCode[1:3] 改为   statusCode[2:3] 即可
        if(sum(statusCode[1:3]) > 0):
            PTS.Data.forCurrentTest.success = False
            PTS.Logger.error(u'事务请求中http 返回状态大于300，请检查请求是否正确!')

        viewLogId = PTS.HttpUtilities.valueFromBodyBetween("id\":\"", "\"")
        PTS.Logger.info("startViewPage return viewLogId:" + str(viewLogId))

        return {
            "statusCode": statusCode,
            "viewLogId": viewLogId
        }

    ## 定时更新页面访问结束时间
    def updateViewPageEndTime(self, dealUserId, logId, pageNum, viewLogId, accessToken):
        statusCode = [0L, 0L, 0L, 0L]

        PTS.Logger.info("startViewPage dealUserId: " + dealUserId)
        PTS.Logger.info("startViewPage logId: " + logId)
        PTS.Logger.info("startViewPage viewLogId: " + viewLogId)
        PTS.Logger.info("startViewPage pageNum: " + pageNum)
        PTS.Logger.info("startViewPage accessToken: " + accessToken)

        headers = [ 
            NVPair('Accept', '*/*'), 
            NVPair('X-DevTools-Emulate-Network-Conditions-Client-Id', 'b00fce11-e264-4396-8f10-7ad3c757b914'), 
            NVPair('Referer', 'https://deal-admin.kuick.cn'), 
            NVPair('Accept-Encoding', 'gzip, deflate, sdch, br'), 
            NVPair('Accept-Language', 'zh-CN,zh;q=0.8'), 
            NVPair('User-Agent', 'PTS-HTTP-CLIENT'),
            NVPair('Authorization', 'Bearer ' + accessToken)
        ]
        
        result = HTTPRequest().GET(self.dealApiURL + '/api/v1.0/deal-user/' + dealUserId + '/web-access-logs/' + logId + '/web-page-view-logs/' + viewLogId + '?_method=PUT&endTime=' + str(time.time()), 
            None, headers
        )
        
        PTS.Framework.addHttpCode(result.getStatusCode(), statusCode)

        ## statusCode[0]代表http code < 300 个数,    statusCode[1] 代表 300<=http code<400 个数
        # statusCode[2]代表400<=http code<500个数，  statusCode[3] 代表 http code >=500个数
        # 如果http code 300 到 400 之间是正常的
        # 那么判断事务失败，请将statusCode[1:3] 改为   statusCode[2:3] 即可
        if(sum(statusCode[1:3]) > 0):
            PTS.Data.forCurrentTest.success = False
            PTS.Logger.error(u'事务请求中http 返回状态大于300，请检查请求是否正确!')

        return statusCode

    ## 提交关键行为
    def submitKeyBehaviour(self, dealUserId, logId, pageNum, viewLogId, accessToken):
        statusCode = [0L, 0L, 0L, 0L]

        PTS.Logger.info("startViewPage dealUserId: " + dealUserId)
        PTS.Logger.info("startViewPage logId: " + logId)
        PTS.Logger.info("startViewPage viewLogId: " + viewLogId)
        PTS.Logger.info("startViewPage pageNum: " + pageNum)
        PTS.Logger.info("startViewPage accessToken: " + accessToken)

        headers = [ 
            NVPair('Accept', '*/*'), 
            NVPair('X-DevTools-Emulate-Network-Conditions-Client-Id', 'b00fce11-e264-4396-8f10-7ad3c757b914'), 
            NVPair('Referer', 'https://deal-admin.kuick.cn'), 
            NVPair('Accept-Encoding', 'gzip, deflate, sdch, br'), 
            NVPair('Accept-Language', 'zh-CN,zh;q=0.8'), 
            NVPair('User-Agent', 'PTS-HTTP-CLIENT'),
            NVPair('Authorization', 'Bearer ' + accessToken)
        ]
        
        datas = [
            NVPair('action', 'behaviour_' + pageNum),
            NVPair('description', '行为测试'),
            NVPair('content', ''),
            NVPair('start_time', str(time.time()))
        ]
         
        result = HTTPRequest().POST(self.dealApiURL + '/api/v1.0/deal-user/' + dealUserId + '/web-page-view-logs/' + viewLogId + '/behaviour-logs', 
            datas, headers
        )
        
        PTS.Framework.addHttpCode(result.getStatusCode(), statusCode)

        ## statusCode[0]代表http code < 300 个数,    statusCode[1] 代表 300<=http code<400 个数
        # statusCode[2]代表400<=http code<500个数，  statusCode[3] 代表 http code >=500个数
        # 如果http code 300 到 400 之间是正常的
        # 那么判断事务失败，请将statusCode[1:3] 改为   statusCode[2:3] 即可
        if(sum(statusCode[1:3]) > 0):
            PTS.Data.forCurrentTest.success = False
            PTS.Logger.error(u'事务请求中http 返回状态大于300，请检查请求是否正确!')

        return statusCode

# 编织压测事务
PTS.Framework.instrumentMethod(u'网站行为记录收集', 'registerDealUser', TestRunner)
PTS.Framework.instrumentMethod(u'网站行为记录收集', 'startAccessSite', TestRunner)
PTS.Framework.instrumentMethod(u'网站行为记录收集', 'startViewPage', TestRunner)
PTS.Framework.instrumentMethod(u'网站行为记录收集', 'updateViewPageEndTime', TestRunner)
PTS.Framework.instrumentMethod(u'网站行为记录收集', 'submitKeyBehaviour', TestRunner)