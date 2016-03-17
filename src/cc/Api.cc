#include <string>
#include "Api.h"

using namespace std;

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

Thermo2Event *Thermo2Api::Get(string label)
{
    return NULL;
}

void Thermo2Api::Set(string label, string value, float t)
{
    return;
}