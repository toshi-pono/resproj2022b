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


if __name__ == "__main__":
    random.seed(42)

    # Create the network
    connection_matrix, NODE_NUM = connection.load_connection_matrix(
        "testcase/connection3.txt")

    # Create the nodes
    nodes: list[AtsNode] = []
    for i in range(NODE_NUM):
        nodes.append(AtsNode(id=i, alpha=random.uniform(
            0.9, 1.1), beta=random.uniform(-0.5, 0.5), Pa=Pa, Pb=Pb))
    for i in range(NODE_NUM):
        nodes[i].send = generate_broadcast(nodes, connection_matrix)

    # Run the simulation
    for t in range(50):
        # diffを計算する
        max_diff = 0
        max_origin_diff = 0
        for i in range(NODE_NUM):
            for j in range(NODE_NUM):
                if i == j:
                    continue
                diff = abs(nodes[i].get_predict_time(
                    t) - nodes[j].get_predict_time(t))
                origin_diff = abs(nodes[i].get_node_time(
                    t) - nodes[j].get_node_time(t))
                if diff > max_diff:
                    max_diff = diff
                if origin_diff > max_origin_diff:
                    max_origin_diff = origin_diff
        print(f"t: {t} max_diff: {max_diff} max_origin_diff: {max_origin_diff}")
        # print(
        #     f"t: {t} nodes[0].alpha_hat: {nodes[1].alpha_hat} nodes[0].beta_hat: {nodes[1].beta_hat}")
        # print("----------------")
        # print("")

        for i in range(NODE_NUM):
            nodes[i].update_time(t)
        for i in range(NODE_NUM):
            nodes[i].update_send()
        for i in range(NODE_NUM):
            nodes[i].update_prediction()
