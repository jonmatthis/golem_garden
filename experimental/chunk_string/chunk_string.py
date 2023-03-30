import math


class ChunkString:
    def __init__(self, input_string: str, chunk_size: int = 100, overlap: int = 10):
        """Initialize the ChunkString object.

        Args:
            input_string (str): The input string to be chunked.
            chunk_size (int): The size of each chunk.
            overlap (int): The number of overlapping characters between chunks.
        """
        self._input_string = input_string
        self._chunk_size = chunk_size
        self._overlap = overlap
        self._chunks = self._generate_chunks()

    @property
    def input_string(self) -> str:
        return self._input_string

    @input_string.setter
    def input_string(self, value: str):
        self._input_string = value
        self._chunks = self._generate_chunks()

    @property
    def chunk_size(self) -> int:
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value: int):
        self._chunk_size = value
        self._chunks = self._generate_chunks()

    @property
    def overlap(self) -> int:
        return self._overlap

    @overlap.setter
    def overlap(self, value: int):
        self._overlap = value
        self._chunks = self._generate_chunks()

    def _generate_chunks(self):
        """Generate the chunks from the input string.

        Returns:
            List[str]: List of chunked strings.
        """
        step_size = self._chunk_size - self._overlap
        num_chunks = math.ceil((len(self._input_string) - self._overlap) / step_size)

        chunks = []
        for i in range(num_chunks):
            start_idx = i * step_size
            end_idx = start_idx + self._chunk_size

            chunk = self._input_string[start_idx:end_idx]
            if len(chunk) < self._chunk_size:
                chunk = chunk.ljust(self._chunk_size, " ")

            chunks.append(chunk)

        return chunks

    def get_chunks(self):
        """Get the list of chunks.

        Returns:
            List[str]: List of chunked strings.
        """
        return self._chunks


if __name__ == "__main__":
    chunk_size_in = 100
    overlap_in = 20
    input_string_in = f"This is a very long string that needs to be chunked into smaller strings based on the " \
                      "parameters provided. The chunk size is {chunk_size_in} and the overlap is {overlap_in}." \
                      " The chunked strings will be returned as a list of strings." \
                      " Now I'm going to add a bunch of extra text to make sure that the chunking works properly." \
                      " just tab completing ai recommendations for the next word in a sentence now let's see if it" \
                      " can handle a sentence that is a little bit longer than the previous one and see if it will" \
                      " still be able to predict the next word in the sentence and see if it can handle a sentence however" \
                      " long it needs to be to make sure that it can handle a sentence that is a little bit longer than the"

chunk_string = ChunkString(input_string=input_string_in,
                           chunk_size=chunk_size_in,
                           overlap=overlap_in)
print(chunk_string.get_chunks())
print("Number of chunks:", len(chunk_string.get_chunks()))