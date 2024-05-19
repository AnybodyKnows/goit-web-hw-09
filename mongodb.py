
import argparse
import json

from mongoengine import (
    connect,
    Document,
    StringField,
    ListField,
    ReferenceField
)

connect(
    db="HW08",
    host="mongodb+srv://goittestdb:1234@cluster0.goh2ue4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

# parser = argparse.ArgumentParser(description="Server Cats Enterprise")
# parser.add_argument("--action", help="create, update, read, delete")  # CRUD action
# parser.add_argument("--id")
# parser.add_argument("--name")
# parser.add_argument("--age")
# parser.add_argument("--features", nargs="+")
#
# arg = vars(parser.parse_args())
#
# action = arg.get("action")
# pk = arg.get("id")
# name = arg.get("name")
# age = arg.get("age")
# features = arg.get("features")


class Author(Document):
    fullname = StringField(max_length=150, required=True)
    born_date = StringField(max_length=20, required=True)
    born_location = StringField(max_length=150, required=True)
    description = StringField(required=True)


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)


with open("authors.json", "r", encoding="UTF-8") as f:
    data_read = json.load(f)
    for el in data_read:
        if not Author.objects(fullname=el["fullname"]).first():
            author = Author(fullname=el["fullname"],
                            born_date=el["born_date"],
                            born_location=el["born_location"],
                            description=el["description"]
                            )
            author.save()


with open("quotes.json", "r", encoding="UTF-8") as f:
    data_read = json.load(f)
    for el in data_read:
        author_name = el["author"]
        author_id = Author.objects(fullname=author_name).first()
        if author_id:
            if not Quotes.objects(quote=el['quote'], author=author_id).first():
                quotes = Quotes(tags=el["tags"],
                                author=author_id,
                                quote=el["quote"]
                                )
                quotes.save()


def parse_input(inputs):
    try:
        cmd, params = inputs.split(":", 1)
    except:
        cmd = inputs
        params = None
    return cmd, params


def main():
    while True:
        inputs = input("Enter command: ")
        cmd, params = parse_input(inputs)

        if cmd == "exit":
            break
        elif cmd == "tag":
            result = Quotes.objects(tags__contains=params)
            for el in result:
                print(el.quote.encode('utf-8').decode('utf-8'))

        elif cmd == "tags":
            tags = params.split(',')
            result = Quotes.objects(tags__in=tags)
            for el in result:
                print(el.quote.encode('utf-8').decode('utf-8'))

        elif cmd == "name":
            author_nm = params.strip()
            authorid = Author.objects(fullname=author_nm).first()
            if authorid:
                result = Quotes.objects(author=authorid)
                for el in result:
                    print(el.quote.encode('utf-8').decode('utf-8'))
            else:
                print("Author not found")


if __name__ == "__main__":
    main()

# name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
#
# tag:life — знайти та повернути список цитат для тега life;
# tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
# exit — завершити виконання скрипту;