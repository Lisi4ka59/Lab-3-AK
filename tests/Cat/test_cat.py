def test_input():
    with open("tests/Cat/Cat_answer", "r") as answer:
        with open("output.txt", "r") as output:
            assert answer.read() == output.read()


def test_log():
    with open("tests/Cat/Cat_log", "r") as answer:
        with open("log.txt", "r") as output:
            assert answer.read() == output.read()
          
