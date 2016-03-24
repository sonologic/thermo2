using Xunit;
using Thermo2;
using System.Threading;
using System.Net;
using System;
using System.Threading.Tasks;

namespace Thermo2Test
{
    public class WebServer
    {
        private bool _abort = false;
        public bool abort
        {
            get { lock(this) { return _abort; } }
            set { lock(this) { _abort = value; } }
        }

        public void Run()
        {
            HttpListener listener = new HttpListener();
            // runas netsh http add urlacl url=http://127.0.0.1:41827/get/ user=gmc
            listener.Prefixes.Add("http://127.0.0.1:41827/get/");
            listener.Start();

            while(!abort)
            {
                System.Console.WriteLine("in server loop");

                Task<HttpListenerContext> task = listener.GetContextAsync();

                while(!task.IsCompleted && !abort)
                {
                    Console.WriteLine("in task loop");
                    Thread.Sleep(1000);
                }

                if (!abort)
                {
                    HttpListenerContext context = task.Result; // listener.GetContext();
                    HttpListenerRequest request = context.Request;
                    HttpListenerResponse response = context.Response;

                    byte[] buffer = System.Text.Encoding.UTF8.GetBytes("{ label:\"test_value\", t: 3.14 }");
                    response.ContentLength64 = buffer.Length;
                    System.IO.Stream output = response.OutputStream;
                    output.Write(buffer, 0, buffer.Length);
                    output.Close();
                }
            }

            System.Console.WriteLine("aborting webserver");
            listener.Stop();
            System.Console.WriteLine("webserver aborted");
        }
    }

    public class TestApi : IDisposable
    {
        private WebServer ws;
        private Thread wsThread;

        [Fact]
        public void VoidConstructorTest()
        {
            Api api = new Api();

            Assert.Equal(api.GetHost(), "127.0.0.1");
            Assert.Equal(api.GetPort(), 8822);
            Assert.Equal(api.GetUrl(), "http://127.0.0.1:8822");
        }

        [Fact]
        public void ConstructorTest()
        {
            Api api = new Api("example.com", 12345);

            Assert.Equal(api.GetHost(), "example.com");
            Assert.Equal(api.GetPort(), 12345);
            Assert.Equal(api.GetUrl(), "http://example.com:12345");
        }

        [Fact]
        public void GetTest()
        {
            Api api = new Api("localhost", 41827);

            Event e = api.Get("test_value");

        }

        public TestApi()
        {
            ws = new WebServer();

            wsThread = new Thread(new ThreadStart(ws.Run));

            wsThread.Start();

            while (!wsThread.IsAlive) ;
        }

        public void Dispose()
        {
            System.Console.WriteLine("aborting thread");

            //wsThread.Abort();
            ws.abort = true;

            System.Console.WriteLine("joining thread");

            wsThread.Join();

            System.Console.WriteLine("done");
        }
    }
}