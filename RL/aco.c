#include<stdio.h>
#include<stdlib.h>

#define _CRT_SECURE_NO_WARNINGS

#define NOA 10       //蟻の個体数
#define ILIMIT 20    //繰り返しの回数
#define Q 3 	     //フェロモン更新の定数
#define RHO 0.8      //蒸発の定数
#define STEP 10      //道のりのステップ数
#define EPSILON 0.15 //行動選択のランダム性を決定
#define SEED 31      //乱数のシード

void printp(double pheromone[2][STEP]); //表示
void printmstep(int mstep[NOA][STEP]);  //蟻の挙動の表示
void walk(int cost[2][STEP],double phenomenone[2][STEP],
		int mstep[NOA][STEP]);  //蟻を歩かせる
void update(int cost[2][STEP],double pheromone[2][STEP],
		int mstep[NOA][STEP]);  //フェロモンの更新
double rand1();
int rand01(); 

/**************************************************************/
int main(){
 int cost[2][STEP]={ //各ステップのコスト(距離が短い方を１、長い方を５とする)
    {1,1,1,1,1,1,1,1,1,1},
    {5,5,5,5,5,5,5,5,5,5}
 };
 double pheromone[2][STEP]={0}; //各ステップのフェロモン量
 int mstep[NOA][STEP]={0};      //蟻が歩いた過程
 int i;				//繰り返し回数の制御

 srand(SEED);

 for(i=0;i<ILIMIT;++i){
    /*フェロモンの状態出力*/
    printf("%d:\n",i); 
    printp(pheromone);
    /*蟻を歩かせる*/
    walk(cost,pheromone,mstep);
    /*フェロモンの更新*/
    update(cost,pheromone,mstep);
 }
 /*フェロモンの状態出力*/
 printf("%d:\n",i); 
 printp(pheromone);

 return 0;
}

/****************************************************************/
/*フェロモンの更新*/
void update(int cost[2][STEP],double pheromone[2][STEP],int mstep[NOA][STEP]){
 int m;   	  //蟻の個体番号
 int lm;	  //蟻の歩いた距離
 double sum_lm=0; //蟻の歩いた距離の合計

 /*フェロモンの蒸発*/
 for(int i=0;i<2;++i){
    for(int j=0;j<STEP;++j){
	pheromone[i][j]*=RHO; //すべてを0.8倍に薄めている
    }
 }

 /*蟻による上塗り*/
 for(int m=0;m<NOA;++m){
    /*個体mの移動距離lmの計算*/
    lm=0;
    for(int i=0;i<STEP;++i){
	lm+=cost[mstep[m][i]][i];
    }
    /*フェロモンの上塗り*/
    for(int i=0;i<STEP;++i){
	pheromone[mstep[m][i]][i]+=Q*(1.0/lm);
    }
    sum_lm+=lm;
 }
 printf("Average Distance=%lf\n\n",sum_lm/NOA); //蟻の歩いた平均距離を出力
}

/*蟻を歩かせる*/
void walk(int cost[2][STEP],double pheromone[2][STEP],int mstep[NOA][STEP]){
 int m; //蟻の個体番号
 int s; //蟻の現在ステップ位置

 for(m=0;m<NOA;++m){
    for(s=0;s<STEP;++s){
	/*ε-greedyによる行動選択*/
	if((rand1()<EPSILON)||(abs(pheromone[0][s]-pheromone[1][s])<1e-9)){
	    mstep[m][s]=rand01(); //ランダムに行動
	}
	else{ //濃度が高い方を選択
	    if(pheromone[0][s]>pheromone[1][s])mstep[m][s]=0;
	    else mstep[m][s]=1; 
	}
    }
 } 
 printmstep(mstep);//蟻の挙動の出力
}

/*蟻の挙動の表示*/
void printmstep(int mstep[NOA][STEP]){
 printf("*mstep\n");
 for(int i=0;i<NOA;++i){
    for(int j=0;j<STEP;++j){
	printf("%d",mstep[i][j]);
    }
    printf("\n");
 }
}

/*フェロモンの表示*/
void printp(double pheromone[2][STEP]){
 for(int i=0;i<2;++i){
    for(int j=0;j<STEP;++j){
	printf("%4.2lf ",pheromone[i][j]);
    }
    printf("\n");
 }
}

/*乱数生成*/
double rand1(){
 return (double)rand()/RAND_MAX;
}

int rand01(){
 int rnd;
 while((rnd=rand())==RAND_MAX);
 return (int)((double)rnd/RAND_MAX*2);
}
