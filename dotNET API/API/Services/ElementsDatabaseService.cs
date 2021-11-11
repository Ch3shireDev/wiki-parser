using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using API.Models;

namespace API.Services
{
    public class ElementsDatabaseService : IElementsService
    {
        public ElementsServiceParams GetData(ElementStringParams parameters = null)
        {

            var connectionString = @"Server=localhost\SQLEXPRESS;Database=WIKI_DB;Trusted_Connection=True;";
            using var connection = new SqlConnection(connectionString);
            connection.Open();

            var elements = GetElements(connection, parameters).ToList();
            var tags = GetTags(connection, parameters).ToList();
            var types = GetTypes(connection, parameters).ToList();

            connection.Close();

            return new ElementsServiceParams
            {
                Elements = elements,
                Tags = tags,
                Types = types,
            };
        }

        public IEnumerable<Element> GetElements(SqlConnection connection, ElementStringParams parameters)
        {
            var query =
                @"
SELECT TOP(100) 
    ARTICLE_URL, 
    ARTICLE_TITLE, 
    ARTICLE_CONTENT 
FROM ARTICLES 
    where ARTICLE_TITLE IS NOT NULL
";
            using var command = new SqlCommand(query, connection);
            var reader = command.ExecuteReader();
            while (reader.Read())
            {
                var element = new Element
                {
                    name = reader["ARTICLE_TITLE"] as string,
                    shortDescriptionOrTagLine = reader["ARTICLE_CONTENT"] as string,
                    urlName = reader["ARTICLE_URL"] as string
                };

                yield return element;
            }
            reader.Close();
        }

        public IEnumerable<Tag> GetTags(SqlConnection connection, ElementStringParams parameters)
        {
            var query = "SELECT TOP(100) KEYWORD_TITLE, KEYWORD_URL FROM KEYWORDS";
            using var command = new SqlCommand(query, connection);
            var reader = command.ExecuteReader();
            while (reader.Read())
            {
                var tag = new Tag
                {
                    name = reader["KEYWORD_TITLE"] as string,
                    urlName = reader["KEYWORD_URL"] as string,
                };
                yield return tag;
            }
            reader.Close();
        }

        public IEnumerable<AppType> GetTypes(SqlConnection connection, ElementStringParams parameters)
        {
            var query = "SELECT TOP(100) CATEGORY_TITLE, CATEGORY_URL FROM CATEGORIES WHERE CATEGORY_TITLE IS NOT NULL";
            using var command = new SqlCommand(query, connection);
            var reader = command.ExecuteReader();
            while (reader.Read())
            {
                var type = new AppType
                {
                    name = reader["CATEGORY_TITLE"] as string,
                    urlName = reader["CATEGORY_URL"] as string,
                    appType = reader["CATEGORY_TITLE"] as string
                };
                yield return type;
            }
            reader.Close();
        }
    }
}