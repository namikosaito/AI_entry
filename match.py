# -*-coding:utf-8 -*-
import random
Beans=20
Learn=0
Test=1
MaxLevel=3 #縦深さ
GoodGoal=31 #正解
Prize=5 #報酬
lcount=0 #学習回数

#rnd=random.random() #0.0~1.0までのランダムなfloat値

#ノードも書かなきゃいけないから面倒だけど39行必要
match_box=[\
       [3,[Beans,Beans,Beans],[1,2,3]],\
       [3,[Beans,Beans,Beans],[4,5,6]],\
       [3,[Beans,Beans,Beans],[7,8,9]],\
       [3,[Beans,Beans,Beans],[10,11,12]],\
       [3,[Beans,Beans,Beans],[13,14,15]],\
       [3,[Beans,Beans,Beans],[16,17,18]],\
       [3,[Beans,Beans,Beans],[19,20,21]],\
       [3,[Beans,Beans,Beans],[22,23,24]],\
       [3,[Beans,Beans,Beans],[25,26,27]],\
       [3,[Beans,Beans,Beans],[28,29,30]],\
       [3,[Beans,Beans,Beans],[31,32,33]],\
       [3,[Beans,Beans,Beans],[34,35,36]],\
       [3,[Beans,Beans,Beans],[37,38,39]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
       [0,[Beans,Beans,Beans],[-1,-1,-1]],\
]

select=[0]*(MaxLevel+1) #[1][2][3]に選ぶルートが入力されていく
nsselect=[0]*(MaxLevel+1) #各マッチ箱の選んだ色が入力されていく

def next_select(pmatch): #次のルートを選びうるものの中からランダムに選択する
    rnd=random.random()
    a=0
    b=0
    for x in match_box[pmatch][1]:
        b+=x
    
    i=0
    for x in match_box[pmatch][1]:
        a+=x
        i+=1
        if b!=0:
            #print rnd,a,b,float(a)/b
            if rnd<float(a)/b: #floatをつけないと1or0になるから注意
                return i-1
    return i-2
            
            
def execute():
    lv=1
    ns=0
    select[0]=0
    nsselect[0]=0
    while lv<=MaxLevel:
        ns=next_select(select[lv-1]) #match_boxの３番めの配列を指定
        if match_box[select[lv-1]][1][ns]<1: #その色のビーズが入っていなかったら
            print "Error"
            break
        select[lv]=match_box[select[lv-1]][2][ns]  
        nsselect[lv]=ns #1~3
        lv+=1


def learn(): #罰か報酬を与える
    if select[MaxLevel]!=GoodGoal:
        lv=1
        while lv<=MaxLevel:
            match_box[select[lv]][1][nsselect[lv]]-=1 #間違っていたらビーズ没収
            lv+=1
    else:
        lv=1
        while lv<=MaxLevel:
            match_box[select[lv]][1][nsselect[lv]]+=Prize #合っていたら報酬
            lv+=1

def print_path(mode,cycle):
    if mode==Learn:
        print "learning now!"
    else:
        print "Test cycle["+str(cycle)+"]"\
            +" (1-"+str(select[1])+")"\
            +"->(2-"+str(select[2]-3)+")"\
            +"->(3-"+str(select[3]-12)+")"

def print_result(tcycle):
    rate=(100.0*goodcount)/tcycle
    print "Learning cycle:"+str(lcount)
    print "Test cycle:"+str(tcycle)
    print "Good:"+str(goodcount)+"(rate:"+str(rate)+"%)"
        
#//////main/////////////////////////////////
x=1
while x>0:
    print "Learning Mode"
    print "Key in Learning cycle"
    i=0
    lc=input() #学習回数を決める
    while i<lc:
        execute()
       # print_path(Learn,i+1)
        learn()
        i+=1
    lcount+=lc #学習回数入力

    goodcount=0
    print "Test Mode"
    print "Key in Test cycle"
    i=0
    lc=input() #クローズドループのテスト回数を決める
    while i<lc: 
        execute()
        print_path(Test,i+1)
        if select[MaxLevel]==GoodGoal: #正解にたどり着いたら
            goodcount+=1
        i+=1
    print_result(lc)
    break
