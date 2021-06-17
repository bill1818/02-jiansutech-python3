import os
import http.client
import dns.resolver

iplist=[]    #定义域名IP列表变量
appdomain="www.baidu.com"    #定义业务域名

def get_iplist(domain=""):    #域名解析函数，解析成功IP将被追加到iplist
    try:
        A = dns.resolver.query(domain, 'A')    #解析A记录类型
    except Exception as e:
        print ("dns resolver error:"+str(e))
        return
    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                iplist.append(j.address)    #追加到iplist
    return True

def checkip(ip):
    checkurl=ip+":80"
    getcontent=""
    http.client.socket.setdefaulttimeout(5)    #定义http连接超时时间(5秒)
    conn=http.client.HTTPConnection(checkurl)    #创建http连接对象

    try:
        conn.request("GET", "/",headers = {"Host": appdomain})  #发起URL请求，添加host主机头                                                      
        r=conn.getresponse()
        getcontent =r.read(15)   #获取URL页面前15个字符，以便做可用性校验
#         print(getcontent)   # 输出的是b'<!DOCTYPE html>'。需要用bytes转换下
    finally:
        if getcontent==bytes("<!DOCTYPE html>", 'utf-8'):  #监控URL页的内容一般是事先定义好的，比如“HTTP200”等
            print (ip+" [OK]")
        else:
            print (ip+" [Error]" )   #此处可放告警程序，可以是邮件、短信通知

if __name__=="__main__":
    if get_iplist(appdomain) and len(iplist)>0:    #条件：域名解析正确且至少返回一个IP
        for ip in iplist:
            checkip(ip)
    else:
        print ("dns resolver error.")