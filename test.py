from node import connection


def test_connect_node():
    m, n = connection.load_connection_matrix("testcase/connection3.txt")
    print(n)
    print(m)


test_connect_node()
