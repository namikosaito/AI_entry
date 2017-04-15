#-*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

N=1000          #学習回数
ETA=0.1        #学習率
sample_no=200  #教師データの個数

#層の数
input_no=2  
hidden_no=4
output_no=2

#教師データ 2*(教師データ数)の行列を作成
b = np.ones(sample_no).reshape(sample_no,1)
teacher=np.zeros(input_no*sample_no).reshape(sample_no,input_no)
teacher[:,0]=[0.8*np.sin(2.0*np.pi*i/20)+0.1*np.random.rand() for i in range(sample_no)]
teacher[:,1]=[0.8*np.sin(4.0*np.pi*i/20)+0.1*np.random.rand() for i in range(sample_no)]
teacher=np.c_[teacher,b] #行列の連結

#出力
yout=np.zeros(output_no*sample_no).reshape(sample_no,output_no)
yout_closed=np.zeros(output_no*sample_no).reshape(sample_no,output_no)


#誤差
error=np.zeros(N)

#input-hidden間の重み
w1=2*np.random.random((hidden_no,input_no+1))-1
#hidden-output間の重み
w2=2*np.random.random((output_no,hidden_no+1))-1
#t-1のhidden-tのhiddenの重み
w3=2*np.random.random((hidden_no,hidden_no+1))-1

#学習
for loop in range(N):
    #パラメータ
    d1=np.zeros((input_no+1)*hidden_no).reshape(hidden_no,input_no+1)
    d2=np.zeros(output_no*(hidden_no+1)).reshape(output_no,hidden_no+1)
    d3=np.zeros(hidden_no*(hidden_no+1)).reshape(hidden_no,hidden_no+1)
    u = np.zeros(hidden_no*sample_no).reshape(sample_no,hidden_no)
    h = np.zeros((hidden_no+1)*sample_no).reshape(sample_no,hidden_no+1)
    v = np.zeros(output_no*sample_no).reshape(sample_no,output_no)
    y = np.zeros(output_no*sample_no).reshape(sample_no,output_no)
    y_back = np.zeros(output_no*sample_no).reshape(sample_no,output_no)
    h_back = np.zeros((hidden_no + 1)*(sample_no+1)).reshape(sample_no+1,hidden_no + 1)
    #順方向
    for t in range(sample_no):
        if(t==0):
            continue
        if(t+1<sample_no):  #一つ先の値を入れていく
            ty = np.array(teacher[t+1][:output_no])
        else: 
            ty = np.array(teacher[0][:output_no])

        #入力層→中間層
        for i in range(hidden_no):
            tmp1=0.0
            tmp2=0.0
            for j in range(input_no+1):
                tmp1+=w1[i][j]*teacher[t][j]
            for id in range(hidden_no):
                tmp2+=w3[i][id]*h[t-1][id]
            u[t][i]=tmp1+tmp2
            h[t][i]=np.tanh(u[t][i])
        h[t][hidden_no]=1.0  #バイアス

        #中間層→出力層
        for k in range(output_no):
            tmp1=0.0
            for i in range(hidden_no+1):
                tmp1+=w2[k][i]*h[t][i]
            v[t][k]=tmp1
            y[t][k]=np.tanh(v[t][k])

        #バックプロップのための計算
        for k in range(output_no):
            y_back[t][k] = (y[t][k] - ty[k]) * (1 - y[t][k] ** 2)
            error[loop]+=0.5*(y[t][k]-ty[k])**2

    #バックプロップ
    for T in range(sample_no-1,0,-1):
        for i in range(hidden_no):
            tmp1 = 0.0
            tmp2 = 0.0
            for k in range(output_no):
                tmp1+=w2[k][i]*y_back[T][k]
                #print tmp1
            for di in range(hidden_no):
                tmp2+=w3[di][i]*h_back[T+1][di]
            h_back[T][i]=(tmp1+tmp2)*(1-h[T][i]**2)
            
    for t in range(sample_no):
        if(t==0):
            continue
        for j in range(input_no + 1):
            for i in range(hidden_no):
                d1[i][j] += h_back[t][i] * teacher[t][j]

        for i in range(hidden_no + 1):
            for k in range(output_no):
                d2[k][i] += y_back[t][k] * h[t][i]

        for di in range(hidden_no+1):
            for i in range(hidden_no):
                d3[i][di]+=h_back[t][i] * h[t-1][i]

    #重み更新
    for j in range(input_no+1):
        for i in range(hidden_no):
           w1[i][j]-=ETA*d1[i][j]/(sample_no*input_no)
    for i in range(hidden_no+1):
        for k in range(output_no):
            w2[k][i]-=ETA*d2[k][i]/(sample_no*input_no)
    for di in range(hidden_no+1):
        for i in range(hidden_no):
            w3[i][di]-=ETA*d3[i][di]/(sample_no*input_no)

    print "loop="+str(loop)+", error="+str(error[loop])

#パラメータ
u = np.zeros(hidden_no*sample_no).reshape(sample_no,hidden_no)
h = np.zeros((hidden_no+1)*sample_no).reshape(sample_no,hidden_no+1)
v = np.zeros(output_no*sample_no).reshape(sample_no,output_no)
    
#オープンループで出力
for t in range(sample_no):
    for i in range(hidden_no):
        tmp1 = 0.0
        tmp2 = 0.0
        for j in range(input_no + 1):
            tmp1 += w1[i][j] * teacher[t][j]
        for id in range(hidden_no):
            tmp2 += w3[i][id] * h[t - 1][id]
        u[t][i] = tmp1 + tmp2
        h[t][i] = np.tanh(u[t][i])
    h[t][hidden_no] = 1.0

    for k in range(output_no):
        tmp1 = 0.0
        for i in range(hidden_no + 1):
            tmp1 += w2[k][i] * h[t][i]
        v[t][k] = tmp1
        yout[t][k] = np.tanh(v[t][k])
 
#クローズドループで出力 
for t in range(1, sample_no - 1):
    x=np.zeros(input_no+1)
    if(t==1):
        x=teacher[t]
    else:
        x[:input_no]=yout_closed[t-1][:]
        x[input_no]=1.0
    print x
    for i in range(hidden_no):
        tmp1 = 0.0
        tmp2 = 0.0
        for j in range(input_no + 1):
            tmp1 += w1[i][j] * x[j]
        for id in range(hidden_no):
            tmp2 += w3[i][id] * h[t - 1][id]
        u[t][i] = tmp1 + tmp2
        h[t][i] = np.tanh(u[t][i])
    h[t][hidden_no] = 1.0
    for k in range(output_no):
        tmp1 = 0.0
        for i in range(hidden_no + 1):
            tmp1 += w2[k][i] * h[t][i]
        v[t][k] = tmp1
        yout_closed[t][k] = np.tanh(v[t][k])
          
#描画
plt.subplot(311)
plt.plot(yout[:,0],yout[:,1],"r",label="training data")    #赤で学習結果を描く
plt.plot(teacher[:,0],teacher[:,1],"b",label="teaching data") #青で教師データを描く
plt.legend(loc="lower right")

plt.subplot(312)
plt.plot(yout_closed[:,0],yout_closed[:,1],"r",label="training data")    #赤で学習結果を描く
plt.plot(teacher[:,0],teacher[:,1],"b",label="teaching data") #青で教師データを描く
plt.legend(loc="lower right")

plt.subplot(313)
plt.yscale("log")
plt.plot(range(N),error)
plt.show()
