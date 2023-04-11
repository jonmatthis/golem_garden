import math
import regex as re

class StringChopper:
    """
    A class to chop a long string into a list of shorter strings with the specified chunk size and overlap.

    Attributes:
        chunk_size (int): The size of the chunks.
        overlap (int): The number of characters that overlap between two consecutive chunks.
    """

    def __init__(self, chunk_size: int, overlap: int):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _get_characters(self, text: str) -> list:
        return re.findall(r'\X', text)

    def chop_string(self, long_string: str) -> list:
        if self.chunk_size <= self.overlap:
            raise ValueError("Chunk size should be greater than overlap.")

        step_size = self.chunk_size - self.overlap
        characters = self._get_characters(long_string)
        num_chunks = math.ceil(len(characters) / step_size)

        chunks = []
        for i in range(num_chunks):
            start = i * step_size
            end = start + self.chunk_size

            if end > len(characters):
                chunk = ''.join(characters[start:]) + ' ' * (end - len(characters))
            else:
                chunk = ''.join(characters[start:end])

            chunks.append(chunk)

        return chunks




def test_string_chopper():
    # Test Case 1
    chopper1 = StringChopper(chunk_size=20, overlap=5)
    long_string1 = "This is a very long string that will be chopped into smaller strings according to the given parameters. 😀🚀"
    expected_output1 = [
        "This is a very long ",
        "long string that wil",
        "t will be chopped in",
        "ed into smaller stri",
        " strings according t",
        "ing to the given par",
        "n parameters. 😀🚀    ",
        "🚀                   "
    ]
    assert chopper1.chop_string(
        long_string1) == expected_output1, f"Test Case 1 failed.\n Expected output: \n{expected_output1}, \n Received output: \n{chopper1.chop_string(long_string1)}"

    # Test Case 2
    chopper2 = StringChopper(chunk_size=10, overlap=3)
    long_string2 = "ABCDEFGHIJKLMN"
    expected_output2 = [
        "ABCDEFGHIJ",
        "HIJKLMN   "
    ]

    assert chopper2.chop_string(
        long_string2) == expected_output2, f"Test Case 2 failed.\n Expected output: \n{expected_output2}, \n Received output: \n{chopper2.chop_string(long_string2)}"

    # Test Case 3
    chopper3 = StringChopper(chunk_size=5, overlap=2)
    long_string3 = "12345"
    expected_output3 = [
        "12345"
    ]
    assert chopper3.chop_string(
        long_string3) == expected_output3, f"Test Case 3 failed.\n Expected output: \n{expected_output3}, \n Received output: \n{chopper3.chop_string(long_string3)}"

    # Test Case 4
    chopper4 = StringChopper(chunk_size=8, overlap=4)
    long_string4 = "The quick brown fox jumps over the lazy dog."
    expected_output4 = [
        "The quic",
        "quick bro",
        "ck brown ",
        "own fox j",
        " fox jumps",
        "umps over",
        "s over the",
        "r the lazy",
        "e lazy dog",
        "y dog.    "
    ]
    assert chopper4.chop_string(
        long_string4) == expected_output4, f"Test Case 4 failed.\n Expected output: \n{expected_output4}, \n Received output: \n{chopper4.chop_string(long_string4)}"

if __name__ == "__main__":
    chunk_size = 20
    overlap = 5
    long_string = "This is a very long string that will be chopped into smaller strings according to the given parameters. 😀🚀"

    chopper = StringChopper(chunk_size, overlap)
    chopped_strings = chopper.chop_string(long_string)

    for i, chunk in enumerate(chopped_strings):
        print(f"Chunk {i + 1}: {chunk}")

    test_string_chopper()