#ifndef MODEL_H
#define MODEL_H

#include <iostream>
#include <string>
#include <vector>
#include <ilcplex/ilocplex.h>

using namespace std;

class Model
{
    private:

        IloEnv env;
        IloModel model;
        IloNumVarArray x;
        IloArray<IloNumVarArray> y;
        
    public:
    
        Model(string filename);
        
        void solve();
};

#endif
