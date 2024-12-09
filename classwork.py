import json


DATASET_PATH = 'memes_dataset.csv'
OUT_PATH = 'out.json'

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

def get_object_all(line, title):
    reader = csv.DictReade([line], title, delimiter=',', quotechar='"')
    res = next(reader)
    return res

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
    with open(DATASET_PATH, encoding="utf8") as dataset:
        title = get_title(dataset)
        # line = next(dataset)
        # res = get_object(line, title)
        # print(res, len(res))
        res = filter_year(dataset, title, 2008)
        res = json.dumps(res, indent = 4)
        print(res)
        with open(OUT_PATH, 'w') as out:
            out.write(res)