using System.Collections.Generic;
using System.IO;
using System.Linq;
using API.Models;
using Newtonsoft.Json;

namespace API.Services
{
    public class ElementsJsonService : IElementsService
    {
        private readonly string elementsPath = "D:\\Users\\Cheshire\\Documents\\GitHub\\alternative-to\\data\\elements.json";
        private readonly string tagsPath = "D:\\Users\\Cheshire\\Documents\\GitHub\\alternative-to\\data\\tags.json";
        private readonly string typesPath = "D:\\Users\\Cheshire\\Documents\\GitHub\\alternative-to\\data\\types.json";

        private IList<Element> elements => JsonConvert.DeserializeObject<IList<Element>>(File.ReadAllText(elementsPath));
        private IList<AppType> types => JsonConvert.DeserializeObject<IList<AppType>>(File.ReadAllText(typesPath));
        private IList<Tag> tags => JsonConvert.DeserializeObject<IList<Tag>>(File.ReadAllText(tagsPath));

        public ElementsServiceParams GetData(ElementStringParams parameters)
        {
            var elementsMatchingTypes = elements;

            if (parameters.Types != null)
                elementsMatchingTypes = elements
                    .Where(element =>
                        parameters.Types
                            .All(
                                selectedType => element.appTypes
                                    .Select(type => type.urlName)
                                    .Any(type => type == selectedType)
                            )
                    ).ToList();

            var foundElements = elementsMatchingTypes;

            if (parameters.Tags != null)
                foundElements = elementsMatchingTypes
                        .Select(element =>
                            {
                                element.MatchingTagsCount =
                                    parameters.Tags
                                        .Intersect(element.tags.Select(tag => tag.urlName))
                                        .Count();
                                return element;
                            }
                        )
                        .Where(element => element.MatchingTagsCount > 0)
                        .ToList()
                    ;

            var foundTagsDict = new Dictionary<string, Tag>();
            foreach (var element in elementsMatchingTypes)
            foreach (var tag in element.tags)
                if (!foundTagsDict.ContainsKey(tag.urlName))
                {
                    tag.Count = 1;
                    foundTagsDict.Add(tag.urlName, tag);
                }
                else
                {
                    foundTagsDict[tag.urlName].Count += 1;
                }

            var foundTags = foundTagsDict.Values.OrderByDescending(t => t.Count).ToList();

            if (parameters.Tags != null)
                foundTags = foundTags.OrderByDescending(t => parameters.Tags.Contains(t.urlName)).ThenByDescending(t => t.Count).ToList();

            var foundTypesDict = new Dictionary<string, AppType>();

            foreach (var element in elementsMatchingTypes)
            foreach (var type in element.appTypes)
            {
                var name = type.appType;
                if (!foundTypesDict.ContainsKey(name))
                {
                    type.Count = 1;
                    foundTypesDict.Add(name, type);
                }
                else
                {
                    foundTypesDict[name].Count += 1;
                }
            }

            var foundTypes = foundTypesDict.Values.OrderByDescending(t=>t.Count).ToList();

            if (parameters.Types != null)
                foundTypes = foundTypes.OrderByDescending(t => parameters.Types.Contains(t.urlName)).ThenByDescending(t=>t.Count).ToList();

            return new ElementsServiceParams
            {
                Elements = foundElements,
                Types = foundTypes,
                Tags = foundTags
            };
        }
    }
}