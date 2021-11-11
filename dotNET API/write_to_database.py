from json import load
from pyodbc import connect

connection_string = r'Driver={ODBC Driver 17 for SQL Server};Server=localhost\SQLEXPRESS;Database=APPS_DB;Trusted_Connection=yes;'

connect = connect(connection_string, autocommit=True)
cursor = connect.cursor()
cursor.execute('USE APPS_DB')

with open('./data/elements.json', 'r', encoding='utf-8') as f:
    data = load(f)

tags = set()

for element in data:

    name = element['name']
    urlName = element['urlName']
    # description = element['shortDescriptionOrTagLine'].replace('&#39;', '\'')

    # cursor.execute("INSERT INTO APPS (APP_NAME, APP_URL_NAME, APP_DESCRIPTION) VALUES (?,?,?)", (name,urlName,description))

    for tag in element['tags']:

        if 'name' not in tag:
            continue

        name = tag['name']
        urlName = tag['urlName']
        
        if name == '' or urlName == '':
            continue

        if urlName in tags:
            continue

        cursor.execute("INSERT INTO TAGS (TAG_NAME, TAG_URL_NAME) VALUES (?,?)", (name,urlName))

        tags.add(urlName)

        # cursor.execute("INSERT INTO TAGS (TAG_NAME) VALUES (?)", (tag,))
        # cursor.execute("SELECT TAG_ID FROM TAGS WHERE TAG_NAME = ?", (tag,))
        # tag_id = cursor.fetchone()[0]
        # cursor.execute(
        #     "INSERT INTO TAGS_TO_APPS (TAG_ID, APP_ID) VALUES (?,?)", (tag_id, id))
