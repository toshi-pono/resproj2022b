from node.base import PredictNode


class DriftDrivenNode(PredictNode):
    c_beta: float = 0.005
    c_alpha1: float = 0.01
    T_o = 10

    def is_send(self) -> bool:
        if self.send_counter == 0:
            self.debug_print(f"send!")
            return True
        if self.node_time - self.before_update > self.T_o:
            self.debug_print(f"send!")
            return True
        is_a = abs(self.last_datas[self.id]
                   ["alpha_hat"] - self.alpha_hat) > self.c_alpha1
        is_b = abs(self.last_datas[self.id]
                   ["beta_hat"] - self.beta_hat) > self.c_beta
        if is_a or is_b:
            self.debug_print(f"send!")
        return is_a | is_b

    def update_alpha_hat(self):
        sum = 0
        for data in self.last_datas.values():
            sum += self.Pa * \
                (self.drift_rates.get(data['id'], 1.0) * data['alpha_hat'] -
                 self.last_datas[self.id]['alpha_hat'])

        self.alpha_hat = self.last_datas[self.id]['alpha_hat'] + sum
