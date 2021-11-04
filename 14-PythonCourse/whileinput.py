#coding: utf-8

a = 0 
while a< 3:
    s = input("input you lang:")
    if s == "python":
        print("your lang is: {0}".format(s))
        break
    else:
        a += 1
        print("a=", a)