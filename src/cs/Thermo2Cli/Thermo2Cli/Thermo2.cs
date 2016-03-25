using System;
using System.Net;
using System.IO;
using System.Collections.Specialized;
using Newtonsoft.Json.Linq;
using Thermo2;
using System.Text;

namespace Thermo2
{
    enum ValueTypes { IntValue, StringValue, DecimalValue };

    public class Event
    {
        ValueTypes Type;
        //
        int int_value;
        decimal decimal_value;
        string string_value;
        //
        string label;
        decimal t;


        public Event(string label, int value, decimal t)
        {
            Type = ValueTypes.IntValue;
            int_value = value;
            this.label = label;
            this.t = t;
        }


        public Event(string label, decimal value, decimal t)
        {
            Type = ValueTypes.DecimalValue;
            decimal_value = value;
            this.label = label;
            this.t = t;
        }

        public Event(string label, string value, decimal t)
        {
            Type = ValueTypes.StringValue;
            string_value = value;
            this.label = label;
            this.t = t;
        }

        static public implicit operator string(Event value)
        {
            if(value==null)
                return "null";

            switch(value.Type) {
                case ValueTypes.IntValue:
                    return value.int_value.ToString();
                case ValueTypes.StringValue:
                    return value.string_value;
                case ValueTypes.DecimalValue:
                    return value.decimal_value.ToString("N");
                default:
                    return "-";
            }
        }

        public override string ToString()
        {
            return String.Format(
                    "Event: <type={0}, label={1}, t={2}, value={3}>",
                    this.Type,
                    this.label,
                    this.t.ToString("N3"),
                    (string)this);
        }

        public decimal GetTime()
        {
            return t;
        }

        public string GetLabel()
        {
            return label;
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

        public string GetHost()
        {
            return Host;
        }

        public int GetPort()
        {
            return Port;
        }

        public string GetUrl()
        {
            return Url;
        }

        private Event ParseJsonResponse(string response)
        {
            JObject o = (JObject)JObject.Parse(response);

            var json_label = o.GetValue("label");
            var json_t = o.GetValue("t");
            var json_value = o.GetValue("value");

            if( (json_label==null) || (json_label.Type != JTokenType.String) ) {
                Console.WriteLine("invalid response (no label)");
                return null;
            }

            if( (json_t==null) || (json_t.Type != JTokenType.Float) ) {
                Console.WriteLine("invalid response (no t)");
                return null;
            }
    
            Event v;
    
            if(json_value == null) {
                v = new Event((string)json_label, "", (decimal)json_t);
            } else if(json_value.Type == JTokenType.Integer) { 
                v = new Event((string)json_label, (int)json_value, (decimal)json_t);
            } else if(json_value.Type == JTokenType.Float) {
                v = new Event((string)json_label, (decimal)json_value, (decimal)json_t);
            } else {
                v = new Event((string)json_label, (string)json_value, (decimal)json_t);
            }

            return v;
        }

        // <summary>
        //   Get the cached event value from the thermo2d instance.
        //   <see cref="Event"/>
        // </summary>
        // <param name="label">Label of cached event to get.</param>
        // <returns>Returns an Event instance or null on failure.</returns>
        public Event Get(string label)
        {
            WebClient client = new WebClient();

            try {
                string response = client.DownloadString(this.Url + "/get/" + label);

                Console.WriteLine(response);
                return ParseJsonResponse(response);
            }
            catch (WebException e) {
                Console.WriteLine(e.Message);
                return null;
            }
        }

        // <summary>
        //   Inject an event into the thermo2d instance.
        // </summary>
        // <param name="label">Label of event to inject.</param>
        // <param name="t">Time (in seconds since epoch) of event to inject.</param>
        // <param name="value">Value of event to inject.</param>
        // <returns>Returns an Event instance or null on failure.</returns>
        public Event Set(string label, string value, string t)
        {
            try {
                WebClient client = new WebClient();
                NameValueCollection post_data = new NameValueCollection();
                post_data.Add("value", value);
                post_data.Add("t", t);

                byte[] response_bytes = client.UploadValues(this.Url + "/set/" + label, "POST", post_data);
                string response = Encoding.UTF8.GetString(response_bytes);

                Console.WriteLine(response);
                return ParseJsonResponse(response);
            }
            catch (WebException e) {
                Console.WriteLine(e.Message);
                return null;
            }
        }
    }
}
