# coding:utf-8

list = [1,2,3,4,5]

for i in list:
    if i % 2 ==0:
        list.remove(i)

print(list)