import os
import shutil
import cv2

# create a directory to store the frames
def manage_directory(dir_path):
    if os.path.exists(dir_path):
        # Remove all files in the directory
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
    else:
        # Create the directory if it does not exist
        os.makedirs(dir_path)


# save the frame in x and y coordinates
def generate_2d_map(x_coord,y_coord,frame):

    frame_path = f"statics/frames/frame_{x_coord}_{y_coord}.jpg"
    #print(frame)
    try:
        cv2.imwrite(frame_path, frame)
    except:
        pass
def detect_turn():
    # compare last 5 frames. if the frames are similar with minimal change then there is no turn.
    # if the frames are different then there is a turn.


    return 1