"""Basic tree implemenatation."""


class Node:
    def __init__(self, contents):
        self.contents = contents
        self.derivative = ""
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __str__(self):
        return self.contents

    def __repr__(self):
        return self.contents
