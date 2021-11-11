namespace API.Models
{
    public class Element
    {
        public string shortDescriptionOrTagLine { get; set; }
        public string licenseCost { get; set; }
        public string licenseModel { get; set; }
        public int alternatives { get; set; }
        public int likes { get; set; }
        public Platform[] platforms { get; set; }
        public Tag[] tags { get; set; }
        public AppType[] appTypes { get; set; }
        public TopAlternative[] topAlternatives { get; set; }
        public string id { get; set; }
        public Image[] images { get; set; }
        public bool adSenseBlocked { get; set; }
        public string name { get; set; }
        public string urlName { get; set; }
        public int MatchingTagsCount { get; set; }
    }
}