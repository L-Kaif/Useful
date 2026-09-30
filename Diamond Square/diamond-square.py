import numpy as np
import random
import matplotlib.pyplot as plt

def diamond_square(size, roughness=0.8):
    if size % 2 == 0:
        raise ValueError("Size must be odd")

    grid = np.zeros((size, size))
    step = size - 1

    grid[0, 0] = random.random()
    grid[0, step] = random.random()
    grid[step, 0] = random.random()
    grid[step, step] = random.random()

    while step > 1:
        half = step // 2

        # Diamond step
        for x in range(0, size - 1, step):
            for y in range(0, size - 1, step):
                corners = [grid[x, y], grid[x + step, y], grid[x, y + step], grid[x + step, y + step]]
                avg = np.mean(corners)
                grid[x + half, y + half] = avg + (np.random.rand() - 0.5) * roughness

        # Square step
        for x in range(0, size, half):
            for y in range((x + half) % step, size, step):
                neighbors = []
                if x - half >= 0: neighbors.append(grid[x - half, y])
                if x + half < size: neighbors.append(grid[x + half, y])
                if y - half >= 0: neighbors.append(grid[x, y - half])
                if y + half < size: neighbors.append(grid[x, y + half])
                grid[x, y] = np.mean(neighbors) + (np.random.rand() - 0.5) * roughness

        step //= 2
        roughness *= 0.5

    grid -= grid.min()
    grid /= grid.max()
    return grid



# --- Generate heightmap ---
heightmap = diamond_square(129)

# --- Create coordinate mesh ---
x = np.arange(heightmap.shape[0])
y = np.arange(heightmap.shape[1])
x, y = np.meshgrid(x, y)

# --- Create side-by-side plots ---
fig = plt.figure(figsize=(12, 6))

# Left: 2D heightmap
ax1 = fig.add_subplot(1, 2, 1)
im = ax1.imshow(heightmap, cmap='terrain', origin='lower')
ax1.set_title("2D Heightmap")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04, label='Height')

# Right: 3D terrain surface
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(x, y, heightmap, cmap='terrain', linewidth=0, antialiased=False)
ax2.set_title("3D Mountain Terrain")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Height")

plt.tight_layout()
plt.show()

