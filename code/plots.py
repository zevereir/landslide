from matplotlib import pyplot as plt
# Data for plotting
t = [0,1,2,3]
s = [0.8,0.81,0.82,0.82]

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='beam size', ylabel='responsivity',
       title='Cutoff 2, learned')
ax.grid()


plt.show()