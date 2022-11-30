def solvable(state: list):
    count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if state[j] and state[i] and state[i] > state[j]:
                count += 1
    return count % 2 == 0


def output_puzzle(array: list):
    string = str()
    for index, element in enumerate(array[0]):
        string += f'Step {index}:'
        for j in range(0, 9):
            if j % 3 == 0:
                string += '\n'
            string += str(element[j]) + ' '
        string += '\n\n'
    print(string)
    print("Iterations:", array[1])
    print("Total states:", array[2])
    print("States in memory:", array[3])
