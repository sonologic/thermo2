using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Thermo2;
using CommandLine;
using CommandLine.Text;

namespace Thermo2Cli
{
    class Options
    {
        [Option('h', "host", HelpText = "Host to connect to (defaults to 127.0.0.1)")]
        public string Host { get; set; }

        [Option('p', "port", HelpText = "Port to connect to (defaults to 8822)")]
        public int Port { get; set; }

        [Option('s', "set", HelpText = "Inject event (requires -v or --value)", MutuallyExclusiveSet = "set")]
        public string Set { get; set; }

        [Option('g', "get", HelpText = "Get cached event", MutuallyExclusiveSet = "get")]
        public string Get { get; set; }

        [Option('v', "value", HelpText = "Value of event to inject", MutuallyExclusiveSet = "set")]
        public string Value { get; set; }

        [HelpOption]
        public string GetUsage()
        {
            return HelpText.AutoBuild(this,
                (HelpText current) => HelpText.DefaultParsingErrorsHandler(this, current));
        }
    }

    class Thermo2Cli
    {
        static int Main(string[] args)
        {
            var options = new Options();
            CommandLine.Parser parser = new Parser();
            if(parser.ParseArguments(args, options)) {
/*
                Console.WriteLine("Get: ");
                if(options.Get!=null) {
                  Console.WriteLine(options.Get);
                } else {
                  Console.WriteLine("null");
                }

                Console.WriteLine("Set: ");
                if(options.Set!=null) {
                  Console.WriteLine(options.Set);
                } else {
                  Console.WriteLine("null");
                }

                Console.WriteLine("Value: ");
                if(options.Value!=null) {
                  Console.WriteLine(options.Value);
                } else {
                  Console.WriteLine("null");
                }
*/
                if(options.Get==null && options.Set==null) {
                    Console.WriteLine("Either specify -s or -g\n");
                    Console.WriteLine(options.GetUsage());
                    return -1;
                }

                string host = options.Host;
                if(host==null)
                    host = "127.0.0.1";

                int port = options.Port;

                if(port==0)
                    port = 8822;

                var api = new Api(host, port);

                if(options.Get!=null) {
                    // get
                    Event get_value = api.Get(options.Get);
                    if(get_value == null) {
                        Console.WriteLine(options.Get + "::");
                    } else {
                        Console.WriteLine(options.Get + ":" + get_value + ":" + get_value.GetTime());
                    }
                    return 0;
                } else {
                    // set
                    if(options.Value==null) {
                        Console.WriteLine("-s requires -v to be set\n");
                        Console.WriteLine(options.GetUsage());
                        return -1;
                    }
                    Event set_value = api.Set(options.Set, options.Value, "0.0");
                    if(set_value == null) {
                        Console.WriteLine(options.Get + "::");
                    } else {
                        Console.WriteLine(options.Set + ":" + set_value + ":" + set_value.GetTime());
                    }
                    return 0;
                }
            } else {
                Console.WriteLine(options.GetUsage());
                return -1;
            }
        }
    }
}
