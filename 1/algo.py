import os
import random
from config import MIN_VALUE, MAX_VALUE


class DefaultSort:
    def __init__(self, n: int, input_name: str, output_name: str, number_of_files: int):
        self.__n = n
        self.__input_name = input_name
        self.__output_name = output_name
        self.__number_of_files = number_of_files
        self.__B_files = [f"{i + 1}B.dat" for i in range(number_of_files)]
        self.__C_files = [f"{i + 1}C.dat" for i in range(number_of_files)]

    def solve(self):
        self.__create_initial(self.__n)
        self.__merge([self.__input_name], self.__B_files)
        flag = 1
        while not self.__is_sorted():
            if flag == 1:
                self.__merge(self.__B_files, self.__C_files)
            else:
                self.__merge(self.__C_files, self.__B_files)
            flag = -flag
        if os.path.getsize(self.__B_files[0]) == os.path.getsize(self.__input_name):
            shutil.copy(self.__B_files[0], self.__output_name)
        else:
            shutil.copy(self.__C_files[0], self.__output_name)

    def __is_sorted(self):
        return os.path.getsize(self.__B_files[0]) == os.path.getsize(self.__input_name) \
            or os.path.getsize(self.__C_files[0]) == os.path.getsize(self.__input_name)

    def __merge(self, input_files: list, output_files: list):
        inputs = [FileReader(i) for i in input_files]
        outputs = [open(i, 'wb') for i in output_files]
        j = 0
        while not self.__merged(inputs):
            number = MAX_VALUE
            index = -1
            for i in range(len(inputs)):
                binary_number = inputs[i].get_current()
                if binary_number:
                    int_number = int.from_bytes(binary_number, byteorder='big')
                    prev = inputs[i].get_prev()
                    if not prev or int_number >= int.from_bytes(prev, byteorder='big'):
                        if int_number <= number:
                            number = int_number
                            index = i
            if index == -1:
                for i in inputs:
                    i.null_prev()
                j = (j + 1) % self.__number_of_files
            else:
                outputs[j].write(number.to_bytes(4, "big"))
                inputs[index].next_number()
        for i in inputs: i.close_file()
        for o in outputs: o.close()

    def __create_initial(self, n: int):
        with open(self.__input_name, 'wb') as f:
            for i in range(n):
                f.write(random.randint(MIN_VALUE, MAX_VALUE).to_bytes(4, byteorder="big"))
            for i in range(self.__number_of_files):
                open(self.__B_files[i], 'wb').close()
                open(self.__C_files[i], 'wb').close()

    def __merged(self, readers: list):
        for reader in readers:
            if reader.get_current():
                return False
        return True


class FileReader:
    def __init__(self, file_path: str):
        self.__file = open(file_path, "rb")
        self.__prev = None
        self.__current_value = self.__file.read(4)

    def null_prev(self):
        self.__prev = None

    def get_prev(self):
        return self.__prev

    def get_current(self):
        return self.__current_value

    def close_file(self):
        self.__file.close()

    def next_number(self):
        self.__prev, self.__current_value = self.__current_value, self.__file.read(4)
