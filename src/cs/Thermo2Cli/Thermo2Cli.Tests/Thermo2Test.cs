using Xunit;
using Thermo2;

namespace Thermo2Test
{
    public class TestApi
    {
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

    }
}