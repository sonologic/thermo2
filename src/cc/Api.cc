#include <string>
#include <iostream>
#include <cpr/cpr.h>
#include "json/src/json.hpp"
#include "Api.h"

using namespace std;
using json = nlohmann::json;

void Thermo2Api::InitUrl(void)
{
    this->url = "http://"+this->host+":"+to_string(this->port);
}

Thermo2Api::Thermo2Api()
{
    this->host = "127.0.0.1";
    this->port = 8822;
    this->InitUrl();
}

Thermo2Api::Thermo2Api(string host, int port)
{
    this->host = host;
    this->port = port;
    this->InitUrl();
}

Thermo2Event *Thermo2Api::Get(const string label)
{
    auto r = cpr::Get(cpr::Url{this->url + "/get/" + label});

    cout << r.status_code << endl;
    cout << r.header["Content-Type"] << endl;
    cout << r.text << endl;

    auto data = json::parse(r.text);

    cout << data["labell"] << endl;

    auto r_label = data["label"];

    if(json::value_t::null==r_label.type()) throw "invalid response, no label";

    auto r_value = data["value"];
    auto r_t = data["t"];

    cout << "label type: " << r_label.type() << endl;
    cout << "value type: " << r_value.type() << endl;
    cout << "value: " << r_value.get<int>() << endl;
    cout << "t type: " << r_t.type() << endl;


    long double t = 0.0;

    if(json::value_t::number_float!=r_t.type()) throw "invalid response, t is not float";

    t = r_t.get<long double>();

    cout.precision(7);
    cout << "t=" << t << endl;

    Thermo2Event* event =  new Thermo2Event;

    event->label = r_label.get<string>();

    if(json::value_t::number_integer==r_value.type()) {
        event->value = to_string(r_value.get<int>());
    } else if(json::value_t::number_unsigned==r_value.type()) {
        event->value = to_string(r_value.get<int>());
    } else if(json::value_t::number_float==r_value.type()) {
        event->value = to_string(r_value.get<float>());
    } else if(json::value_t::string==r_value.type()) {
        event->value = r_value.get<string>();
    } else {
        throw "invalid response, unsupported json type for value";
    }

    event->t = t;

    return event;
}

void Thermo2Api::Set(string label, string value, float t)
{
    return;
}
