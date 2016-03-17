#include <string>
#include <iostream>
#include "Api.h"

using namespace std;

int main()
{
    Thermo2Api api = Thermo2Api();

    Thermo2Event *event = nullptr;

    try {
        event = api.Get("sum_value");
    } catch(const char *e) {
        cout << "error: " << e << endl;
        return -1;
    } catch(...) {
        cout << "default exception" << endl;
        return -1;
    }

    cout.precision(7);

    cout << event->label << ":" << event->value << ":" << event->t << endl;

    delete event;
    
    return 0;
}
