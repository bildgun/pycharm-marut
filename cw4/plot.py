import matplotlib.pyplot as plt
import numpy as np

# xpoints = np.array([1,4])
# ypoints = np.array([-2,30])
# p3 = np.array([3,8,1,0])
# colors = np.array([0, 20.05, 80, 100])
# font1 = {'family':'serif','color':'blue','size':20}
# font2 = {'family':'serif','color':'darkred','size':15}
# plt.subplot(1,2,1)
# plt.plot(xpoints,ypoints, 'D--c',ms=5, lw=10)
# plt.title("....", fontdict = font1)
# plt.xlabel("Vr0000emya", fontdict = font2)
# plt.ylabel("Kolichestwo", fontdict = font2)
# plt.scatter(p3,p3, c=colors, cmap="winter_r")
# plt.colorbar()
# plt.grid(color='green', lw = 0.2)
# plt.subplot(1,2,2)
# plt.plot(xpoints,ypoints, 'D--c',ms=5, lw=10)
# plt.suptitle("Wykresy Dwa")
# plt.show()

#sin-cos
x1 = np.linspace(-2*np.pi,2*np.pi,100)
ysin = np.sin(x1)
ycos = np.cos(x1)
#kółkowy
x2 = np.random.rand(5)
x2*=100
expl = np.random.rand(5)/5
#słupkowy
x3 = np.array(['A','B','C','D'])
y3 = np.random.rand(4)*100

#Punktowy
x = np.random.normal(0,0.1,1000)
y = np.random.normal(0,0.1,1000)

plt.subplot(2,2,1)
plt.plot(x1,ysin,'r')
plt.plot(x1,ycos,'g')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("SIN/COS")

plt.subplot(2,2,2)
plt.pie(x2, labels=['A','B','C','D','E'],explode=expl)
plt.title("Wykres Kółkowy")

plt.subplot(2,2,3)
plt.bar(x3,y3)

plt.subplot(2,2,4)
plt.scatter(x,y)

plt.show()