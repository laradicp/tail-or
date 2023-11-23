#include "Model.h"
#include <vector>

using namespace std;

int main(int argc, char** argv)
{
    if(argc != 2)
    {
        cout << "Correct usage: ./opt.bin <path>" << endl;
        exit(1);
    }

    Model model(argv[1]);
    model.solve();

    return 0;
}
