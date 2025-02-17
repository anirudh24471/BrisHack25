import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "area_map.jpeg"
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply threshold to detect the rooms
_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

# Find contours (which correspond to rooms)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw circles at the center of each detected room
output_image = image.copy()
for contour in contours:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.circle(output_image, (cx, cy), 10, (0, 255, 0), -1)  # Green circle

# Convert image from BGR to RGB for displaying
output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

# Display the processed image
plt.figure(figsize=(8, 8))
plt.imshow(output_image)
plt.axis("off")
plt.show()
