from typing import List

from models.models import Author, Quote
from connection.connect import get_connection


def find_by_tag(tag: str) -> List[str]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


def find_by_author(author: Author) -> dict[str, List[str]]:
    print(f"Find by {author.fullname}")
    quotes = Quote.objects(author=author)
    result = {author.fullname: [q.quote for q in quotes]}
    return result


def main():
    while True:
        command = input("Enter command: ")
        if command.startswith("name:"):
            author_name = command.split(":", 1)[1].strip()
            author = Author.objects(fullname__iregex=author_name).first()
            if author:
                result = find_by_author(author)
                print(result)
            else:
                print(f"No author found with name: {author_name}")

        elif command.startswith("tag:"):
            tag = command.split(":", 1)[1].strip()
            result = find_by_tag(tag)
            if result:
                print(result)
            else:
                print(f"No quotes found for tag: {tag}")

        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip().split(",")
            results = []
            for tag in tags:
                tag_results = find_by_tag(tag)
                if tag_results:
                    results.extend(tag_results)
                else:
                    print(f"No quotes found for tag: {tag}")
            if results:
                print(results)

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
    main()