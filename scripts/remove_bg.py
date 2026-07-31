import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

SRC = "public/assets/images/logo-wide.jpg"
DST = "public/assets/images/logo-wide.png"

img = Image.open(SRC).convert("RGB")
arr = np.array(img, dtype=np.int16)
h, w, _ = arr.shape

min_channel = arr.min(axis=2)
# Loose threshold bridges JPEG noise/antialiasing near the white background.
bg_candidate = min_channel >= 215

visited = np.zeros((h, w), dtype=bool)
q = deque()

for x in range(w):
    for y in (0, h - 1):
        if bg_candidate[y, x] and not visited[y, x]:
            visited[y, x] = True
            q.append((x, y))
for y in range(h):
    for x in (0, w - 1):
        if bg_candidate[y, x] and not visited[y, x]:
            visited[y, x] = True
            q.append((x, y))

while q:
    x, y = q.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx] and bg_candidate[ny, nx]:
            visited[ny, nx] = True
            q.append((nx, ny))

alpha = np.where(visited, 0, 255).astype(np.uint8)
alpha_img = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(0.6))

rgba = img.convert("RGBA")
rgba.putalpha(alpha_img)
rgba.save(DST)
print("saved", DST, rgba.size)
