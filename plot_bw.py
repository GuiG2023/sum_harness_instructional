import pandas as pd
import matplotlib.pyplot as plt

# %
df = pd.read_csv("bw_util_3vars.csv")

sizes   = df.iloc[:,0].tolist()
direct  = df.iloc[:,1].tolist()
vector  = df.iloc[:,2].tolist()
indirect= df.iloc[:,3].tolist()

plt.figure(figsize=(9,5))
plt.title("Problem Size vs Memory Bandwidth Utilization (%)")
plt.plot(direct,  "r-o", label="Direct")
plt.plot(vector,  "b-x", label="Vector")
plt.plot(indirect,"g-^", label="Indirect")


plt.xticks(range(len(sizes)), [f"{s}" for s in sizes])
plt.xlabel("Problem Size (N)")
plt.ylabel("Utilization (%)")
plt.ylim(0, 3)               
plt.grid(True, which="both", axis="both")
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("bw_utilization.png", dpi=300)
plt.show()