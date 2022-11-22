from node.base import PredictNode


class AtsNode(PredictNode):
    def is_send(self) -> bool:
        # send always
        self.debug_print(f"send!")
        return True
