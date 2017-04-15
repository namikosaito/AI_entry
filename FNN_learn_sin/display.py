# -*-coding:utf-8 -*-

import numpy as np
import csv
import matplotlib.pyplot as plt

def read_error():
    f=open('ERROR.csv','r')
    data=csv.reader(f)
    y=[]
    for row in data:
        y.append(float(row[0]))
    f.close()
    plt.subplot(211) #画面の上
    plt.title('Error')
    plt.ylim([0,3])
    plt.plot(y)

def result():
    f_teacher_x=open('INPUT_x.csv','r')
    data=csv.reader(f_teacher_x)
    teacher_x=[]
    for row in data:
        teacher_x.append(float(row[0]))
    f_teacher_x.close()

    f_teacher_y=open('INPUT_y.csv','r')
    data=csv.reader(f_teacher_y)
    teacher_y=[]
    for row in data:
        teacher_y.append(float(row[0]))
    f_teacher_y.close()

    f_test_x=open('OUTPUT_x.csv','r')
    data=csv.reader(f_test_x)
    test_x=[]
    for row in data:
        test_x.append(float(row[0]))
    f_test_x.close()

    f_test_y=open('OUTPUT_y.csv','r')
    data=csv.reader(f_test_y)
    test_y=[]
    for row in data:
        test_y.append(float(row[0]))
    f_test_y.close()
    X=np.arange(0,6.28,0.01)

    plt.subplot(212) #画面の下
    plt.title('Result')
    plt.plot(X,np.sin(X),color="c",linewidth=3)
    plt.plot(teacher_x,teacher_y,"o",markersize=8,color="b",label="teacher")
    plt.plot(test_x,test_y,"o",markersize=4,label="result",color="r")
     
def main():
    read_error()
    result()
    plt.show()
    
if __name__=="__main__":
    main()
