file1 = open("name,tel.txt", "rb")
#!/usr/bin/evn python3
# python如何将两个txt文件内容合并

file2 = open("name,email.txt", "rb")
 
file_list1 = file1.readlines() # 将所有变量读入列表file_list1
file_list2 = file2.readlines() # 将所有变量读入列表file_list2
# print(type(file1))
  
# 定义各属性数据存储列表
file_list1_name = []
file_list1_tel = []
file_list2_name = []
file_list2_email = []
 
  
# 遍历file_list1 列表 将得到的信息进行下列操作
for message in file_list1:
  
  temp_list = message.split()
  # 将txt文件中的第一行 也就是file_list1 列表的第一项 用split方法操作 以空格为分隔符 分成两部分继续放到temp_list列表里
  
  file_list1_name.append(str(temp_list[0].decode('gbk')))  # 包含中文 选gbk
  file_list1_tel.append(str(temp_list[1].decode('gbk')))
  
 # 操作与file_list1列表完全相同
 for message in file_list2:
   temp_list = message.split()
 
   file_list2_name.append(str(temp_list[0].decode('gbk')))
   file_list2_email.append(str(temp_list[1].decode('gbk')))
  
  
 # print(len(file_list1_name))
 
 # 选择与file_list2中的名称相同的file_list1中的名称并合并
 file_list3 = []
 for i in range(len(file_list1_name)):
  s = ''
  if file_list1_name[i] in file_list2_name:
    j = file_list2_name.index(file_list1_name[i]) #列表index方法 查找括号内对象 返回值为索引位置
 
    s = '\t'.join([file_list1_name[i], file_list1_tel[i], file_list2_email[j]])
    # 字符串join方法连接三个属性,之间以(\t 制表位)隔开
 
    s += '\n'
   else:
     s = '\t'.join([file_list1_name[i], file_list1_tel[i], str("--------------")])
     s += '\n'
  file_list3.append(s)
  
 # 选择file_list1中的名称与file_list2中的名称不相同的
 for i in range(len(file_list2_name)):
   s = ''
   if file_list2_name[i] not in file_list1_name:
     s = '\t'.join([file_list2_name[i], str('--------------'), file_list2_email[i]])
     s += '\n'
   file_list3.append(s)
  
  
# 将数据写入file3
file3 = open("三属性合并.txt", "w")
file3.writelines(file_list3)
  
# 关闭文件
file1.close()
file2.close()
file3.close()