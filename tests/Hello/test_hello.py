def test_answer():
    with open("tests/Hello/Hello_answer", "r") as answer:
        with open("output.txt", "r") as output:
            assert answer.read() == output.read()
    with open("tests/Hello/Hello_log", "r") as answer:
        with open("log.txt", "r") as output:
            assert answer.read() == output.read()
