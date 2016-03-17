#include <string>
#include "Api.h"

using namespace std;

int main()
{
    Thermo2Api api = Thermo2Api();

    Thermo2Event *event = api.Get("sum_value");
    
    return 0;
}
