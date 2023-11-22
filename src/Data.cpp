#include "Data.h"
#include <fstream>

Data::Data(string filename)
{
    // Read data from file
    ifstream file(filename);

    if (file.is_open())
    {
        file >> n >> m;

        k.resize(n);
        d.resize(m);
        t.resize(n);

        for (int i = 0; i < n; i++)
        {
            file >> k[i];
        }

        for (int i = 0; i < m; i++)
        {
            file >> d[i];
        }

        for (int i = 0; i < n; i++)
        {
            t[i].resize(m);

            for (int j = 0; j < m; j++)
            {
                file >> t[i][j];
            }
        }
    }
    else
    {
        cout << "Error opening file" << endl;
    }
}

int Data::getN()
{
    return n;
}

int Data::getM()
{
    return m;
}

int Data::getK(int i)
{
    return k[i];
}

int Data::getD(int i)
{
    return d[i];
}

double Data::getT(int i, int j)
{
    return t[i][j];
}
