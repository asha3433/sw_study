import cv2
import numpy as np
import os

# Parameters for drawing
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates of the region

# List to store segmentation points
annotations = []

# Mouse callback function to draw contours
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # Start a new contour

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Add points to the current contour
            annotations[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Close the contour by connecting the last point to the first
        annotations[-1].append((x, y))

# Function to display the image and collect annotations
def segment_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found: {image_path}")
        return False  # Return False if the image could not be read

    # Create a clone of the image for annotation display
    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    cv2.setMouseCallback("Image Segmentation", draw_contour)

    while True:
        # Show the annotations on the cloned image
        temp_image = annotated_image.copy()
        for contour in annotations:
            points = np.array(contour, dtype=np.int32)
            cv2.polylines(temp_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        # Display the image with annotations
        cv2.imshow("Image Segmentation", temp_image)
        
        # Press 's' to save annotations, 'c' to clear, and 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            # Save annotations
            with open("annotations.txt", "a") as f:  # Append mode for multiple images
                f.write(f"Annotations for {os.path.basename(image_path)}:\n")
                for contour in annotations:
                    f.write(str(contour) + "\n")
            print(f"Annotations saved for {image_path}")
        elif key == ord("c"):
            # Clear annotations
            annotations.clear()
            annotated_image = image.copy()
            print("Annotations cleared")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()
    return True  # Return True when finished

# Function to process all images in a folder
def process_images_in_folder(folder_path):
    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'tiff'))]
    image_files.sort()  # Optional: sort images alphabetically or by name

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"Processing {image_file}...")
        if not segment_image(image_path):
            print(f"Skipping {image_file} due to an error.")
        else:
            print(f"Finished processing {image_file}.\n")

# Example usage
if __name__ == "__main__":
    PathNames = r"C:\Users\cic\Documents\sw_study\Image_dataset"
    process_images_in_folder(PathNames)
