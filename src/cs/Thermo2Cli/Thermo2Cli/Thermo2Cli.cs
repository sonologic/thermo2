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

        [Option('g', "get", HelpText = "Get cachd event")]
        public string Get { get; set; }

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
        static void Main(string[] args)
        {
            
            Console.WriteLine("Hello, world..");
        }
    }
}
