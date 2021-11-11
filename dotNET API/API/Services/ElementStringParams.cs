using System.Collections.Generic;

namespace API.Services
{
    public class ElementStringParams
    {
        public IList<string> Tags { get; set; }
        public IList<string> Types { get; set; }
        public IList<string> Elements { get; set; }
    }
}