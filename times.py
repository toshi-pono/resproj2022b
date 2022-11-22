import random
import math
from node import connection
from node.send import generate_broadcast
from node.base import PredictNode
from graph import draw

Pa: float = 0.1
Pb: float = 0.1


class TimeDrivenNode(PredictNode):
    c_beta: float = 0.1
    c_alpha1: float = 0.1
    c_alpha2: float = 0.1

    def is_send(self) -> bool:
        if self.send_counter == 0:
            print(f"\t[send] {self.id} -> connect Node")
            return True
        is_a = abs(self.last_datas[self.id]["alpha_hat"] -
                   self.alpha_hat) > self.c_alpha1 * math.exp(-self.c_alpha2 * self.node_time)
        is_b = abs(self.last_datas[self.id]
                   ["beta_hat"] - self.beta_hat) > self.c_beta
        if is_a or is_b:
            print(f"\t[send] {self.id} -> connect Node")
        return is_a | is_b


if __name__ == "__main__":
    random.seed(42)

    # Create the network
    connection_matrix, NODE_NUM = connection.load_connection_matrix(
        "testcase/connection3.txt")

    # Create the nodes
    nodes: list[TimeDrivenNode] = []
    for i in range(NODE_NUM):
        nodes.append(TimeDrivenNode(id=i, alpha=random.uniform(
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
        print("")

    for i in range(NODE_NUM):
        print(
            f"node {i} alpha_hat: {nodes[i].alpha_hat} beta_hat: {nodes[i].beta_hat} send_counter: {nodes[i].send_counter} predict_time: {nodes[i].get_predict_time(SYCLE_NUM)}")
    draw.diff_plot(diff_list)
    draw.diff_plot(alpha_list, "alpha.png")
    draw.diff_plot(beta_list, "beta.png")
