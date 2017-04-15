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

#教師データ(8の字) 2*(教師データ数)の行列を作成 
teacher=np.zeros(input_no*sample_no).reshape(sample_no,input_no)
teacher[:,0]=[0.8*np.sin(2.0*np.pi*i/20)+0.1*np.random.rand() for i in range(sample_no)]
teacher[:,1]=[0.8*np.sin(4.0*np.pi*i/20)+0.1*np.random.rand() for i in range(sample_no)]

#出力
yout=np.zeros(output_no*sample_no).reshape(sample_no,output_no)

#誤差
error=np.zeros(N)

#input-hidden間の重み
w1=2*np.random.random((hidden_no,input_no+1))-1
#hidden-output間の重み
w2=2*np.random.random((output_no,hidden_no+1))-1

#学習
#I(teacher→x) → H(u→h) → O(v→y)
for loop in range(N):
    d1=np.zeros((input_no+1)*hidden_no).reshape(hidden_no,input_no+1)
    d2=np.zeros(output_no*(hidden_no+1)).reshape(output_no,hidden_no+1)

    for n in range(sample_no):
        #パラメータ設定
        x = np.array(teacher[n])
        if(n+1<sample_no):
            ty = np.array(teacher[n+1]) #一つ先の値を入れていく
        else:
            ty = np.array(teacher[0])
        u = np.zeros(hidden_no) 
        h = np.zeros(hidden_no)
        v=np.zeros(output_no)
        y = np.zeros(output_no)
        y_back = np.zeros(output_no).reshape(output_no, 1)
        h_back = np.zeros(hidden_no + 1).reshape(hidden_no + 1, 1)
        
        #hiddenのバイアスを入れる
        x = np.insert(x, 1, 1)
        x = np.reshape(x,(output_no+1,1))

        #入力層→中間層
        for i in range(hidden_no):
            tmp=0.0
            for j in range(input_no+1):
                tmp+=w1[i][j]*x[j]
            u[i]=tmp
            h[i]=np.tanh(u[i])
        h=np.insert(h,hidden_no,1.0).reshape(hidden_no+1,1) #バイアス

        #中間層→出力層
        for k in range(output_no):
            tmp=0.0
            for i in range(hidden_no+1):
                tmp+=w2[k][i]*h[i]
            v[k]=tmp
            y[k]=np.tanh(tmp)

        #ここからバックプロップ

        #出力層→中間層
        for k in range(output_no):
            y_back[k]=(y[k]-ty[k])*(1-y[k]**2)
            error[loop]+=0.5*(y[k]-ty[k])**2   #エラー計算

        #中間層→入力層
        for i in range(hidden_no):
            tmp=0.0
            for j in range(output_no):
                tmp+=w2[j][i]*y_back[j]
            h_back[i]=tmp*(1-h[i]**2)

        #勾配を計算
        for j in range(input_no + 1):
            for i in range(hidden_no):
                d1[i][j] += h_back[i] * x[j]
        for i in range(hidden_no+1):
            for k in range(output_no):
                d2[k][i] += y_back[k] * h[i]
                
    #重みのアップデート             
    for j in range(input_no+1):
        for i in range(hidden_no):
           w1[i][j]=w1[i][j]-ETA*d1[i][j]/(sample_no*input_no)
    for i in range(hidden_no+1):
        for k in range(output_no):
            w2[k][i]=w2[k][i]-ETA*d2[k][i]/(sample_no*input_no)
    print "loop="+str(loop)+", error="+str(error[loop])
    
            
#クローズドループで出力していく
for n in range(sample_no):
    x = np.array(teacher[n])
    if (n + 1 < sample_no):
        ty = np.array(teacher[n + 1])
    else:
        ty = np.array(teacher[0])
    h = np.zeros(hidden_no)
    y = np.zeros(output_no).reshape(input_no, 1)
    y_back = np.zeros(output_no).reshape(output_no, 1)
    h_back = np.zeros(hidden_no + 1).reshape(hidden_no + 1, 1)
    x = np.insert(x, 1, 1)
    x = np.reshape(x, (output_no + 1, 1))

    for i in range(hidden_no):
        tmp = 0.0
        for j in range(input_no + 1):
            tmp += w1[i][j] * x[j]
        h[i] = np.tanh(tmp)
    h = np.insert(h, hidden_no, 1.0).reshape(hidden_no + 1, 1)

    for k in range(output_no):
        tmp = 0.0
        for i in range(hidden_no + 1):
            tmp += w2[k][i] * h[i]
        y[k] = np.tanh(tmp)
        yout[n][k] = y[k]

        
#描画
plt.subplot(211)
plt.plot(yout[:,0],yout[:,1],"r",label="training data")    #赤で学習結果を描く
plt.plot(teacher[:,0],teacher[:,1],"b",label="teaching data") #青で教師データを描く
plt.legend(loc="lower right")
plt.subplot(212)
plt.yscale("log")
plt.plot(range(N),error)
plt.show()
