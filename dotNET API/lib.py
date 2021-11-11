from json import load


def get_tags(file_name):
    with open(file_name, encoding='utf-8') as f:
        return load(f)


def get_elements(file_name):
    with open(file_name, encoding='utf-8') as f:
        return load(f)


def find_elements(elements, type_names, tag_names):
    '''
    Finds elements that matches the most tags and returns them
    '''
    matching_elements = []

    for element in elements:
        element_type_names = [tag['urlName'] for tag in element['appTypes']]
        type_intersection = set(type_names).intersection(set(element_type_names))
        n = len(type_intersection)
        if n > 0:
            element['matchingTypes'] = list(type_intersection)
            matching_elements.append(element)
    
    elements = matching_elements

    for element in elements:
        element_tag_names = [tag['urlName'] for tag in element['tags']]
        tag_intersection = set(tag_names).intersection(set(element_tag_names))
        n = len(tag_intersection)
        if n > 0:
            element['matchingTags'] = list(tag_intersection)
            matching_elements.append(element)

    matching_elements.sort(key=lambda x: len(x['matchingTags']), reverse=True)
    return list(matching_elements)
