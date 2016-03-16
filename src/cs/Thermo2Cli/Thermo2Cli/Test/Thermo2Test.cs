using Xunit;
using Thermo2;

namespace Thermo2Test {
    public class TestApi
    {
        [Fact]
        public void ConstructorTest()
        {
            Api api = new Api();

            Assert.Equal(api.GetHost(), "127.0.0.1");
            Assert.Equal(api.GetPort(), 8822);
            Assert.Equal(api.GetUrl(), "http://127.0.0.1:8822");
        }
    }
}
