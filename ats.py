import random
from node import connection
from node.send import generate_broadcast
from node.base import PredictNode
from graph import draw

Pa: float = 0.1
Pb: float = 0.1


class AtsNode(PredictNode):
    def is_send(self) -> bool:
        # send always
        print(f"\t[send] {self.id} -> connect Node")
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
    SYCLE_NUM = 150
    diff_list: list[list[float]] = [[] for _ in range(NODE_NUM*NODE_NUM)]
    alpha_list: list[list[float]] = [[] for _ in range(NODE_NUM)]
    beta_list: list[list[float]] = [[] for _ in range(NODE_NUM)]
    for t in range(SYCLE_NUM):
        # diffを計算する
        max_diff = 0
        max_origin_diff = 0
        for i in range(NODE_NUM):
            for j in range(i, NODE_NUM):
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
                diff_list[i+NODE_NUM*j].append(nodes[i].get_predict_time(
                    t) - nodes[j].get_predict_time(t))
        for i in range(NODE_NUM):
            alpha_list[i].append(nodes[i].alpha_hat)
            beta_list[i].append(nodes[i].beta_hat)
        print("----------------")
        print(f"t: {t} max_diff: {max_diff} max_origin_diff: {max_origin_diff}")

        for i in range(NODE_NUM):
            nodes[i].update_time(t*0.1)
        for i in range(NODE_NUM):
            nodes[i].update_send()
        for i in range(NODE_NUM):
            nodes[i].update_prediction()
        print("")

    print("")
    for i in range(NODE_NUM):
        print(
            f"node {i} alpha_hat: {nodes[i].alpha_hat} beta_hat: {nodes[i].beta_hat} send_counter: {nodes[i].send_counter} predict_time: {nodes[i].get_predict_time(SYCLE_NUM)}")

    print(len(diff_list[0]))
    draw.diff_plot(diff_list)
    draw.diff_plot(alpha_list, "alpha.png")
    draw.diff_plot(beta_list, "beta.png")
