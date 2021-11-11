using System.Collections.Generic;
using API.Models;

namespace API.Services
{
    public class ElementsServiceParams
    {
        public IList<Tag> Tags { get; set; }
        public IList<AppType> Types { get; set; }
        public IList<Element> Elements { get; set; }
    }
}