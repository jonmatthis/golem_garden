from experimental.knowledge_corpus_embeddings.string_chopper import StringChopper


def test_string_chopper():
    # Test Case 1
    chopper1 = StringChopper(chunk_size=20, overlap=5)
    long_string1 = "This is a very long string that will be chopped into smaller strings according to the given parameters. 😀🚀"
    expected_output1 = [
        "This is a very long ",
        "ng string that will ",
        "hat will be chopped ",
        "pped into smaller st",
        "aller strings accord",
        "rings according to th",
        "ding to the given pa",
        " the given parameter",
        " parameters. 😀🚀    ",
    ]
    assert chopper1.chop_string(long_string1) == expected_output1, f"Test Case 1 failed.\n Expected output: \n{expected_output1}, \n Received output: \n{chopper1.chop_string(long_string1)}"

    # Test Case 2
    chopper2 = StringChopper(chunk_size=10, overlap=3)
    long_string2 = "Hello world! This is a test."
    expected_output2 = [
        "Hello worl",
        "lo world! ",
        "orld! This",
        "d! This is",
        " This is a",
        "s is a tes",
        " is a test.",
    ]
    assert chopper2.chop_string(long_string2) == expected_output2

    # Test Case 3
    chopper3 = StringChopper(chunk_size=5, overlap=1)
    long_string3 = "abcde"
    expected_output3 = [
        "abcde",
    ]
    assert chopper3.chop_string(long_string3) == expected_output3

    # Test Case 4 (Empty string)
    chopper4 = StringChopper(chunk_size=5, overlap=1)
    long_string4 = ""
    expected_output4 = []
    assert chopper4.chop_string(long_string4) == expected_output4

    print("All test cases passed!")

if __name__ == "__main__":
    test_string_chopper()

