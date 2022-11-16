ConnectionMatrix = list[list[bool]]


def connect_node(matrix: ConnectionMatrix, id1: int, id2: int):
    matrix[id1][id2] = True
    matrix[id2][id1] = True


def create_matrix(num_nodes: int) -> ConnectionMatrix:
    return [[False for _ in range(num_nodes)] for _ in range(num_nodes)]
