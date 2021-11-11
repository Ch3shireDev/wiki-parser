from json import load, dump


with open('elements.json', 'r', encoding='utf-8') as f:
    elements = load(f)

app_types_dict = {}

for element in elements:
    appTypes = element['appTypes']
    for appType in appTypes:
        urlName = appType['urlName']
        appType['count'] = 1
        if urlName not in app_types_dict:
            app_types_dict[urlName] = appType
        else:
            app_types_dict[urlName]['count'] += 1

appTypes = app_types_dict.values()
appTypes = list(appTypes)

with open('types.json', 'w', encoding='utf-8') as f:
    dump(appTypes, f, ensure_ascii=False, indent=4)