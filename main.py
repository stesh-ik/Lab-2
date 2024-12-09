import json
import csv
import random

DATASET_PATH = 'books-en.csv'
OUT_PATH_AUTHOR = 'author.json'
OUT_PATH_BIBL = 'books.json'


def get_title(dataset):
    dataset.seek(0)
    title = next(dataset)
    title = title.split(';')
    title = [col.strip() for col in title]
    return title


def get_object(line, title):
    reader = csv.DictReader([line], title, delimiter=';', quotechar='"')
    res = next(reader)
    return res


def filter_year(dataset, title, year):
    filtered = []

    for line in dataset:
        obj = get_object(line, title)
        year_value = obj['Year-Of-Publication']
        if year_value == str(year):
            filtered.append(obj)

    dataset.seek(0)
    return filtered


def filter_book_title(dataset, title):
    ans = 0

    for line in dataset:
        obj = get_object(line, title)
        book_title_value = obj['Book-Title']
        if len(book_title_value) > 30:
            ans += 1

    dataset.seek(0)
    return ans


def find_by_author_filtered(dataset, title, author):
    results = []
    
    for line in dataset:
        obj = get_object(line, title)
        author_value = obj['Book-Author']
        if author_value.capitalize() == author.capitalize():
            if (int(obj['Year-Of-Publication']) == 2014) or \
                (int(obj['Year-Of-Publication']) == 2016) or \
                    (int(obj['Year-Of-Publication']) == 2017):
                results.append(obj)

    dataset.seek(0)
    return results


def find_by_isbn(dataset, title, isbn):
    for line in dataset:
        obj = get_object(line, title)
        isbn_value = obj['ISBN']
        if isbn_value == isbn:
            author, book_title, year = obj['Book-Author'], obj['Book-Title'], \
                obj['Year-Of-Publication']
            break

    dataset.seek(0)
    return f'{author}. {book_title} - {year}'


if __name__ == '__main__':
    with open(DATASET_PATH) as dataset:

        title = get_title(dataset)
        print(filter_book_title(dataset, title))

        res = find_by_author_filtered(dataset, title, input())
        ans = json.dumps(res, indent=4)
        with open(OUT_PATH_AUTHOR, 'w') as out:
            out.write(ans)
        isbns = []
        for line in dataset:
            obj = get_object(line, title)
            isbns.append(obj['ISBN'])
        dataset.seek(0)
        
        res = []
        for j in range(20):
            res.append(find_by_isbn(dataset, title, random.choice(isbns)))
        ans = json.dumps(res, indent = 4)
        with open(OUT_PATH_BIBL, 'w') as out:
            out.write(ans)
