def function_without_parameters():
    print("I did a thing")


def function_with_parameters(one, two):
    print("first parameter was " + one)
    print("second parameter was " + two)


if __name__ == "__main__":
    print("example functions")
    function_without_parameters()
    function_with_parameters("hello", "world")
