import random
import math
import numpy as np

from node import connection
from node.send import generate_broadcast
from node.base import PredictNode
from node.extend import generate_extend_node, ExtendNodeType
from graph import draw

# モデルのパラメータ
Pa: float = 0.1
Pb: float = 0.1
ALPHA_ERROR = 0.1
BETA_ERROR = 0.5

SEED = 42
NODE_TYPE: ExtendNodeType = ExtendNodeType.DRIFT
MAX_TIME = 50.0
dT = 0.1
SYCLE_TIME = math.ceil(MAX_TIME / dT)

OUTPUT_DIR = "output"


def generate_nodes() -> list[PredictNode]:
    # ノードの接続情報読み込み
    connection_matrix, NODE_NUM = connection.load_connection_matrix(
        "testcase/connection3.txt")

    # ノードを生成する
    nodes: list[PredictNode] = []
    for i in range(NODE_NUM):
        alpha = random.uniform(1.0-ALPHA_ERROR, 1.0 + ALPHA_ERROR)
        beta = random.uniform(0.0-BETA_ERROR, 0.0 + BETA_ERROR)
        nodes.append(generate_extend_node(
            NODE_TYPE, i, alpha, beta, Pa, Pb))
    for i in range(NODE_NUM):
        nodes[i].send = generate_broadcast(nodes, connection_matrix)

    return nodes


def calc_diff(nodes: list[PredictNode], time: float) -> list[float]:
    diff_list: list[float] = []
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i == j:
                continue
            diff_list.append(nodes[i].get_predict_time(
                time) - nodes[j].get_predict_time(time))
    return diff_list


def calc_origin_diff(nodes: list[PredictNode], time: float) -> list[float]:
    diff_list: list[float] = []
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i == j:
                continue
            diff_list.append(nodes[i].get_node_time(
                time) - nodes[j].get_node_time(time))
    return diff_list


def main():
    random.seed(SEED)
    nodes = generate_nodes()
    NODE_NUM = len(nodes)

    # Run the simulation
    diff_list: list[list[float]] = []
    alpha_list: list[list[float]] = [[] for _ in range(NODE_NUM)]
    beta_list: list[list[float]] = [[] for _ in range(NODE_NUM)]
    for t in np.arange(0, MAX_TIME, dT):
        # diffを計算する
        diff = calc_diff(nodes, t)
        origin_diff = calc_origin_diff(nodes, t)
        max_diff = max(np.abs(diff))
        max_origin_diff = max(np.abs(origin_diff))
        diff_list.append(diff)

        for i in range(NODE_NUM):
            alpha_list[i].append(nodes[i].alpha_hat)
            beta_list[i].append(nodes[i].beta_hat)
        print("----------------")
        print(f"t: {t} max_diff: {max_diff} max_origin_diff: {max_origin_diff}")

        for i in range(NODE_NUM):
            nodes[i].update_time(t)
        for i in range(NODE_NUM):
            nodes[i].update_send()
        for i in range(NODE_NUM):
            nodes[i].update_prediction()
        print("")

    print("")
    for i in range(NODE_NUM):
        print(
            f"node {i} alpha_hat: {nodes[i].alpha_hat} beta_hat: {nodes[i].beta_hat} send_counter: {nodes[i].send_counter} predict_time: {nodes[i].get_predict_time(MAX_TIME)}")

    diff_list = np.array(diff_list).T.tolist()
    draw.diff_plot(diff_list, dT, f'{OUTPUT_DIR}/{NODE_TYPE.value}_diff.png')
    draw.diff_plot(alpha_list, dT, f'{OUTPUT_DIR}/{NODE_TYPE.value}_alpha.png')
    draw.diff_plot(beta_list, dT, f'{OUTPUT_DIR}/{NODE_TYPE.value}_beta.png')


if __name__ == "__main__":
    main()
