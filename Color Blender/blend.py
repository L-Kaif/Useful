import numpy as np
import matplotlib.pyplot as plt

def gradient_panel(n, c1, c2):
    c1, c2 = np.array(c1)/255, np.array(c2)/255
    x = np.linspace(0, 1, n)
    t = (x[:, None] + x[None, :]) / 2  # diagonal blend
    return (1 - t)[..., None]*c1 + t[..., None]*c2

n = 100
cyan, pink = (0,255,255), (255,105,180)
img = gradient_panel(n, cyan, pink)

plt.imshow(img, origin='lower')
plt.axis('off')
plt.show()
