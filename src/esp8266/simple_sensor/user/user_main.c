#include "ets_sys.h"
#include "osapi.h"
#include "gpio.h"
#include "os_type.h"
#include "user_config.h"
#include "user_interface.h"
#include "httpclient.h"
#include "persist.h"

#ifdef DEBUG
#define PRINTF(...) os_printf(__VA_ARGS__)
#else
#define PRINTF(...)
#endif

// states
typedef enum {
    STATE_LOAD_PERSIST,
    STATE_INIT_PERSIST,
    STATE_HF_READ,
    STATE_HF_WIFI_CONNECT,
    STATE_HF_WIFI_WAIT,
    STATE_HF_SEND,
    STATE_HF_SEND_WAIT,
    STATE_LF_READ,
    STATE_LF_WIFI_CONNECT,
    STATE_LF_WIFI_WAIT,
    STATE_LF_SEND,
    STATE_LF_SEND_WAIT,
    STATE_IDLE,
} state_type;

#define user_procTaskPrio        0
#define user_procTaskQueueLen    1
os_event_t    user_procTaskQueue[user_procTaskQueueLen];
static void timer_fn(void *timer_data);
static void wifi_connect(void);


static os_timer_t timer;
static state_type state = STATE_IDLE;
static int timeout = 0;
/*
static void ICACHE_FLASH_ATTR
delay_ms(int i)
{
    int j;

    for(j=0;j<i;j++) {
        os_delay_us(1000);
    }
}*/

static void ICACHE_FLASH_ATTR my_http_callback(char * response_body, int http_status, char * response_headers, int body_size)
{
    os_printf("http_status=%d\n", http_status);
    if (!HTTP_STATUS_IS_ERROR(http_status)) {
        os_printf("strlen(headers)=%d\n", strlen(response_headers));
        os_printf("body_size=%d\n", body_size);
        os_printf("body=%s<EOF>\n", response_body); // FIXME: this does not handle binary data.
    }
    state = 0;
}


static void ICACHE_FLASH_ATTR
timer_fn(void *timer_data)
{
    uint32_t delay = MAX_LOOP_TIMER_MS;

    os_timer_disarm(&timer);

    PRINTF("state: %d\n\r", state);
    switch(state) { 
        case STATE_LOAD_PERSIST:
            if(persist_load()) {
                state = STATE_HF_READ;
                persist_data_ptr()->poll_counter += 1;

                if(persist_data_ptr()->poll_counter >= 10) {
                    // read low-frequency sensor (temp etc)
                    persist_data_ptr()->poll_counter = 0;
                }
                persist_dirty();
            } else {
                PRINTF("err loading persist\r\n");
                // todo: goto error state (blink led?)
                state = STATE_IDLE;
            }
            delay = MIN_LOOP_TIMER_MS;
            break;
        case STATE_INIT_PERSIST:
            persist_init();
            state = STATE_HF_READ;
            delay = MIN_LOOP_TIMER_MS;
            break;
        case STATE_HF_READ:
            state = STATE_LF_READ;
            if(GPIO_INPUT_GET(GPIO_SWITCH)) {
                if(!(persist_data_ptr()->sensor_value)) {
                    persist_data_ptr()->sensor_value = true;
                    persist_dirty();
                    state = STATE_HF_WIFI_CONNECT;
                }
            } else {
                if(persist_data_ptr()->sensor_value) {
                    persist_data_ptr()->sensor_value = false;
                    persist_dirty();
                    state = STATE_HF_WIFI_CONNECT;
                }
            }
            break;
        case STATE_HF_WIFI_CONNECT:
            if(wifi_station_get_connect_status()==STATION_GOT_IP) {
                state = STATE_HF_SEND;
            } else {
                wifi_connect();
                state = STATE_HF_WIFI_WAIT;
            }
            break;
        case STATE_HF_WIFI_WAIT:
            if(wifi_station_get_connect_status()==STATION_GOT_IP) {
                state = STATE_HF_SEND;
            }
            break;
        case STATE_HF_SEND:
            state = STATE_HF_SEND_WAIT;
            break;
        case STATE_HF_SEND_WAIT:
            state = STATE_HF_SEND_WAIT;
            break;
        case STATE_LF_READ:
            state = STATE_LF_WIFI_CONNECT;
            break;
        case STATE_LF_WIFI_CONNECT:
            if(wifi_station_get_connect_status()==STATION_GOT_IP) {
                state = STATE_HF_SEND;
            } else {
                wifi_connect();
                state = STATE_HF_WIFI_WAIT;
            }
            break;
        case STATE_LF_WIFI_WAIT:
            if(wifi_station_get_connect_status()==STATION_GOT_IP) {
                state = STATE_LF_SEND;
            }
            break;
        case STATE_LF_SEND:
            state = STATE_LF_SEND_WAIT;
            break;
        case STATE_LF_SEND_WAIT:
            state = STATE_IDLE;
            break;
        case STATE_IDLE:
            // go to deep sleep
            persist_save();
            system_deep_sleep(SLEEP_TIME_US);
            break;
        default:
            // uhoh
            PRINTF("invalid state, reset\n\r");
            state = STATE_IDLE;
            break;
    }
       
    os_timer_setfn(&timer, (os_timer_func_t *)timer_fn, NULL);
    os_timer_arm(&timer, delay, false); 
/*
        case STATE_IDLE:
            http_get("http://10.1.3.161/text", "", my_http_callback);
            state = STATE_HTTP_PENDING;
            timeout = 30;
            break;
        case STATE_HTTP_PENDING:
            timeout--;
            if(timeout==0) {
                PRINTF("timeout!\n\r");
                state=STATE_IDLE;
            } else {
                delay_ms(1000);
            }
            break;
        default:
            PRINTF("invalid state, reset\n\r");
            state=STATE_IDLE;
            break;
    }
    //system_os_post(user_procTaskPrio, 0, 0 ); */
}

static void ICACHE_FLASH_ATTR
wifi_handle_event_cb(System_Event_t *evt)
{
    PRINTF("wifi event    %x\n",  evt->event);

    if(evt->event == EVENT_STAMODE_GOT_IP) {
    }    
}

static void ICACHE_FLASH_ATTR
wifi_connect()
{
    char ssid[32] = SSID;
    char password[64] = SSID_PASSWORD;
    struct station_config stationConf;

    //Set station mode
    wifi_set_opmode( 0x1 );

    //Set ap settings
    os_memcpy(&stationConf.ssid, ssid, 32);
    os_memcpy(&stationConf.password, password, 64);
    wifi_station_set_config(&stationConf);
    wifi_set_event_handler_cb(wifi_handle_event_cb);
    wifi_station_connect();
}

static void ICACHE_FLASH_ATTR
send_heartbeat()
{
    wifi_connect();
}

//Init function 
void ICACHE_FLASH_ATTR
user_init()
{
    struct rst_info *reset_info;

    PRINTF("wake\r\n");

    GPIO_DIS_OUTPUT(1<<GPIO_SWITCH);
    
    reset_info = system_get_rst_info();

    PRINTF("rst reason: %d\r\n", reset_info->reason);

    if(reset_info->reason == REASON_DEEP_SLEEP_AWAKE) {
        state = STATE_LOAD_PERSIST;
    } else {
        state = STATE_INIT_PERSIST;
    }

    os_timer_disarm(&timer);
    os_timer_setfn(&timer, (os_timer_func_t *)timer_fn, NULL);
    os_timer_arm(&timer, MIN_LOOP_TIMER_MS, false);
    
/*

    // read high-frequency sensor
    // compare sensor w/ persistent value
    // if different:
    //   connect to ap
    //   notify server
    //   on success change persistent value
    //   deep sleep
    
    state = STATE_HF_READ;

    //Start os task
    system_os_task(loop, user_procTaskPrio,user_procTaskQueue, user_procTaskQueueLen);

    system_os_post(user_procTaskPrio, 0, 0 ); */
}
