import random
Pa = 0.01
Pb = 0.01


class AtsNode:
    last_alphas = {}
    last_betas = {}
    last_times = {}
    id = 0

    def __init__(self, id, alpha, beta):
        self.id = id
        self.alpha = alpha
        self.beta = beta
        self.alpha_hat = 1
        self.beta_hat = 0

        self.last_alphas[id] = 0
        self.last_betas[id] = 0
        self.last_times[id] = 0

    def getNodeTime(self, t):
        return self.alpha * t + self.beta

    def getPredictTime(self, t):
        return self.alpha_hat * self.getNodeTime(t) + self.beta_hat

    def is_send(self, t):
        # Send always
        return True

    def recieve(self, id, alpha, beta, time):
        print(f'\t{id=}: recieve: {alpha=:.3g}, {beta=:.3g}, {time=:.3g}')
        self.last_alphas[id] = alpha
        self.last_betas[id] = beta
        self.last_times[id] = time

    def update(self, t, rate):
        if self.is_send(t):
            self.send(self.id, self.getNodeTime(t))

        # Update prediction
        for key in self.last_alphas:
            self.alpha_hat += Pa * \
                (rate * self.last_alphas[key] - self.last_alphas[self.id])
            self.beta_hat += Pb * (self.last_alphas[key] * self.last_times[key] + self.last_betas[key] - (
                self.last_alphas[self.id] * self.last_times[self.id] + self.last_betas[self.id]))

        self.last_alphas[self.id] = self.alpha_hat
        self.last_betas[self.id] = self.beta_hat
        self.last_times[self.id] = self.getNodeTime(t)


# main
def connect_node(matrix, id1, id2):
    matrix[id1][id2] = 1
    matrix[id2][id1] = 1


def generateSendFunc(nodes, matrix):
    def send(id, nodeTime):
        for i in range(len(nodes)):
            if matrix[id][i] == 1:
                nodes[i].recieve(id, nodes[id].alpha_hat,
                                 nodes[id].beta_hat, nodeTime)
    return send


# とりあえず2個で
NODE_NUM = 2
if __name__ == "__main__":
    random.seed(42)

    # Create the network
    connectionMatrix = [[0 for x in range(NODE_NUM)] for y in range(NODE_NUM)]
    connect_node(connectionMatrix, 0, 1)

    # Create the nodes
    nodes = []
    for i in range(NODE_NUM):
        nodes.append(AtsNode(id=i, alpha=random.uniform(
            0.9, 1.1), beta=random.uniform(-0.5, 0.5)))

    for i in range(NODE_NUM):
        nodes[i].send = generateSendFunc(nodes, connectionMatrix)

    # Run the simulation
    for t in range(50):
        print(
            f't={t}, diff={nodes[0].getPredictTime(t) - nodes[1].getPredictTime(t):.3g}, origin={nodes[0].getNodeTime(t) - nodes[1].getNodeTime(t):.3g}')
        for i in range(NODE_NUM):
            nodes[i].update(t, nodes[1-i].alpha / nodes[i].alpha)
        # print(
        #     f't={t}, diff={nodes[0].getPredictTime(t) - nodes[1].getNodeTime(t):.3g}, origin={nodes[0].getPredictTime(t) - nodes[1].getNodeTime(t):.3g}')
