import csv
import time
from pathlib import Path
from typing import Any, List, Union

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running {func.__name__} ...", end='\r')
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} Done in {end - start:.2f} seconds")
        return result
    return wrapper

@timer
def read_file(filename: Union[str, Path]) -> List[List[int]]:
    """read_file

    Args:
        filename (Union[str, Path]): The filename to read

    Returns:
        List[List[int]]: The data in the file
    """
    return [
        [int(x) for x in line.split()]
        for line in Path(filename).read_text().splitlines()
    ]

@timer
def write_file(data: List[List[Any]], filename: Union[str, Path]) -> None:
    """write_file writes the data to a csv file and
    adds a header row with `relationship`, `support`, `confidence`, `lift`.

    Args:
        data (List[List[Any]]): The data to write to the file
        filename (Union[str, Path]): The filename to write to
    """
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["antecedent", "consequent", "support", "confidence", "lift"])
        writer.writerows(data)
