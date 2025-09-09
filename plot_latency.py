import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("latency_3vars.csv")

problem_sizes = df["Problem Size"].tolist()
direct = df["Direct"].tolist()
vector = df["Vector"].tolist()
indirect = df["Indirect"].tolist()

plt.figure(figsize=(8,5))
plt.title("Average Memory Access Latency vs Problem Size")


plt.xscale("log", base=2)   


plt.plot(problem_sizes, direct, "r-o", label="Direct")
plt.plot(problem_sizes, vector, "b-x", label="Vector")
plt.plot(problem_sizes, indirect, "g-^", label="Indirect")

plt.xlabel("Problem Size (N)")
plt.ylabel("Latency (ns/access)")
plt.grid(True, which="both")
plt.legend(loc="best")

plt.tight_layout()
plt.savefig("latency_vs_N.png", dpi=300)
plt.show()