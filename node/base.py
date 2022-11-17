from typing import TypedDict, Callable


class Data(TypedDict):
    id: int
    alpha_hat: float
    beta_hat: float
    time: float
    updated_at: float


class RawNode:
    __alpha: float = 0
    __beta: float = 0

    def __init__(self, alpha: float, beta: float):
        self.__alpha = alpha
        self.__beta = beta

    def get_time(self, t: float) -> float:
        return self.__alpha * t + self.__beta


class PredictNode:
    last_datas: dict[int, Data] = {}
    drift_rates: dict[int, float] = {}
    id: int
    alpha_hat: float
    beta_hat: float
    node_time: float
    send: Callable[[int, Data], None]
    raw_node: RawNode
    send_counter: int = 0

    Pa: float
    Pb: float

    def __init__(self, id: int, alpha: float, beta: float, Pa: float = 0.1, Pb: float = 0.1):
        self.id = id
        self.alpha_hat = 1.0
        self.beta_hat = 0.0
        self.node_time = 0.0
        self.last_datas = {}
        self.drift_rates = {}
        self.raw_node = RawNode(alpha, beta)
        self.Pa = Pa
        self.Pb = Pb

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
        return self.raw_node.get_time(t)

    def get_predict_time(self, t: float) -> float:
        return self.alpha_hat * self.get_node_time(t) + self.beta_hat

    def is_send(self) -> bool:
        # Send always
        return True

    def recieve(self, data: Data):
        sender_id = data['id']
        if self.last_datas.get(sender_id) is None:
            self.drift_rates[sender_id] = 1.0
        else:
            self.drift_rates[sender_id] = (data['time'] - self.last_datas[sender_id]['time']) / (
                self.node_time - self.last_datas[sender_id]['updated_at'])

        data['updated_at'] = self.node_time
        self.last_datas[data['id']] = data

    def update_send(self):
        if self.is_send():
            self.send(self.id, self.get_node_data())
            self.send_counter += 1
            self.last_datas[self.id] = self.get_node_data()

    def update_prediction(self):
        # Update prediction
        self.__update_alpha_hat()
        self.__update_beta_hat()

    def __update_alpha_hat(self):
        for data in self.last_datas.values():
            self.alpha_hat += self.Pa * \
                (self.drift_rates.get(data['id'], 1.0) * data['alpha_hat'] -
                 self.last_datas[self.id]['alpha_hat'])

    def __update_beta_hat(self):
        for data in self.last_datas.values():
            self.beta_hat += self.Pb * (data['alpha_hat'] * data['time'] + data['beta_hat'] - (
                self.last_datas[self.id]['alpha_hat'] * self.last_datas[self.id]['time'] + self.last_datas[self.id]['beta_hat']))

    def update_time(self, t: float):
        self.node_time = self.get_node_time(t)
