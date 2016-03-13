using System;
using System.Net;
using System.IO;

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

        static public implicit operator Value(int value)
        {
            return new Value(value);
        }

        public Value(float value)
        {
            Type = ValueTypes.FloatValue;
            float_value = value;
        }

        static public implicit operator Value(float value)
        {
            return new Value(value);
        }

        public Value(string value)
        {
            Type = ValueTypes.StringValue;
            string_value = value;
        }

        static public implicit operator Value(string value)
        {
            return new Value(value);
        }

        static public implicit operator string(Value value)
        {
            switch(value.Type) {
                case ValueTypes.IntValue:
                    return value.int_value.ToString();
                case ValueTypes.StringValue:
                    return value.string_value;
                case ValueTypes.FloatValue:
                    return value.float_value.ToString();
                default:
                    return "-";
            }
        }

        public override string ToString()
        {
            return "Value: <type=" + this.Type.ToString() + ">";
        }
    }

    public class Api
    {
        private string Host;
        private int Port;
        private string Url;

        private void InitUrl()
        {
            this.Url = "http://" + this.Host + ":" + this.Port;
        }

        public Api(string Host, int Port)
        {
            this.Host = Host;
            this.Port = Port;

            this.InitUrl();
        }

        public Api()
        {
            this.Host = "127.0.0.1";
            this.Port = 8822;

            this.InitUrl();
        }

        public Value Get(string label)
        {
            WebClient client = new WebClient();

            string response = client.DownloadString(this.Url + "/get/" + label);

            Console.WriteLine(response);           
            return null;
        }

        public void Set(string label, float value, float t)
        {
            
        }
    }
}
