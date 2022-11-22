from node.base import PredictNode


class AtsNode(PredictNode):
    def is_send(self) -> bool:
        # send always
        print(f"\t[send] {self.id} -> connect Node")
        return True
