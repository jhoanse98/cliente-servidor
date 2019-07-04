#include<iostream>
#include<stdlib.h>
#include<thread>
#include<ctime>
#include<vector>


//g++ -std=c++11 -o matrices matrices.cc -lpthread && ./matrices
/*
terminate called after throwing an instance of 'std::system_error'
  what():  Resource temporarily unavailable
Abortado (`core' generado) 
sucede cuando tamaño mayor a 100
*/

using namespace std;

vector<int> llenavector(int tam){
    vector<int> vectorlleno;
    int totalSize =tam*tam;
    for(int i=0; i<totalSize; i++){
        vectorlleno.push_back(rand()%9);
    }
    return vectorlleno;
}


void muestramatrixvector(vector<int> const& A){
    for(auto& n: A){
        cout<<n<<" ";
    }
    cout<<endl;
}

int multiplica(vector<int> A, vector<int> B, vector<int>& C, int tam, int fila){
    int pos=0;
    int pos2=0;
    for(int k=0; k<tam; k++){
        for (int i=0; i<tam; i++){
            pos=k+tam*i;
            pos2=fila*tam+i;
            C[fila*tam+k]+=A[pos2]*B[pos];
        }
    }       
}


void multiplicamatriz(vector<int> A, vector<int> B, vector<int>& C, int tam){
    for(int fila=0; fila<tam; fila++){
        multiplica(A, B, ref(C), tam, fila);
    }    
}



void multiplicamatrixvectorhilos(vector<int> A, vector<int> B, vector<int>& C, int tam, int idthread, int totalthreads){
    int inicio = (tam*idthread)/totalthreads;
    int finaliza = (tam*(idthread+1))/totalthreads; 
    for(int filas=inicio; filas<finaliza; filas++){
        multiplica(A, B, ref(C), tam, filas);
    }    
}





int main(int argc, char *argv[]){
    int tam=0;
    int Nthreads=0;
    if (argc==3){

	    tam= atoi(argv[1]);
        Nthreads=atoi(argv[2]);
		vector<int> A = llenavector(tam);
        vector<int> B = llenavector(tam);
        vector<thread> hilos;

        vector<int> C(tam*tam,0);
        vector<int> D(tam*tam,0);
        
        //clock_t begin=clock(); 
        //multiplicamatriz(A,B,ref(C),tam);
        //clock_t end=clock();
        //double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
        //cout<<"tiempo transcurrido fue : "<<elapsed_secs<<endl;
        //muestramatrixvector(C);
        //cout<<endl;
        std::chrono::time_point<std::chrono::system_clock> start, end;

        start= std::chrono::system_clock::now();
        multiplicamatriz(A,B,ref(C),tam);
        end= std::chrono::system_clock::now();
        double time1= std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
        //muestramatrixvector(C);
        start = std::chrono::system_clock::now();
        //begin=clock();
        for(int i=0; i<Nthreads;i++){
            hilos.push_back(thread(multiplicamatrixvectorhilos, ref(A),ref(B), ref(D), tam, i, Nthreads));
        }
        //multiplicamatrixvectorhilos(ref(A),ref(B),ref(D),tam);
        for(auto& it : hilos){
            it.join();
        }
        end = std::chrono::system_clock::now();
        double time2 = std::chrono::duration_cast<std::chrono::milliseconds> (end-start).count();

        //end=clock();
        //elapsed_secs=double(end-begin)/CLOCKS_PER_SEC;
        cout<<tam<<", "<<time1<<", "<<time2<<", "<<Nthreads<<endl;
        //muestramatrixvector(D);
        //cout<<"hola";
    }
    else{
        cout<<"Falta el tamaño de la matriz"<<endl;
        return 0;   
    }

}