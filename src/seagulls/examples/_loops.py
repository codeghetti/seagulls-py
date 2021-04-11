def say_hello(person):
    print("hello, " + person)


if __name__ == "__main__":
    print("example loops")
    say_hello("bob")
    say_hello("tom")

    people = ["dave", "jane", "bill"]
    for person in people:
        say_hello(person)
