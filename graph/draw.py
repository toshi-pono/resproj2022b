import matplotlib.pyplot as plt


def diff_plot(datas: list[list[float]], filename="diff.png"):
    fig = plt.figure()
    for i, data in enumerate(datas):
        plt.plot(list(range(len(data))), data, label=f"diff{i}", lw=0.5)

    fig.savefig(filename)
