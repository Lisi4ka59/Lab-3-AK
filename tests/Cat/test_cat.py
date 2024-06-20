def test_random_input():
    with open("input.txt", "r") as answer:
        with open("output.txt", "r") as output:
            assert answer.read() == output.read()


def test_input_log():
    with open("tests/Cat/Cat_answer", "r") as answer:
        with open("output.txt", "r") as output:
            assert answer.read() == output.read()
