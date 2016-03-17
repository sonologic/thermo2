#ifndef _THERMO2_API_H
#define _THERMO2_API_H

using namespace std;

struct Thermo2Event {
    string label;
    string value;
    float t;
};

class Thermo2Api {
    string          host;
    int             port;
    string          url;
    void            InitUrl(void);
  public:
                    Thermo2Api();
                    Thermo2Api(string, int);
    Thermo2Event   *Get(string label);
    void            Set(string label, string value, float t);
};

#endif // _THERMO2_API_H
