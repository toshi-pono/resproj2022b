import random
from node import connection
from node.send import generate_broadcast
from node.base import PredictNode

Pa: float = 0.1
Pb: float = 0.1


class AtsNode(PredictNode):
    def is_send(self) -> bool:
        # send always
        return True


# とりあえず2個で
NODE_NUM = 2
if __name__ == "__main__":
    random.seed(42)

    # Create the network
    connection_matrix = connection.create_matrix(NODE_NUM)
    connection.connect_node(connection_matrix, 0, 1)

    # Create the nodes
    nodes: list[AtsNode] = []
    for i in range(NODE_NUM):
        nodes.append(AtsNode(id=i, alpha=random.uniform(
            0.9, 1.1), beta=random.uniform(-0.5, 0.5), Pa=Pa, Pb=Pb))
    for i in range(NODE_NUM):
        nodes[i].send = generate_broadcast(nodes, connection_matrix)

    # Run the simulation
    for t in range(50):
        print(
            f't={t}, diff={nodes[0].get_predict_time(t) - nodes[1].get_predict_time(t):.3g}, origin={nodes[0].get_node_time(t) - nodes[1].get_node_time(t):.3g}')
        print(nodes[0].raw_node._RawNode__beta * nodes[0].alpha_hat + nodes[0].beta_hat,
              nodes[1].raw_node._RawNode__beta * nodes[1].alpha_hat + nodes[1].beta_hat, (nodes[0].raw_node._RawNode__beta + nodes[1].raw_node._RawNode__beta) / 2)

        for i in range(NODE_NUM):
            nodes[i].update_time(t)
        for i in range(NODE_NUM):
            nodes[i].update_send()
        for i in range(NODE_NUM):
            nodes[i].update_prediction()

        # print("------------")
        # print(nodes[0].last_datas[0])
        # print(nodes[0].last_datas[1])
        # print("------------")
