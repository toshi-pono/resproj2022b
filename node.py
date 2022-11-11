class BaseNode:
    alpha = 0
    beta = 0

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
    
    def getTime(self, t):
        return self.alpha * t + self.beta


class PredictNode:
    alpha_hat = 0
    beta_hat = 0

    def __init__(self, alpha, beta):
        self.node = BaseNode(alpha, beta)

    def getTime(self, t):
        return self.node.getTime(t)
    
    def predictTime(self, t):
        return self.alpha_hat * self.getTime(t) + self.beta_hat