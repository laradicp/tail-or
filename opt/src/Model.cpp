#include "Model.h"

Model::Model(string filename)
{
    data = Data(filename);
    
    env = IloEnv();
    model = IloModel(env);
    
    // Xi corresponds to how many beds are allocated to facility i
    x = IloNumVarArray(env, data.getNbFacilities(), 0, data.getNbBeds(), ILOINT);
    
    // add variable x to the model
    for(int i = 0; i < data.getNbFacilities(); i++)
    {
        x[i].setBounds(data.getLbBeds(i), data.getUbBeds(i));
        char name[100];
        sprintf(name, "X(%d)", i);
        x[i].setName(name);
        model.add(x[i]);
    }
    
    // Yij corresponds to the number of customers in j that are assigned to facility i
    y = IloArray<IloNumVarArray>(env, data.getNbFacilities());

    // add variable y to the model
    for(int i = 0; i < data.getNbFacilities(); i++)
    {
        y[i] = IloNumVarArray(env, data.getNbRegions(), 0, data.getDemand(i), ILOINT);
        for(int j = 0; j < data.getNbRegions(); j++)
        {
            char name[100];
            sprintf(name, "Y(%d)(%d)", i, j);
            y[i][j].setName(name);
            model.add(y[i][j]);
        }
    }

    // // Z is the maximum value of distance*y
    // z = IloNumVar(env, 0, IloInfinity, ILOFLOAT);

    // // add objective function
    // IloExpr obj(env);
    // model.add(IloMinimize(env, z));

    // // add constraints
    // // define z
    // for(int i = 0; i < data.getNbFacilities(); i++)
    // {
    //     for(int j = 0; j < data.getNbRegions(); j++)
    //     {
    //         IloRange r = (z - data.getDistance(i, j)*y[i][j] >= 0);
    //         char name[100];
    //         sprintf(name, "Maximum distance(%d)(%d)", i, j);
    //         r.setName(name);
    //         model.add(r);
    //     }
    // }

    // add objective function
    IloExpr obj(env);
    for(int i = 0; i < data.getNbFacilities(); i++)
    {
        for(int j = 0; j < data.getNbRegions(); j++)
        {
            obj += data.getDistance(i, j)*y[i][j];
        }
    }
    model.add(IloMinimize(env, obj));

    // respect total number of beds
    IloExpr sumX(env);
    for(int i = 0; i < data.getNbFacilities(); i++)
    {
        sumX += x[i];
    }
    IloRange r = (sumX == data.getNbBeds());
    r.setName("Total number of beds");
    model.add(r);

    // respect capacity
    for(int i = 0; i < data.getNbFacilities(); i++)
    {
        IloExpr sumY(env);
        for(int j = 0; j < data.getNbRegions(); j++)
        {
            sumY += y[i][j];
        }

        IloRange r = (sumY - x[i] <= 0);
        char name[100];
        sprintf(name, "Capacity(%d)", i);
        r.setName(name);
        model.add(r);
    }

    // respect demand
    for(int j = 0; j < data.getNbRegions(); j++)
    {
        IloExpr sumY(env);
        for(int i = 0; i < data.getNbFacilities(); i++)
        {
            sumY += y[i][j];
        }

        IloRange r = (sumY == data.getDemand(j));
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
            // int nbVulnerableCustomers = 0;
            // for(int i = 0; i < data.getNbFacilities(); i++)
            // {
            //     for(int j = 0; j < data.getNbRegions(); j++)
            //     {
            //         if(data.getDistance(i, j)*cplex.getValue(y[i][j]) + 0.05 >= cplex.getObjValue())
            //         {
            //             cout << "Maximum distance: " << data.getDistance(i, j) << endl;
            //             cout << "Demand: " << cplex.getValue(y[i][j]) << endl;
            //             nbVulnerableCustomers += cplex.getValue(y[i][j]);
            //         }
                        
            //     }
            // }
            // cout << "Number of vulnerable customers: " << nbVulnerableCustomers << endl;
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
