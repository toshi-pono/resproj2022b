import matplotlib.pyplot as plt
import numpy as np


def diff_plot(datas: list[list[float]], dT: float, filename: str, title: str = "", xlabel: str = "", ylabel: str = "", ylim: tuple[float, float] | None = None):
    fig = plt.figure()
    if ylim is not None:
        plt.ylim(ylim)
    if title != "":
        plt.title(title)
    if xlabel != "":
        plt.xlabel(xlabel)
    if ylabel != "":
        plt.ylabel(ylabel)
    for i, data in enumerate(datas):
        plt.plot(np.arange(0, len(data) * dT, dT),
                 data, label=f"diff{i}", lw=0.5)

    fig.savefig(filename)


def send_timing_plot(datas: list[list[float]], dT: float, filename: str, title: str = "", xlabel: str = "", ylabel: str = ""):
    fig = plt.figure()
    if title != "":
        plt.title(title)
    if xlabel != "":
        plt.xlabel(xlabel)
    if ylabel != "":
        plt.ylabel(ylabel)
    for i, data in enumerate(datas):
        plt.plot(data, [i+1] * len(data), "D",
                 label=f"node{i}", markersize=2)

    fig.savefig(filename)
