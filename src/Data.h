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

        vector<pair<double, double>> facilityCoordinates; // vector of coordinates of each facility
        vector<pair<double, double>> regionCoordinates; // vector of coordinates of each region
        vector<vector<double>> distance; // matrix of distances between facilities and regions
        
    public:

        Data(string filename);

        int getNbFacilities();
        int getNbRegions();
        int getNbBeds();

        int getLbBeds(int i);
        int getUbBeds(int i);

        int getDemand(int j);

        double getDistance(int i, int j);
        
};

#endif
