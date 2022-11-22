import enum
from node.base import PredictNode
from node.extendAts import AtsNode
from node.extendDrift import DriftDrivenNode
from node.extendTimes import TimeDrivenNode


class ExtendNodeType(enum.Enum):
    ATS = 'ats'
    DRIFT = 'drift'
    TIMES = 'times'

    @classmethod
    def value_of(cls, value: str) -> 'ExtendNodeType':
        for node_type in cls:
            if node_type.value == value:
                return node_type
        raise ValueError(f"Invalid value: {value}")


def generate_extend_node(node_type: ExtendNodeType, id: int, alpha: float, beta: float, Pa: float, Pb: float, debug: bool = False) -> PredictNode:
    if node_type == ExtendNodeType.ATS:
        return AtsNode(id=id, alpha=alpha, beta=beta, Pa=Pa, Pb=Pb, debug=debug)
    elif node_type == ExtendNodeType.DRIFT:
        return DriftDrivenNode(id=id, alpha=alpha, beta=beta, Pa=Pa, Pb=Pb, debug=debug)
    elif node_type == ExtendNodeType.TIMES:
        return TimeDrivenNode(id=id, alpha=alpha, beta=beta, Pa=Pa, Pb=Pb, debug=debug)
    else:
        raise ValueError(f"Invalid node type: {node_type}")
