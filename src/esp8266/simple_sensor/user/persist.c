#include "os_type.h"
#include "persist.h"

#define USER_DATA_OFFSET 256

static persist_type data = { 0 };
static bool dirty = false;

void ICACHE_FLASH_ATTR
persist_init()
{
    data.sensor_value = false;
    data.poll_counter = 0;
    dirty = false;
}

inline persist_type *
persist_data_ptr()
{
    return &data;
}

void ICACHE_FLASH_ATTR
persist_dirty()
{
    dirty = true;
}

bool ICACHE_FLASH_ATTR
persist_load()
{
    bool rv = false;

    rv = system_rtc_mem_read(USER_DATA_OFFSET/4, &data, sizeof(data));

    dirty = false;

    return rv;
}

bool ICACHE_FLASH_ATTR
persist_save()
{
    bool rv = false;

    if(dirty) {
        rv = system_rtc_mem_write(USER_DATA_OFFSET/4, &data, sizeof(data));
        if(rv) dirty = false;
    } else {
        rv = true;
    }

    return rv;
}
