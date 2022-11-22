import matplotlib.pyplot as plt
import numpy as np


def diff_plot(datas: list[list[float]], dT: float, filename="diff.png"):
    fig = plt.figure()
    for i, data in enumerate(datas):
        plt.plot(np.arange(0, len(data) * dT, dT),
                 data, label=f"diff{i}", lw=0.5)

    fig.savefig(filename)
