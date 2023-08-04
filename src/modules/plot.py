import matplotlib.pyplot as plt

def plot_multi(xlabel, ylabel, ylim, title, bars: dict[str, tuple[float, float]]):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0, ylim)
    plt.title(title)

    for key, value in bars.items():
        plt.bar(key, value[0], width=0.3, align='center', color='blue')
        plt.bar(key, value[1], width=0.3, align='edge', color='red')

    plt.show()
