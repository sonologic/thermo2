# define knob, retrieve url, expect json value
# knob:<uri>:<value>:<event>:...
# as many value,event pairs may follow (up to ?)
# value * means to send this event always
#
knob:http://uihost.dmz/thermo2/setting:*:setting_value

sensor:1wire://0012003a.../temp:*:sensor_value

# cmp(value_event1,value_event2):cond:event
cmp(setting_value,sensor_value):gt:heating_on
cmp(setting_value,sensor_value):lt:heating_off


