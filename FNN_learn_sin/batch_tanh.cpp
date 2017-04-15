#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

#define Input_size 20 //訓練データ数
#define eta 0.005        //学習係数
#define No 300000         //学習回数
#define test_size 100 //学習結果を出す時のプロット数
#define input_x "INPUT_x.csv"
#define input_y "INPUT_y.csv"
#define output_x "OUTPUT_x.csv"
#define output_y "OUTPUT_y.csv"
#define error_file "ERROR.csv"

/*ニューロン数*/
#define Input_dim 1  
#define Hidden_dim 12
#define Output_dim 1

int Teacher();
void Init();
void FP();
void GetError(int input);
void BP(int input);
void UpdateParameter();
int Test();

double error=0; //二乗和誤差
double dk_oh[Output_dim][Hidden_dim+1]={0};    //勾配(中間と出力層の間)
double dk_oh_sum[Output_dim][Hidden_dim+1]={0};
double dk_hi[Hidden_dim+1][Input_dim+1]={0}; //勾配(入力と中間層の間)
double dk_hi_sum[Hidden_dim+1][Input_dim+1]={0};

/*教師データ*/
double x[Input_size][Input_dim]={0};
double y[Input_size][Output_dim]={0};

/*入力、中間、出力層のニューロンの値(+1はバイアス分)*/
double I[Input_dim+1]={0};
double H[Hidden_dim+1]={0};
double O[Output_dim]={0};

/*入力と中間、中間と出力の重み*/
double W_hi[Hidden_dim+1][Input_dim+1]={0};
double W_oh[Output_dim][Hidden_dim+1]={0};

int main(){
  int i,j,k;
  FILE *fp2;
  fp2=fopen(error_file,"w");
  if(fp2==NULL){
    printf("ファイルを開けません\n");
    return -1;
  }
  
  Teacher();
  Init();
  for(i=0;i<No;i++){
    error=0;
    for(j=0;j<Input_size;j++){
      /*入力層のニューロンに初期状態xを入力*/
      for(k=0;k<Input_dim;k++){
	I[k+1]=x[j][k];
      }
      FP();
      GetError(j);
      BP(j);
    }
    UpdateParameter();
    fprintf(fp2,"%f\n",error);
    printf("Error:%f\n",error); //エラー表示
  }
  fclose(fp2);
  Test();
  return 0;
}



int Teacher(){	//教師データを変数に格納
  	FILE *fp;
	int i, j;
       
	fp=fopen(input_x,"r");
	if(fp==NULL){
	  printf("ファイルが開けません\n");
	  return -1;
	}
	for (i = 0; i < Input_size; i++){
		for (j = 0; j < Input_dim; j++){
			fscanf(fp, "%lf ", &x[i][j]);
		}
	}
	fclose(fp);
       
	fp=fopen(input_y,"r");
	if(fp==NULL){
	  printf("ファイルが開けません\n");
	  return -1;
	}
	for (i = 0; i < Input_size; i++){
	  for(j=0;j<Output_dim;j++){
		fscanf(fp, "%lf ", &y[i][j]);
	  }
	}
	fclose(fp);
}

void Init(){  //変数の初期化をする。
  int i,j;
  
  /*バイアス*/
  I[0]=1;
  H[0]=1;

  /*重みの初期化*/
  for(i=0;i<Hidden_dim;i++){
    for(j=0;j<Input_dim+1;j++){
      W_hi[i][j]=2.0*rand()/(double)RAND_MAX-1.0;
    }
  }
  for(i=0;i<Output_dim;i++){
    for(j=0;j<Hidden_dim+1;j++){
      W_oh[i][j]=2.0*rand()/(double)RAND_MAX-1.0;
    }
  }
}

void FP(){ //前向き計算
  int i,j;
  double temp;
  
  /*中間層のニューロンの計算*/
  for(i=0;i<Hidden_dim;i++){
    temp=0;
    for(j=0;j<Input_dim+1;j++){
      temp+=I[j]*W_hi[i][j];  //中間層の内部状態
    }
    H[i+1]=tanh(temp);     //活性化
  }

  /*出力層のニューロンの計算*/
  for(i=0;i<Output_dim;i++){
    temp=0;
    for(j=0;j<Hidden_dim+1;j++){
      temp+=H[j]*W_oh[i][j];  //出力層の内部状態
    }
    O[i]=tanh(temp);        //活性化
  }
}

void GetError(int input){ //二乗和誤差を計算する。
  int i;
  for(i=0;i<Output_dim;i++){
    error+=0.5*(y[input][i]-O[i])*(y[input][i]-O[i]);
    }
}

void BP(int input){
  int i,j,k;
  for(j=0;j<Hidden_dim+1;j++){
   for(i=0;i<Output_dim;i++){
     dk_oh[i][j]=-(y[input][i]-O[i])*(1.0-O[i]*O[i])*H[j]; //チェーンルールを用いて勾配計算
     dk_oh_sum[i][j]+=dk_oh[i][j];
   }
  }
  for(k=0;k<Input_dim+1;k++){
   for(i=0;i<Hidden_dim+1;i++){
     for(j=0;j<Output_dim;j++){
       dk_hi[i][k]=dk_oh[j][i]*W_oh[j][i]*(1.0-H[i]*H[i])*I[k];
       dk_hi_sum[i][k]+=dk_hi[i][k];
     }
   }
  }
}

void UpdateParameter(){
  int i,j;
  for(i=0;i<Output_dim;i++){
    for(j=0;j<Hidden_dim+1;j++){
      dk_oh[i][j]=dk_oh_sum[i][j]/(double)Input_size; //平均化する
      W_oh[i][j]-=eta*dk_oh[i][j]; //重み(出力と中間の間)の更新
      dk_oh_sum[i][j]=0;
    }
  }
    
  for(i=0;i<Hidden_dim+1;i++){
    for(j=0;j<Input_dim+1;j++){
      dk_hi[i][j]=dk_hi_sum[i][j]/(double)Input_size;
      W_hi[i][j]-=eta*dk_hi[i][j];
      dk_hi_sum[i][j]=0;
    }
  }
}

int Test(){ //学習結果
  int i,j,k;
  double p;
  double test[test_size][Input_dim];
  FILE *fp;
  
  /*初期状態の最大と最小値を探す*/
  double max[Input_dim]={0}; //初期状態ｘの最大値
  double min[Input_dim]={0}; //最小値
  for (i = 0; i < Input_dim; i++){	//maxとminの初期化
		max[i] = x[0][i];
		min[i] = x[0][i];
	}

   for (i = 0; i < Input_size; i++){
	for (j = 0; j < Input_dim; j++){
		if (max[j] < x[i][j]){
			max[j] = x[i][j];
		 }
		 if (min[j] > x[i][j]){
			min[j] = x[i][j];
		 }
        }
   }

   //初期状態を作る
   for (i = 0; i < Input_dim; i++){
	j = 0;
	for (p = min[0]; p <= max[0]; p += (max[0] - min[0]) / test_size){
	       test[j][i] = p;
	       j++;
	}
   }

   fp=fopen(output_y,"w");
  if(fp==NULL){
      printf("ファイルが開けません\n");
      return -1;
   }
 
   //Forward Propagationする
   for(i=0;i<test_size;i++){
     for(j=0;j<Input_dim;j++){
       I[j+1]=test[i][j];
     }
    FP();
     
   //csvに結果を保存
   for(k=0;k<Output_dim;k++){
     fprintf(fp,"%f,",O[k]);
   }
   fprintf(fp,"\n");
     
   }  //FPここまで
      
   fclose(fp);
  
   fp=fopen(output_x,"w");
   if(fp==NULL){
       printf("ファイルが開けません\n");
       return -1;
   }
  
   for(i=0;i<test_size;i++){
       for(j=0;j<Input_dim;j++){
	 fprintf(fp,"%f,",test[i][j]);
        }
	fprintf(fp,"\n");
        }
  
  fclose(fp);
}

