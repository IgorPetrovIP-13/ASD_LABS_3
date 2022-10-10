import os


def output_file(path: str):
    with open(path, "rb") as fileA:
        if os.path.getsize(path) >= 400:
            number = 100
        else:
            number = os.path.getsize(path)//4
        print(f'\nFile ({path}):', [int.from_bytes(fileA.read(4), "big") for _ in range(number)], '...')
