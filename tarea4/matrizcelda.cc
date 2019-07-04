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
sucede cuando tamaño mayor a 180
*/


// cat /proc/sys/kernel/threads-max : me dice el numero maximo de hilos (30340)


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

void multiplicacelda(vector<int>  A, vector<int> B, vector<int>& C, int  i, int k, int tam){
    for(int j=0; j<tam; j++){
        C[i*tam+k]+=A[i*tam+j]*B[k+tam*j];
    }
}

void multiplicamatriz(vector<int> A, vector<int> B, vector<int>& C, int tam){
    int contador=0;
    for(int i=0; i<tam; i++){
        for(int k=0; k<tam; k++){
            multiplicacelda(A, B, ref(C), i, k, tam);
        }
    }
}



void multiplicamatrixvectorhilos(vector<int> const& A, vector<int> const& B, vector<int>& C, int tam){
    vector<thread> hilos;
    for(int filas=0; filas<tam; filas++){
        for(int ciclo=0;ciclo<tam; ciclo++){
            hilos.push_back(thread(multiplicacelda,A,B,ref(C),filas,ciclo,tam));
        }
    }    

    for(auto& it : hilos){
        it.join();
        //cout<<"hola"<<endl;
    }
}




int main(int argc, char *argv[]){
    int tam=0;
    if (argc==2){

	    tam= atoi(argv[1]);
		vector<int> A = llenavector(tam);
        vector<int> B = llenavector(tam);
        vector<int> C(tam*tam, 0);
        vector<int> D(tam*tam,0);
        //muestramatrixvector(A);
        //muestramatrixvector(B);
        
        std::chrono::time_point<std::chrono::system_clock> start, end;
        start = std::chrono::system_clock::now();
        multiplicamatriz(A,B,ref(C),tam);
        end = std::chrono::system_clock::now();
        double time = std::chrono::duration_cast<std::chrono::milliseconds> (end-start).count();
        
        //muestramatrixvector(C);

            
        
        start=std::chrono::system_clock::now();
        multiplicamatrixvectorhilos(A,B,D,tam);
        end=std::chrono::system_clock::now();
        double time2 = std::chrono::duration_cast<std::chrono::milliseconds> (end-start).count();        
        cout<<tam<<", "<<time<<", "<<time2<<endl;
        //muestramatrixvector(D);
        
        return 0;
    }
}