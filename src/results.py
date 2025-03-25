import matplotlib.pyplot as plt

def latency_graph(data):
    plt.plot(data)
    plt.title("Latency Over Iterations")
    plt.xlabel("Iteration #")
    plt.ylabel("Time (s)")
    plt.grid(True)
    plt.savefig('data.png')