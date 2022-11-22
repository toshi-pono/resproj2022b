import math
from node.base import PredictNode


class TimeDrivenNode(PredictNode):
    c_beta: float = 0.01
    c_alpha1: float = 0.01
    c_alpha2: float = 0.1

    def is_send(self) -> bool:
        if self.send_counter == 0:
            print(f"\t[send] {self.id} -> connect Node")
            return True
        is_a = abs(self.last_datas[self.id]["alpha_hat"] -
                   self.alpha_hat) > self.c_alpha1 * math.exp(-self.c_alpha2 * self.node_time)
        is_b = abs(self.last_datas[self.id]
                   ["beta_hat"] - self.beta_hat) > self.c_beta
        if is_a or is_b:
            print(f"\t[send] {self.id} -> connect Node")
        return is_a | is_b
