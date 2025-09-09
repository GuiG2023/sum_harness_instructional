import pandas as pd
import matplotlib.pyplot as plt

fname = "mflops_3vars.csv"
df = pd.read_csv(fname, comment="#")

problem_sizes = df[df.columns[0]].values.tolist()
direct = df[df.columns[1]].values.tolist()
vector = df[df.columns[2]].values.tolist()
indirect = df[df.columns[3]].values.tolist()

plt.figure(figsize=(8,5))
plt.title("Problem Size vs MFLOP/s")

plt.plot(problem_sizes, direct, "r-o", label="Direct")
plt.plot(problem_sizes, vector, "b-x", label="Vector")
plt.plot(problem_sizes, indirect, "g-^", label="Indirect")

plt.xscale("log", base=2)
plt.xlabel("Problem Size (N)")
plt.ylabel("MFLOP/s")
plt.grid(True, which="both")
plt.legend(loc="best")

plt.tight_layout()
plt.savefig("mflops_vs_N.png", dpi=300) 
plt.show()  