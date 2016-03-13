using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Thermo2;
using CommandLine;

namespace Thermo2Cli
{
    class Options
    {
        [Option('s', "set", HelpText = "Inject event")]
        public string Set { get; set; }

        [Option('g', "get", HelpText = "Get cached event")]
        public string Get { get; set; }

        [Option('v', "value", HelpText = "Value of event to inject")]
        public string Value { get; set; }

        [HelpOption]
        public string GetUsage()
        {
            var usage = new StringBuilder();
            usage.AppendLine("Thermo2 client");
            return usage.ToString();
        }
    }

    class Thermo2Cli
    {
        static int Main(string[] args)
        {
            var options = new Options();
            CommandLine.Parser parser = new Parser();
            if(parser.ParseArguments(args, options)) {
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

                if(options.Get==null && options.Set==null) {
                    Console.WriteLine("Either specify -s or -g");
                    return -1;
                }

                var api = new Api();

                if(options.Get!=null) {
                    // get
                    Value get_value = api.Get(options.Get);
                    Console.WriteLine(get_value);
                    return 0;
                } else {
                    // set
                    Console.WriteLine("Set not implemented yet..");
                    return -1;
                }
            } else {
                Console.WriteLine(options.GetUsage());
                return -1;
            }
        }
    }
}
