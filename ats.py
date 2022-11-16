import random
from typing import TypedDict
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
    id: int = 0

    def __init__(self, id: int, alpha: float, beta: float):
        self.id = id
        self.alpha = alpha
        self.beta = beta
        self.alpha_hat = 1.0
        self.beta_hat = 0.0
        self.node_time = 0.0

        self.last_datas[self.id] = self.get_node_data()

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
        data['updated_at'] = self.node_time
        self.last_datas[data['id']] = data

    def update(self):
        if self.is_send():
            self.send(self.id)

        # Update prediction
        for data in self.last_datas.values():
            self.alpha_hat += Pa * \
                (data['alpha_hat'] - self.last_datas[self.id]['alpha_hat'])
            self.beta_hat += Pb * (data['alpha_hat'] * data['time'] + data['beta_hat'] - (
                self.last_datas[self.id]['alpha_hat'] * self.last_datas[self.id]['time'] + self.last_datas[self.id]['beta_hat']))

        self.last_datas[self.id] = self.get_node_data()

    def update_time(self, t: float):
        self.node_time = self.get_node_time(t)


# main
def connect_node(matrix, id1, id2):
    matrix[id1][id2] = 1
    matrix[id2][id1] = 1


def generate_sendfunc(nodes, matrix):
    def send(sender_id):
        for target_id in range(len(nodes)):
            if matrix[sender_id][target_id] == 1:
                data: Data = nodes[sender_id].get_node_data()
                nodes[target_id].recieve(data)
    return send


# とりあえず2個で
NODE_NUM = 2
if __name__ == "__main__":
    random.seed(42)

    # Create the network
    connection_matrix = [[0 for x in range(NODE_NUM)] for y in range(NODE_NUM)]
    connect_node(connection_matrix, 0, 1)

    # Create the nodes
    nodes = []
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
