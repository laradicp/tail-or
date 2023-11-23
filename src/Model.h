#ifndef MODEL_H
#define MODEL_H

#include <iostream>
#include <string>
#include <vector>
#include <ilcplex/ilocplex.h>
#include "Data.h"

using namespace std;

class Model
{
    private:

        IloEnv env;
        IloModel model;
        IloNumVarArray x;
        IloArray<IloNumVarArray> y;
        // IloNumVar z;

        Data data;
        
    public:
    
        Model(string filename);
        
        void solve();
};

#endif
