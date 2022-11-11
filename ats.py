class AtsNode:
    alpha = 0
    beta = 0
    alpha_hat = 0
    beta_hat = 0
    last_alphas = {}
    last_betas = {}
    id = 0

    def __init__(self, id, alpha, beta):
        self.id = id
        self.alpha = alpha
        self.beta = beta
    
    def getNodeTime(self, t):
        return self.alpha * t + self.beta
    
    def getPredictTime(self, t):
        return self.alpha_hat * self.getNodeTime(t) + self.beta_hat

    def is_send(self, t):
        # Send always
        return True




# main
import random

def connect_node(matrix, id1, id2):
    matrix[id1][id2] = 1
    matrix[id2][id1] = 1

# とりあえず2個で
NODE_NUM = 2
if __name__ == "__main__":
    # Create the nodes
    random.seed(42)
    nodes = []
    for i in range(NODE_NUM):
        nodes.append(AtsNode(i, random.uniform(0.9, 1.1), random.uniform(-0.5, 0.5)))
    
    # Create the network 
    connectionMatrix = [[0 for x in range(NODE_NUM)] for y in range(NODE_NUM)]
    connect_node(connectionMatrix, 0, 1)

    # Run the simulation
    for t in range(50):
        for i in range(NODE_NUM):
