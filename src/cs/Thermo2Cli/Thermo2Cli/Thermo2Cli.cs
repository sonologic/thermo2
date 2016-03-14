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
        [Option('s', "set", HelpText = "Inject event (requires -v or --value)")]
        public string Set { get; set; }

        [Option('g', "get", HelpText = "Get cached event")]
        public string Get { get; set; }

        [Option('v', "value", HelpText = "Value of event to inject")]
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

                var api = new Api();

                if(options.Get!=null) {
                    // get
                    Event get_value = api.Get(options.Get);
                    if(get_value == null) {
                        Console.WriteLine("no value");
                    } else {
                        Console.WriteLine(get_value.ToString());
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
                        Console.WriteLine("no value");
                    } else {
                        Console.WriteLine(set_value.ToString());
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
