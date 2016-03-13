using System;

namespace Thermo2
{
    enum ValueTypes { IntValue, StringValue, FloatValue };

    public class Value
    {
        ValueTypes Type;
        int int_value;
        float float_value;
        string string_value;

        public Value(int value)
        {
            Type = ValueTypes.IntValue;
            int_value = value;
        }

        public Value(float value)
        {
            Type = ValueTypes.FloatValue;
            float_value = value;
        }

        public Value(string value)
        {
            Type = ValueTypes.StringValue;
            string_value = value;
        }
    }

    public class Api
    {
        private string Host;
        private int Port;

        public Api(string Host, int Port)
        {
            this.Host = Host;
            this.Port = Port;
        }

        public Api()
        {
            Host = "127.0.0.1";
            Port = 8822;
        }

        public Value Get(string label)
        {
            return null;
        }

        public void Set(string label, float value, float t)
        {

        }
    }
}
