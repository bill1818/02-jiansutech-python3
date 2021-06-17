import configparser,requests
from time import sleep
import WeChat,Mail,datetime
 
class checkurl(object):
    def __init__(self,file):
        self.file=file
        self.cfg=configparser.ConfigParser()
         
    def cfg_load(self):
        self.cfg.read(self.file)
        self.allurl=self.cfg.items('yuming')
        self.reload=self.cfg.get('time','reload')
        self.mailto=self.cfg.items('mailto')
         
    def sendmessage(self,errinfo):
        wechat.send('@all',errinfo)
        for key,values in self.mailto:
            mail.send(values,errinfo,'url访问失败报警')
             
    def senderror(self,errcont):
        enow=datetime.datetime.now()
        now=enow.strftime('%Y-%m-%d %H:%M:%S')
        errfile=open('url.log','a')
        errfile.write(now)
        errfile.write(str(errcont))
        errfile.write('\n')
        errfile.close()
             
    def cfg_dump(self):
        while True:
            for k,v in self.allurl:
                checknum=0
                #设置重试错误次数
                while checknum < 5:
                    try:
                        res=requests.get(v,timeout=20)
                        print(v,res.status_code)
                        res.close()
                        if res.status_code >= 400:
                            errinfo=v+' '+str(res.status_code)
                            self.sendmessage(errinfo)
                            self.senderror(errinfo)
                        break
                    except:
                        errinfo=v+' is error'
                        print(errinfo+'\r\n请稍等,正在第',checknum+1,'次重试...')
                        sleep(1)
                        if checknum == 4:
                            print('重试仍然无法连接,正在发送微信和邮件报警...')
                            self.sendmessage(errinfo)
                            self.senderror(errinfo)
                    checknum=checknum+1
            print('-----------------------------------')
            nextcheck=0
            while nextcheck < int(self.reload):
                print('距离下次检测还剩',int(self.reload)-nextcheck,'秒')
                sleep(1)
                nextcheck=nextcheck+1
 
if __name__ =='__main__':
    mail=Mail.sendmail()
    wechat=WeChat.WeChat()
    check=checkurl('yuming.ini')
    check.cfg_load()
    check.cfg_dump()