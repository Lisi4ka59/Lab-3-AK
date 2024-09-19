def test_answer():
    with open("tests/Hello_user_name/Hello_user_name_answer", "r") as answer:
        with open("output.txt", "r") as output:
            assert answer.read() == output.read()
    with open("tests/Hello_user_name/Hello_user_name_log", "r") as answer:
        with open("log.txt", "r") as output:
            assert answer.read() == output.read()
