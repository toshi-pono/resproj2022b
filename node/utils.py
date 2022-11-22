from node.base import PredictNode


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
