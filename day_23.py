from itertools import chain

from common import read_input


class CircleNode:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedCircle:
    def __init__(self, values):
        self._set_values(values)

    def _set_values(self, iterable):
        first_value = iterable[0]
        first_node = CircleNode(first_value)
        self.nodes = {first_value: first_node}
        self.cursor = first_node

        for i in iterable[1:]:
            self._push(i)

        self.nodes[iterable[-1]].next = self.nodes[iterable[0]]  # Wrap to circle
        self.cursor = first_node
        self.max_value = max(self.nodes)

    def _push(self, value):
        node = CircleNode(value)
        self.nodes[value] = node
        self.cursor.next = node
        self.cursor = node

    def peek(self, n):
        res = []
        node = self.cursor
        for _ in range(n):
            node = node.next
            res.append(node.value)
        return res

    def set_cursor(self, value):
        self.cursor = self.nodes[value]

    def move(self, n):
        for _ in range(n):
            self._move()

    def _move(self):
        peek = self.peek(4)
        picked_up, next_one = peek[:3], peek[3]

        dst = self.cursor.value - 1
        if dst == 0:
            dst = self.max_value
        while dst in picked_up:
            dst -= 1
            if dst == 0:
                dst = self.max_value

        # Remove the three
        self.cursor.next = self.nodes[next_one]

        # Attach the picked up ones
        attach_point = self.nodes[dst].next
        self.nodes[dst].next = self.nodes[picked_up[0]]
        self.nodes[picked_up[2]].next = attach_point

        # Update cursor
        self.cursor = self.cursor.next

    def __repr__(self):
        return f"LinkedCircle with {len(self.nodes)} nodes. Cursor is at {self.cursor}"


def solve_1(raw_in):
    inputs = [int(i) for i in raw_in[0]]

    cups = LinkedCircle(inputs)
    cups.move(100)

    cups.set_cursor(1)
    return "".join(str(i) for i in cups.peek(8))


def solve_2(raw_in):
    MAX_VALUE = 1_000_000
    max_input = int(max(list(raw_in[0])))
    inputs = chain([int(i) for i in raw_in[0]], range(max_input + 1, MAX_VALUE + 1))

    cups = LinkedCircle([i for i in inputs])
    cups.move(10_000_000)

    cups.set_cursor(1)
    a, b = cups.peek(2)
    return a*b


if __name__ == "__main__":
    raw_in = read_input("data/day_23.txt")

    answer_1 = solve_1(raw_in)
    answer_2 = solve_2(raw_in)

    print(f"Part 1 answer: {answer_1}")
    print(f"Part 2 answer: {answer_2}")
