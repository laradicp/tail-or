#ifndef DATA_H
#define DATA_H

#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Data
{
    private:

        int n; // number of facilities / candidate cities for receiving hospital beds
        int m; // number of customers / cities

        vector<int> k; // vector of capacities of each facility / number of hospital beds increased
        vector<int> d; // vector of demands of each customer / percentage of city population

        vector<vector<double>> t; // matrix of distances between facilities and customers / cities
        
    public:

        Data(string filename);

        int getN();
        int getM();

        int getK(int i);
        int getD(int i);

        double getT(int i, int j);
        
};

#endif
