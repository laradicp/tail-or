#ifndef DATA_H
#define DATA_H

#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Data
{
    private:

        int nbFacilities;
        int nbRegions;
        int nbBeds;

        vector<int> lbBeds; // vector of lower bounds of beds of each facility
        vector<int> ubBeds; // vector of upper bounds of beds of each facility

        vector<int> demand; // vector of demands of each region

        vector<vector<int>> distance; // matrix of distances between facilities and regions
        
    public:

        Data(){};

        Data(string filename);

        int getNbFacilities();
        int getNbRegions();
        int getNbBeds();

        int getLbBeds(int i);
        int getUbBeds(int i);

        int getDemand(int j);

        int getDistance(int i, int j);
        
};

#endif
