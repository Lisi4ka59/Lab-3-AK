def test_answer():
    with open("tests/Fibonnachi_answer", "r") as answer:
        with open("output.txt", "r") as output:
            assert answer.read() == output.read()
