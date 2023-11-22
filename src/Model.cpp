#include "Model.h"
#include "Data.h"

Model::Model(string filename)
{
    Data data = Data(filename);
    
    env = IloEnv();
    model = IloModel(env);
    
    // let Xi assume value 1 if facility i is selected, otherwise
    x = IloBoolVarArray(env, data.getN());
    
    // add variable x to the model
    for(int i = 0; i < data.getN(); i++)
    {
        char name[100];
        sprintf(name, "X(%d)", i);
        x[i].setName(name);
        model.add(x[i]);
    }
    
    // Yij corresponds to the fraction of demand of customer j that is satisfied by facility i
    y = IloArray<IloNumVarArray>(env, data.getN());

    // add variable y to the model
    for(int i = 0; i < data.getN(); i++)
    {
        y[i] = IloNumVarArray(env, data.getM(), 0, 1, ILOFLOAT);
        for(int j = 0; j < data.getM(); j++)
        {
            char name[100];
            sprintf(name, "Y(%d)(%d)", i, j);
            y[i][j].setName(name);
            model.add(y[i][j]);
        }
    }

    // add objective function
    IloExpr obj(env);
    for(int i = 0; i < data.getN(); i++)
    {
        for(int j = 0; j < data.getM(); j++)
        {
            obj += data.getT(i, j)*y[i][j]*data.getD(j);
        }
    }
    model.add(IloMinimize(env, obj));

    // add constraints
    // respect capacity
    for(int i = 0; i < data.getN(); i++)
    {
        IloExpr sumY(env);
        for(int j = 0; j < data.getM(); j++)
        {
            sumY += y[i][j]*data.getD(j);
        }

        IloRange r = (sumY <= data.getK(i)*x[i]);
        char name[100];
        sprintf(name, "Capacity(%d)", i);
        r.setName(name);
        model.add(r);
    }

    // respect demand
    for(int j = 0; j < data.getM(); j++)
    {
        IloExpr sumY(env);
        for(int i = 0; i < data.getN(); i++)
        {
            sumY += y[i][j];
        }

        IloRange r = (sumY == 1);
        char name[100];
        sprintf(name, "Demand(%d)", j);
        r.setName(name);
        model.add(r);
    }
}

void Model::solve()
{
    IloCplex cplex(model);
    cplex.setParam(IloCplex::TiLim, 3600);
    cplex.setParam(IloCplex::Threads, 1);

    cplex.exportModel("model.lp");

    try
    {
        if(cplex.solve())
        {
            cout << "Solution status: " << cplex.getStatus() << endl;
            cout << "Objective value: " << cplex.getObjValue() << endl;
        }
        else
        {
            cout << "Solution status: " << cplex.getStatus() << endl;
        }
    }
    catch(IloException& e)
    {
        cout << e;
    }
}
