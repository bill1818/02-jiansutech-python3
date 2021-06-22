import random
if __name__ =="__main__":    #四位数字字母验证码的生成
    checkcode="" #保存验证码的变量
    for i in range(4):
        index=random.randrange(0,4)  #生成一个0~3中的数
        if index!=i and index +1 !=i:
            checkcode +=chr(random.randint(97,122))  # 生成a~z中的一个小写字母
        elif index +1==i:
            checkcode +=chr(random.randint(65,90) ) # 生成A~Z中的一个大写字母
        else:
            checkcode +=str(random.randint(1,9))  # 数字1-9
    print(checkcode)
