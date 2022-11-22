import random
import numpy as np
from argparse import ArgumentParser

from node import connection
from node.send import generate_broadcast
from node.base import PredictNode
from node.extend import generate_extend_node, ExtendNodeType
import node.utils as utils
from graph import draw

# モデルのパラメータ
Pa: float = 0.2
Pb: float = 0.2
ALPHA_ERROR = 0.1
BETA_ERROR = 0.5

RAND_SEED = 42
NODE_TYPE: ExtendNodeType = ExtendNodeType.ATS
MAX_TIME = 50.0
dT = 0.01

OUTPUT_DIR = "output"
DEBUG = False
CONNECTION_FILE_PATH = "testcase/connection3.txt"


def set_option():
    global RAND_SEED, NODE_TYPE, MAX_TIME, dT, OUTPUT_DIR, DEBUG, CONNECTION_FILE_PATH

    parser = ArgumentParser()
    parser.add_argument("--seed", type=int, default=RAND_SEED)
    parser.add_argument("--node-type", type=str, default=NODE_TYPE.value)
    parser.add_argument("--max-time", type=float, default=MAX_TIME)
    parser.add_argument("--dt", type=float, default=dT)
    parser.add_argument("--output-dir", type=str, default=OUTPUT_DIR)
    parser.add_argument("--debug", action="store_true", default=DEBUG)
    parser.add_argument("--input", type=str, default=CONNECTION_FILE_PATH)

    args = parser.parse_args()
    RAND_SEED = args.seed
    NODE_TYPE = ExtendNodeType(args.node_type)
    MAX_TIME = args.max_time
    dT = args.dt
    OUTPUT_DIR = args.output_dir
    DEBUG = args.debug
    CONNECTION_FILE_PATH = args.input
    return


def generate_nodes() -> list[PredictNode]:
    # ノードの接続情報読み込み
    connection_matrix, NODE_NUM = connection.load_connection_matrix(
        CONNECTION_FILE_PATH)

    # ノードを生成する
    nodes: list[PredictNode] = []
    for i in range(NODE_NUM):
        alpha = random.uniform(1.0-ALPHA_ERROR, 1.0 + ALPHA_ERROR)
        beta = random.uniform(0.0-BETA_ERROR, 0.0 + BETA_ERROR)
        nodes.append(generate_extend_node(
            NODE_TYPE, i, alpha, beta, Pa, Pb, DEBUG))
    for i in range(NODE_NUM):
        nodes[i].send = generate_broadcast(nodes, connection_matrix)

    return nodes


def debug_print(*values):
    if DEBUG:
        print(*values)


def main():
    set_option()
    random.seed(RAND_SEED)
    nodes = generate_nodes()
    NODE_NUM = len(nodes)

    # Run the simulation
    diff_list: list[list[float]] = []
    alpha_list: list[list[float]] = [[] for _ in range(NODE_NUM)]
    beta_list: list[list[float]] = [[] for _ in range(NODE_NUM)]
    for t in np.arange(0, MAX_TIME + dT, dT):
        # diffを計算する
        diff = utils.calc_diff(nodes, t)
        origin_diff = utils.calc_origin_diff(nodes, t)
        max_diff = max(np.abs(diff))
        max_origin_diff = max(np.abs(origin_diff))
        diff_list.append(diff)

        for i in range(NODE_NUM):
            alpha_list[i].append(nodes[i].alpha_hat)
            beta_list[i].append(nodes[i].beta_hat)
        debug_print("----------------")
        debug_print(
            f"t: {t:.4f} max_diff: {max_diff:.4f} max_origin_diff: {max_origin_diff:.4f}")

        for i in range(NODE_NUM):
            nodes[i].update_time(t)
        for i in range(NODE_NUM):
            nodes[i].update()

        debug_print("")

    debug_print("")
    for i in range(NODE_NUM):
        print(
            f"node {i} alpha_hat: {nodes[i].alpha_hat} beta_hat: {nodes[i].beta_hat} send_counter: {nodes[i].send_counter} update_counter: {nodes[i].update_counter} predict_time: {nodes[i].get_predict_time(MAX_TIME)}")

    max_diff = max(np.abs(utils.calc_diff(nodes, MAX_TIME)))
    max_origin_diff = max(np.abs(utils.calc_origin_diff(nodes, MAX_TIME)))
    print(
        f"t: {t:.4f} max_diff: {max_diff} max_origin_diff: {max_origin_diff}")
    diff_list = np.array(diff_list).T.tolist()
    draw.diff_plot(diff_list, dT, f'{OUTPUT_DIR}/{NODE_TYPE.value}_diff.png',
                   xlabel="Time t", ylabel="Synch. Error", ylim=(-1, 1))
    draw.diff_plot(alpha_list, dT, f'{OUTPUT_DIR}/{NODE_TYPE.value}_alpha.png')
    draw.diff_plot(beta_list, dT, f'{OUTPUT_DIR}/{NODE_TYPE.value}_beta.png')


if __name__ == "__main__":
    main()
