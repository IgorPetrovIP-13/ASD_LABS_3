import os


def output_file(path: str):
    with open(path, "rb") as file:
        if os.path.getsize(path) >= 400:
            print(f'\nFile ({path}):', [int.from_bytes(file.read(4), "big") for _ in range(50)], '...', end='')
            file.seek(os.path.getsize(path) - 50*4)
            print('', [int.from_bytes(file.read(4), "big") for _ in range(50)])
        else:
            print(f'\nFile ({path}):', [int.from_bytes(file.read(4), "big") for _ in range(os.path.getsize(path)//4)])