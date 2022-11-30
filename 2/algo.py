from config import starting_values


class Node:
    def __init__(self, previous=None, current=None, g=None):
        self.prev = previous
        self.current = current
        self.g = g

    # def get_f(self):
    #     return sum(abs((val-1) % 3 - i % 3) + abs((val-1)//3 - i//3)
    #                for i, val in enumerate(self.current) if val) + self.g
    def get_f(self):
        count = 8
        for i in range(8):
            if self.current[i] == starting_values[i]:
                count -= 1
        return count + self.g


class Algorithm:
    def __init__(self, state: list):
        self.__start_state = state

    def solve_bfs(self):
        iterations = 0
        total_states = 1
        queue = [Node(None, self.__start_state)]
        while queue:
            state = queue.pop(0)
            iterations += 1
            if starting_values == state.current:
                return self.__get_values(state), iterations, total_states, len(queue)
            for neighbour in self.__neighbours(state.current):
                queue.append(Node(state, neighbour))
                total_states += 1

    def solve_a(self):
        iterations = 0
        opened_nodes = [Node(None, self.__start_state, 0)]
        closed_nodes = [self.__start_state]
        while opened_nodes:
            state = min(opened_nodes, key=lambda node: node.get_f())
            opened_nodes.remove(state)
            if state.current == starting_values:
                return self.__get_values(state), iterations, len(opened_nodes) + len(closed_nodes), len(opened_nodes) + len(closed_nodes)
            for neighbour in self.__neighbours(state.current):
                if neighbour not in closed_nodes:
                    opened_nodes.insert(0, Node(state, neighbour, state.g + 1))
                    # opened_nodes.append(Node(state, neighbour, state.g + 1))
                    closed_nodes.append(neighbour)
                    iterations += 1

    @staticmethod
    def __neighbours(state: list):
        res = list()
        ind = state.index(0)
        if not ind < 3:
            new = state.copy()
            new[ind], new[ind - 3] = new[ind - 3], new[ind]
            res.append(new)
        if not ind > 5:
            new = state.copy()
            new[ind], new[ind + 3] = new[ind + 3], new[ind]
            res.append(new)
        if ind not in [0, 3, 6]:
            new = state.copy()
            new[ind], new[ind - 1] = new[ind - 1], new[ind]
            res.append(new)
        if ind not in [2, 5, 8]:
            new = state.copy()
            new[ind], new[ind + 1] = new[ind + 1], new[ind]
            res.append(new)
        return res

    @staticmethod
    def __get_values(state: Node):
        res = list()
        while state.prev:
            res.append(state.current)
            state = state.prev
        res.append(state.current)
        return list(reversed(res))
