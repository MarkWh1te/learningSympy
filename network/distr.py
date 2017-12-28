import random
import matplotlib.pyplot as plt

normSamples = [random.normalvariate(9.0, 2.0) for i in range(100000)]
print(normSamples[0:10])  #Take a look at the first 10
fig, axis = plt.subplots()
axis.hist(normSamples, bins=100, normed=True)
axis.set_title(r"Histogram of an Normal RNG $\mu = 9$ and $\sigma = 2$")
axis.set_xlabel("x")
axis.set_ylabel("normalized frequency of occurrence")
plt.show()
