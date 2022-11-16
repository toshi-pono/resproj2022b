ConnectionMatrix = list[list[bool]]


def connect_node(matrix: ConnectionMatrix, id1: int, id2: int):
    matrix[id1][id2] = True
    matrix[id2][id1] = True


def create_matrix(num_nodes: int) -> ConnectionMatrix:
    return [[False for _ in range(num_nodes)] for _ in range(num_nodes)]


def load_connection_matrix(path: str) -> tuple[ConnectionMatrix, int]:
    with open(path) as f:
        NODE_NUM = int(f.readline())
        matrix = create_matrix(NODE_NUM)
        for line in f:
            id1, id2 = map(int, line.split())
            connect_node(matrix, id1 - 1, id2 - 1)
        return matrix, NODE_NUM
