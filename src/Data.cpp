#include "Data.h"
#include <fstream>
#include <math.h>

Data::Data(string filename)
{
    // Read data from file
    ifstream file(filename);

    if (file.is_open())
    {
        file >> nbFacilities;
        file >> nbRegions;
        file >> nbBeds;

        lbBeds.resize(nbFacilities);
        ubBeds.resize(nbFacilities);
        
        for (int i = 0; i < nbFacilities; i++)
        {
            file >> lbBeds[i];
            file >> ubBeds[i];
        }

        demand.resize(nbRegions);

        for (int j = 0; j < nbRegions; j++)
        {
            file >> demand[j];
        }

        distance.resize(nbFacilities);

        for (int i = 0; i < nbFacilities; i++)
        {
            distance[i].resize(nbRegions);
            for (int j = 0; j < nbRegions; j++)
            {
                file >> distance[i][j];
            }
        }

        file.close();   
    }
    else
    {
        cout << "Error opening file" << endl;
    }
}

int Data::getNbFacilities()
{
    return nbFacilities;
}

int Data::getNbRegions()
{
    return nbRegions;
}

int Data::getNbBeds()
{
    return nbBeds;
}

int Data::getLbBeds(int i)
{
    return lbBeds[i];
}

int Data::getUbBeds(int i)
{
    return ubBeds[i];
}

int Data::getDemand(int j)
{
    return demand[j];
}

int Data::getDistance(int i, int j)
{
    return distance[i][j];
}
