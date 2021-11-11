namespace API.Models
{
    public class TopAlternative
    {
        public int likes { get; set; }
        public string id { get; set; }
        public Image[] images { get; set; }
        public bool adSenseBlocked { get; set; }
        public string name { get; set; }
        public string urlName { get; set; }
    }
}