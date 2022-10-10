import os
import random
import shutil
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
        sorted_set = list()
        while not self.__merged(inputs):
            min_value = MAX_VALUE
            min_index = -1
            for i in range(len(inputs)):
                binary_number = inputs[i].get_current()
                if binary_number:
                    int_number = int.from_bytes(binary_number, byteorder='big')
                    if not sorted_set or int_number >= sorted_set[-1]:
                        if int_number <= min_value:
                            min_value = int_number
                            min_index = i
            if min_index == -1:
                for num in sorted_set: outputs[j].write(num.to_bytes(4, "big"))
                sorted_set.clear()
                j = (j + 1) % self.__number_of_files
            else:
                sorted_set.append(min_value)
                inputs[min_index].next_number()
        for num in sorted_set: outputs[j].write(num.to_bytes(4, "big"))
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
        self.__current_value = self.__file.read(4)
        self.__next_value = self.__file.read(4)

    def get_current(self):
        return self.__current_value

    def close_file(self):
        self.__file.close()

    def next_number(self):
        temp = self.__current_value
        self.__current_value, self.__next_value = self.__next_value, self.__file.read(4)
        return temp
