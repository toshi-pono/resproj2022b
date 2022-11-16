from typing import Callable
from node.base import PredictNode, Data
from node.connection import ConnectionMatrix


def generate_broadcast(nodes: list[PredictNode], matrix: ConnectionMatrix) -> Callable[[int, Data], None]:
    def broadcast(sender_id: int, data: Data) -> None:
        for target_id in range(len(nodes)):
            if matrix[sender_id][target_id] == 1:
                nodes[target_id].recieve(data)
    return broadcast
