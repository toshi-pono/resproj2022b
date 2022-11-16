import random
from typing import TypedDict, Callable
Pa: float = 0.1
Pb: float = 0.1


class Data(TypedDict):
    id: int
    alpha_hat: float
    beta_hat: float
    time: float
    updated_at: float


class AtsNode:
    last_datas: dict[int, Data] = {}
    drift_rates: dict[int, float] = {}
    id: int
    alpha: float
    beta: float
    alpha_hat: float
    beta_hat: float
    node_time: float
    send: Callable[[int, Data], None]

    def __init__(self, id: int, alpha: float, beta: float):
        self.id = id
        self.alpha = alpha
        self.beta = beta
        self.alpha_hat = 1.0
        self.beta_hat = 0.0
        self.node_time = 0.0

        self.last_datas[self.id] = self.get_node_data()
        self.drift_rates[self.id] = 1.0

    def get_node_data(self) -> Data:
        return {
            'id': self.id,
            'alpha_hat': self.alpha_hat,
            'beta_hat': self.beta_hat,
            'time': self.node_time,
            'updated_at': -1,  # -1 means not updated
        }

    def get_node_time(self, t: float) -> float:
        return self.alpha * t + self.beta

    def get_predict_time(self, t: float) -> float:
        return self.alpha_hat * self.get_node_time(t) + self.beta_hat

    def is_send(self) -> bool:
        # Send always
        return True

    def recieve(self, data: Data):
        print(
            f'\tid={data["id"]}: recieve: alpha_hat={data["alpha_hat"]:.3g}, beta_hat={data["beta_hat"]:.3g}, time={data["time"]:.3g}')
        sender_id = data['id']
        if self.last_datas.get(sender_id) is None:
            self.drift_rates[sender_id] = 1.0
        else:
            self.drift_rates[sender_id] = (data['time'] - self.last_datas[sender_id]['time']) / (
                self.node_time - self.last_datas[sender_id]['updated_at'])

        data['updated_at'] = self.node_time
        self.last_datas[data['id']] = data

    def update(self):
        if self.is_send():
            self.send(self.id, self.get_node_data())

        # Update prediction
        for data in self.last_datas.values():
            self.alpha_hat += Pa * \
                (self.drift_rates.get(data['id'], 1.0) * data['alpha_hat'] -
                 self.last_datas[self.id]['alpha_hat'])
            self.beta_hat += Pb * (data['alpha_hat'] * data['time'] + data['beta_hat'] - (
                self.last_datas[self.id]['alpha_hat'] * self.last_datas[self.id]['time'] + self.last_datas[self.id]['beta_hat']))

        self.last_datas[self.id] = self.get_node_data()

    def update_time(self, t: float):
        self.node_time = self.get_node_time(t)


# main
def connect_node(matrix: list[list[bool]], id1: int, id2: int):
    matrix[id1][id2] = True
    matrix[id2][id1] = True


def generate_sendfunc(nodes: list[AtsNode], matrix: list[list[int]]) -> Callable[[int, Data], None]:
    def broadcast(sender_id: int, data: Data) -> None:
        for target_id in range(len(nodes)):
            if matrix[sender_id][target_id] == 1:
                nodes[target_id].recieve(data)
    return broadcast


# とりあえず2個で
NODE_NUM = 2
if __name__ == "__main__":
    random.seed(42)

    # Create the network
    connection_matrix: list[list[bool]] = [
        [False for x in range(NODE_NUM)] for y in range(NODE_NUM)]
    connect_node(connection_matrix, 0, 1)

    # Create the nodes
    nodes: list[AtsNode] = []
    for i in range(NODE_NUM):
        nodes.append(AtsNode(id=i, alpha=random.uniform(
            0.9, 1.1), beta=random.uniform(-0.5, 0.5)))
    for i in range(NODE_NUM):
        nodes[i].send = generate_sendfunc(nodes, connection_matrix)

    # Run the simulation
    for t in range(50):
        print(
            f't={t}, diff={nodes[0].get_predict_time(t) - nodes[1].get_predict_time(t):.3g}, origin={nodes[0].get_node_time(t) - nodes[1].get_node_time(t):.3g}')

        for i in range(NODE_NUM):
            nodes[i].update_time(t)
        for i in range(NODE_NUM):
            nodes[i].update()
