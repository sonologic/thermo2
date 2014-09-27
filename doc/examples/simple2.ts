# define knob, retrieve url, expect json value
# knob:<uri>:<value>:<event>:...
# as many value,event pairs may follow (up to ?)
# value * means to send this event always
#

timer test_timer {
    interval: 10s
    event: test_timer_event
}

sensor temp1 {
    interval: 10s
    uri: 1wire://0012003a.../temp
    type: float
}

sensor knob {
    interval: 30s
    uri: http://uihost.dmz/thermo2/setting
    type: float
}

process demo_add {
    trigger: op1_value, op2_value
    script: {
        sum := op1_value + op2_value
        emit sum_value(sum)
    }
}

process simple {
    trigger: setting_value, sensor_value
    script: {
        if setting_value > sensor_value then
            emit heating_on
        endif
        if setting_value < sensor_value then
            emit heating_off
        endif
    }
}

process simple2 {
    trigger: setting_value, sensor_value
    script: {
        error := 0.1
        if sensor_value + error < setting_value then
            emit heating_on
        endif
        if sensor_value - error > setting_value then
            emit heating_off
        endif
    }
}

