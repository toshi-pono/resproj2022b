import random
import math
import numpy as np
from argparse import ArgumentParser

from node import connection
from node.send import generate_broadcast
from node.base import PredictNode
from node.extend import generate_extend_node, ExtendNodeType
import node.utils as utils
import matplotlib.pyplot as plt

# モデルのパラメータ
Pa: float = 0.2
Pb: float = 0.2
ALPHA_ERROR = 0.1
BETA_ERROR = 0.5

RAND_SEED = 42
NODE_TYPE: ExtendNodeType = ExtendNodeType.ATS
MAX_TIME = 150.0
dT = 0.01

OUTPUT_DIR = "output"
DEBUG = False
CONNECTION_FILE_PATH = "testcase/connection3.txt"


def set_option():
    global RAND_SEED, MAX_TIME, dT, OUTPUT_DIR, DEBUG, CONNECTION_FILE_PATH

    parser = ArgumentParser()
    parser.add_argument("--seed", type=int, default=RAND_SEED)
    parser.add_argument("--max-time", type=float, default=MAX_TIME)
    parser.add_argument("--dt", type=float, default=dT)
    parser.add_argument("--output-dir", type=str, default=OUTPUT_DIR)
    parser.add_argument("--debug", action="store_true", default=DEBUG)
    parser.add_argument("--input", type=str, default=CONNECTION_FILE_PATH)

    args = parser.parse_args()
    RAND_SEED = args.seed
    MAX_TIME = args.max_time
    dT = args.dt
    OUTPUT_DIR = args.output_dir
    DEBUG = args.debug
    CONNECTION_FILE_PATH = args.input
    return


def generate_all_nodes() -> list[tuple[ExtendNodeType, list[PredictNode]]]:
    # ノードの接続情報読み込み
    connection_matrix, NODE_NUM = connection.load_connection_matrix(
        CONNECTION_FILE_PATH)

    # ノードを生成する
    nodes_list: list[tuple[ExtendNodeType, list[PredictNode]]] = []
    for node_type in ExtendNodeType:
        random.seed(RAND_SEED)
        nodes: list[PredictNode] = []
        for i in range(NODE_NUM):
            alpha = random.uniform(1.0-ALPHA_ERROR, 1.0 + ALPHA_ERROR)
            beta = random.uniform(0.0-BETA_ERROR, 0.0 + BETA_ERROR)
            nodes.append(generate_extend_node(
                node_type, i, alpha, beta, Pa, Pb, DEBUG))
        for i in range(NODE_NUM):
            nodes[i].send = generate_broadcast(nodes, connection_matrix)
        nodes_list.append((node_type, nodes.copy()))
    return nodes_list


def debug_print(*values):
    if DEBUG:
        print(*values)


def main():
    set_option()
    nodes_list = generate_all_nodes()
    result_list: list[tuple[ExtendNodeType, list[float], list[float]]] = []

    # Run the simulation
    for nodes_obj in nodes_list:
        nodes = nodes_obj[1]
        max_diff_list = []
        send_count_list = []
        for t in np.arange(0, MAX_TIME + dT, dT):
            # maxdiff
            max_diff = max(np.abs(utils.calc_diff(nodes, t)))
            max_diff_list.append(max_diff)

            # update
            for node in nodes:
                node.update_time(t)
            for node in nodes:
                node.update()

            # send count
            send_count = 0
            for node in nodes:
                send_count += node.send_counter
            send_count_list.append(send_count)

        result_list.append((nodes_obj[0], max_diff_list, send_count_list))

    # Draw graph
    lineStyles = ["solid", "dashed", "dotted"]
    fig = plt.figure()
    plt.yscale("log")
    for i, result in enumerate(result_list):
        plt.plot(np.arange(0, 50 + dT, dT),
                 result[1][:math.floor((50 + dT)/dT)], label=f"{result[0].value}", lw=1, linestyle=lineStyles[i])
    plt.legend()
    fig.savefig(f"{OUTPUT_DIR}/maxdiff.png")

    fig = plt.figure()
    for i, result in enumerate(result_list):
        plt.plot(np.arange(0, MAX_TIME + dT, dT),
                 result[2], label=f"{result[0].value}", lw=1, linestyle=lineStyles[i])
    plt.legend()
    fig.savefig(f"{OUTPUT_DIR}/sendcount.png")


if __name__ == "__main__":
    main()
