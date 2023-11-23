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
        facilityCoordinates.resize(nbFacilities);

        for (int i = 0; i < nbFacilities; i++)
        {
            file >> lbBeds[i];
            file >> ubBeds[i];
            file >> facilityCoordinates[i].first;
            file >> facilityCoordinates[i].second;
        }

        demand.resize(nbRegions);
        regionCoordinates.resize(nbRegions);

        for (int j = 0; j < nbRegions; j++)
        {
            file >> demand[j];
            file >> regionCoordinates[j].first;
            file >> regionCoordinates[j].second;
        }

        distance.resize(nbFacilities);

        for (int i = 0; i < nbFacilities; i++)
        {
            distance[i].resize(nbRegions);
            for (int j = 0; j < nbRegions; j++)
            {
                distance[i][j] = sqrt(pow(facilityCoordinates[i].first - regionCoordinates[j].first, 2) + pow(facilityCoordinates[i].second - regionCoordinates[j].second, 2));
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

double Data::getDistance(int i, int j)
{
    return distance[i][j];
}
