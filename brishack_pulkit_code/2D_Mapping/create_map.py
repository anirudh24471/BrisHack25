import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim

def load_images_from_folder(folder, num_frames=5):
    """
    Load the latest num_frames from the given folder.
    If there are fewer than num_frames, return "No turn detected".
    """
    images = []
    sorted_files = sorted(os.listdir(folder), reverse=True)  # Sort files by last modified
    #print(sorted_files)
    # Check if there are enough frames
    if len(sorted_files) < num_frames:
        #print("Not enough frames available. Assuming no turn.")
        return []
    else:
        # Load the latest num_frames images
        for i in range(num_frames):
            file_path = os.path.join(folder, sorted_files[i])
            img = cv2.imread(file_path)
            if img is not None:
                images.append(img)
            #print(f"Loaded frame {i+1}: {file_path}")
        return images


def compare_images(image1, image2):
    """
    Compare two images using SSIM and return the similarity score.
    """
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM between two images
    score, _ = ssim(gray1, gray2, full=True)
    return score

def check_for_turn(images, threshold=0.85):
    """
    Check if the last five frames are similar. If similarity is high, no turn occurred.
    If the similarity score is low, a turn may have occurred.
    """
    if len(images) < 5:
        return 0
    for i in range(len(images) - 1):
        similarity = compare_images(images[i], images[i + 1])
        #print(f"SSIM between frame {i+1} and frame {i+2}: {similarity}")
        
        # If similarity score is below the threshold, return True (turn detected)
        if similarity < threshold:
            return 1
    
    return 0

