# define knob, retrieve url, expect json value
# knob:<uri>:<value>:<event>:...
# as many value,event pairs may follow (up to ?)
# value * means to send this event always
#

timer test_timer {
    interval: 2s
    event: test_timer_event
}

process demo_add {
    trigger: op1_value, op2_value
    script: {
        sum := op1_value + op2_value
        emit sum_value(sum)
    }
}

process gen_op1 {
    trigger: test_timer_event
    script: {
        emit op1_value(2)
    }
}

process gen_op2 {
    trigger: test_timer_event
    script: {
        emit op2_value(3)
    }
}

