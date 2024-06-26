from models.models import Author, Quote
from connection.connect import get_connection


def search_quotes():
    while True:
        command = input("Enter command: ")
        if command.startswith("name:"):
            author_name = command.split(":", 1)[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                if quotes:
                    for quote in quotes:
                        print(quote.tags)
                else:
                    print(f"No quotes found for author: {author_name}")
            else:
                print(f"No author found with name: {author_name}")

        elif command.startswith("tag:"):
            tag = command.split(":", 1)[1].strip()
            quotes = Quote.objects(tags=tag)
            if quotes:
                for quote in quotes:
                    print(quote.tags)
            else:
                print(f"No quotes found for tag: {tag}")

        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip().split(",")
            quotes = Quote.objects(tags__in=tags)
            if quotes:
                for quote in quotes:
                    print(quote.tags)
            else:
                print(f"No quotes found for tags: {', '.join(tags)}")

        elif command.strip() == "exit":
            print("Exiting...")
            break

        else:
            print("Invalid command. Please use one of the following formats:")
            print("name:<author_name>")
            print("tag:<tag>")
            print("tags:<tag1>,<tag2>,...")
            print("exit")

if __name__ == '__main__':
    get_connection()
    search_quotes()