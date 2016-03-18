#include <string>
#include <iostream>
#include <tclap/CmdLine.h>
#include "Api.h"

using namespace std;

int main(int argc, char *argv[])
{
    try {
        TCLAP::CmdLine cmd("Thermo2Cli", ' ', "0.9");

        TCLAP::ValueArg<std::string> getArg("g","get","label of cached event to get",false,"","string");
        TCLAP::ValueArg<std::string> setArg("s","set","label of event to inject (requires --value to be specified)",false,"","string");

        cmd.xorAdd(getArg, setArg);

        TCLAP::ValueArg<std::string> valueArg("v","value","value of event to inject",false,"","string");
        cmd.add(valueArg);

        cmd.parse(argc, argv);

        Thermo2Api api = Thermo2Api();

        Thermo2Event *event = nullptr;

        if(getArg.getValue().length()>0) {
            event = api.Get("sum_value");
            cout.precision(7);
            cout << event->label << ":" << event->value << ":" << event->t << endl;
            delete event;
        } else {
            cout << "--set not yet implemented" << endl;
        }

    } catch (TCLAP::ArgException &e) {
        std::cerr << "error: " << e.error() << " for arg " << e.argId() << std::endl;
    } catch(const char *e) {
        cout << "error: " << e << endl;
        return -1;
    } catch(...) {
        cout << "default exception" << endl;
        return -1;
    }

    return 0;
}
