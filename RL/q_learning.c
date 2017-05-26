/*
迷路抜け知識の獲得
s=14が報酬最大とする
           (0)
       (1        2)
  (3    4)      (5    6)
(7 8) (9 10) (11 12) (13 14)
             　○　        　☆
*/
#include<stdio.h>
#include<stdlib.h>

#define _CRT_SECURE_NO_WARNINGS

#define NODENO 15    //Q値のノード数
#define GENMAX 100  //学習の繰り返し回数
#define ALPHA 0.1    //学習係数
#define GAMMA 0.9    //割引率
#define EPSILON 0.3  //行動選択のランダム性を決定（閾値）
#define REWARD 1000  //報酬
#define DEPTH 3      //道のりの深さ
#define SEED 3277

int rand100();   //0~100の乱数
int rand01();    //0or1の乱数
double rand1();  //0~1の乱数
void printqvalue(int qvalue[NODENO]);   //Q値出力
int selecta(int s,int qvalue[NODENO]);  //行動選択
int updateq(int s,int qvalue[NODENO]);  //Q値更新

/***********************************/
int main(){
 int qvalue[NODENO]; //Q値
 int s; //状態
 int t; //時間
 
 srand(SEED);

 //Q値の初期化
 for(int i=0;i<NODENO;++i)qvalue[i]=rand100();
 printqvalue(qvalue);

 //学習の本体
 for(int i=0;i<GENMAX;++i){
    s=0; //行動の初期化
    for(t=0;t<DEPTH;++t){
	s=selecta(s,qvalue); //行動選択
	qvalue[s]=updateq(s,qvalue); //Q値の更新
    }
    if(i%20==0){
	for(int j=1;j<NODENO;++j)printf("s=%d\t",j);
	printf("\n");
    }
    printqvalue(qvalue);
 }
 return 0;
}

/*******************************************/
/*Q値を更新する*/
int updateq(int s,int qvalue[NODENO]){ 
 int qv;   //更新されるQ値
 int qmax; //Q値の最大値

 if(s>6){ //最下段
    if(s==14)qv=qvalue[s]+ALPHA*(1000-qvalue[s]); //報酬の付与
    else if(s==11)qv=qvalue[s]+ALPHA*(500-qvalue[s]);
    else qv=qvalue[s];
 }
 else{   //最下段以外
    if((qvalue[2*s+1])>(qvalue[2*s+2]))qmax=qvalue[2*s+1];
    else qmax=qvalue[2*s+2];
    qv=qvalue[s]+ALPHA*(GAMMA*qmax-qvalue[s]);
 }
 return qv;
}

/*行動を選択(ε-greedy)*/
int selecta(int olds,int qvalue[NODENO]){
 int s;
 if(rand1()<EPSILON){ //ランダムに行動
    if(rand01()==0)s=2*olds+1;
    else s=2*olds+2;
 }
 else{  //Q値最大値を選択
    if((qvalue[2*olds+1])>(qvalue[2*olds+2]))s=2*olds+1;
    else s=2*olds+2;
 }
 return s;
}

/*Q値表示*/
void printqvalue(int qvalue[NODENO]){
 for(int i=1;i<NODENO;++i)printf("%d\t",qvalue[i]);
 printf("\n");
}

/*乱数*/
double rand1(){  //0~1
 return (double)rand()/RAND_MAX;
}

int rand01(){ //0or1
 int rnd;
 while((rnd=rand())==RAND_MAX);
 return (int)((double)rnd/RAND_MAX*2); 
}

int rand100(){ //0~100
 int rnd;
 while((rnd=rand())==RAND_MAX);
 return (int)((double)rnd/RAND_MAX*101); 
}
