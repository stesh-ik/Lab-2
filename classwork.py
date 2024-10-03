import json


DATESET_PATH = 'memes_dataset.csv'

def get_title(dataset):
    dataset.seek(0)
    title = next(dataset)
    title = title.split(',')
    title = [col.strip() for col in title]
    return title

def get_object(line, title):
    flieds = []
    value = ''
    in_complex = False

    for char in line:
        if in_complex:
            value += char

            if char == '"':
                value = value[:-1]
                flieds.append(value)
                value = ''
                in_complex = False
        else: 
            if char not in [',', '"']:
                value += char
                continue
            if char == ',':
                flieds.append(value)
                value = ''
                continue
            if char == '"':
                in_complex = True
                continue
    
    result = dict()
    for col, flied in zip(title, flieds):
        result[col] = flied
    return result

def filter_year(dataset, title, year):
    filtered = []

    for line in dataset:
        obj = get_object(line, title)
        year_value = obj['origin_year']
        if year_value == str(year):
            filtered.append(obj)
    dataset.seek(0)
    return filtered


if __name__ == '__main__':
    with open(DATESET_PATH) as dataset:
        title = get_title()
        res = filter_year(dataset, title, 2008)
        print(res, len(res))
        res = 