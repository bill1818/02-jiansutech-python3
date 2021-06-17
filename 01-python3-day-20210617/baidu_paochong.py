#!/usr/local/env python
from tkinter import *
import re,os,requests,hashlib,threading
from PIL import Image
 
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.school=threading.local()
        self.pack()
        self.createWidgets()
 
    def createWidgets(self):
        self.nameLabel=Label(self,text='请输入关键词:')
        self.nameLabel.grid(row=0,sticky=W)
         
        self.nameInput = Entry(self)
        self.nameInput.grid(row=0,column=1)
         
        self.picys=IntVar()
        self.Checkbutton = Checkbutton(self,text='图片压缩',variable=self.picys)
        self.Checkbutton.grid(row=1,column=0,columnspan=2,sticky=W)
         
        self.alertButton = Button(self, text='下载',command=self.gorun)
        self.alertButton.grid(row=1,column=1,sticky=E)
 
    def cddir(self):
        keyword=self.nameInput.get()
        os.chdir('C:\\Users\\Administrator\\Desktop\\')
        if os.path.exists(keyword) ==False:
            os.mkdir(keyword)
        os.chdir(keyword)
         
    def gorun(self):
        self.cddir()
        word=self.nameInput.get()
        x=0
        for i in range(5):
            t=threading.Thread(target=self.xiazai,args=(x,word,))
            t.start()
            x+=20
            if i == 4:
                t.join()
                self.delfile()
                if self.picys.get() == 1:
                    self.suoxiao()
    def xiazai(self,page,word):
        baidupn=self.school.student=page
        num=1
        for i in range(50):
            url='https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8'
            payload={'word':word,'pn':baidupn}
            html = requests.get(url,params=payload).text
            regular='"objURL":"(.*?)",'
            pic=re.findall(regular,html)
            baidupn+=100
 
            for tu in pic:
                try:
                    dl=requests.get(tu,timeout=60)
                    pic_name=os.path.basename(tu)
                    if pic_name in os.walk(os.getcwd()):
                        continue
                    else:
                        if ('?' in pic_name) or ('&' in pic_name) or ('.' not in pic_name):
                            pic_name='%s%s' %(num,'.jpg')
                        with open(pic_name,"wb") as code:
                            code.write(dl.content)
                            requests.session().keep_alive = False
                            dl.close()
                        num+=1
                except requests.exceptions.ConnectionError:
                    #print('这张图片下载失败了,图片地址',tu)
                    continue
         
    def suoxiao(self):
        self.cddir()
        filedir=os.walk(os.getcwd())
        for i in filedir:
            for tplb in i[2]:
                if ('jpg' in tplb) or ('jpeg' in tplb):
                    try:
                        im=Image.open(tplb)
                        w,h=im.size
                        if w > 500:
                            im.thumbnail((w//2,h//2))
                            im.save(tplb,'jpeg')
                        im.close()
                    except OSError:
                        print('跳过此文件')
 
    def md5sum(self,filename):
        f=open(filename, 'rb')
        md5=hashlib.md5()
        while True:
            fb = f.read(8096)
            if not fb:
                break
            md5.update(fb)
        f.close()
        return (md5.hexdigest())
 
    def delfile(self):
        all_md5={}
        self.cddir()
        filedir=os.walk(os.getcwd())
        for i in filedir:
            for tlie in i[2]:
                if self.md5sum(tlie) in all_md5.values():
                    os.remove(tlie)
                else:
                    all_md5[tlie]=self.md5sum(tlie)
 
 
 
app=Application()
app.master.title('图片下载器')
app.mainloop()