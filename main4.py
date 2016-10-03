import matplotlib.pyplot as plt

plt.figure()
plt.subplot(2, 1, 1)
x = list(range(1000))
y1 = list(range(1000))
y2 = list(range(1000))

c1=0.0
c2=0.0

for i in x:
    val=[0.0, 1.0][i%20==0 and i<800]
    c1+=val
    c2=(c2*500+val)/501
    y1[i]=c1
    y2[i]=c2*1000

plt.plot(x, y1)
plt.subplot(2, 1, 2)
plt.plot(x, y2)

plt.show()