from algo import DefaultSort
from func import output_file


def main():
    num = int(input('Enter number of int numbers: '))
    files = int(input('Enter number of C and B files: '))
    solver = DefaultSort(num, 'A.dat', 'END.dat', files)
    solver.solve()
    output_file('A.dat')
    output_file('END.dat')


if __name__ == '__main__':
    main()
