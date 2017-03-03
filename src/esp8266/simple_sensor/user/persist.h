#include "ets_sys.h"
#include <stdbool.h>

// data to persist in rtc user memory
typedef struct {
    bool sensor_value;
    uint16 poll_counter;
} persist_type;


void ICACHE_FLASH_ATTR
persist_init();

inline persist_type * 
persist_data_ptr();

void ICACHE_FLASH_ATTR
persist_dirty();

bool ICACHE_FLASH_ATTR
persist_load();

bool ICACHE_FLASH_ATTR
persist_save();

