from typing import Iterator


def get_lines_from_file(file_path: str) -> Iterator[str]:
    """
    Takes in a string representing a file path and returns a generator of lines in the file
    """
    with open(file_path, 'r') as handle:
        for line in handle:
            yield line.strip()
