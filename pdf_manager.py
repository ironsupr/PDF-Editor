import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pdf2image import convert_from_path
import os
import PyPDF2
# from pdf2jpg import pdf2jpg

def check_rotate(img):
    # Step 1: Read the image
    image = cv2.imread(img)  # Replace with your image path

    # Step 2: Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Step 4: Apply Canny edge detection
    edges = cv2.Canny(blurred_image, threshold1=100, threshold2=200)

    # Step 5: Find lines using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)  # Parameters: image, resolution, angle resolution, threshold

    # Step 6: Calculate the angle of the detected line
    angle = 0  # Default to 0 degrees if no lines are found
    if lines is not None:
        # Calculate the angle of the first line
        for rho, theta in lines[0]:
            angle = theta * 180 / np.pi - 90  # Convert from radians to degrees and normalize
            break  # Use the first detected line for simplicity

        # If the angle is negative, rotate in the opposite direction
        if angle < 0:
            angle += 180  # Normalize to a positive angle

    # Step 7: Check if the image is straight or inverted
    print(f"Detected angle: {angle} degrees")

    # If the angle is greater than 90 degrees, it's likely inverted, rotate by 180 degrees
    if angle > 90:
        print("The image is likely inverted. Rotating by 180 degrees.")
        angle -= 180  # Correct for the inversion by rotating back 180 degrees

    # Step 8: Rotate the image to straighten the edges
    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Calculate the bounding box dimensions after rotation to avoid cutting
    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])

    # Calculate the new width and height
    new_width = int(height * abs_sin + width * abs_cos)
    new_height = int(height * abs_cos + width * abs_sin)

    # Adjust the rotation matrix to account for translation (i.e., to keep the center of the image)
    rotation_matrix[0, 2] += (new_width - width) / 2
    rotation_matrix[1, 2] += (new_height - height) / 2

    # Perform the rotation with the new dimensions
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))

    # Step 9: Display the original and rotated images
    # plt.figure(figsize=(10, 5))

    # # Show original image
    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title('Original Image')
    # plt.axis('off')

    # # Show rotated image
    # plt.subplot(1, 2, 2)
    # plt.imshow(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
    # plt.title('Rotated Image (Straightened)')
    # plt.axis('off')

    # plt.show()

    return rotated_image

def pdf_to_png(pdf_path, output_dir="output"):
    # poppler_path = r"D:\Project\Release-24.07.0-0\poppler-24.07.0\Library\bin"
    i = 1
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_files = [os.path.join(pdf_path, f) for f in os.listdir(pdf_path) if f.lower().endswith('.pdf')]
    print(pdf_files)

    image_paths = []
    
    for pdf_file in pdf_files:
        # Convert PDF to images
        images = convert_from_path(pdf_file)
        print(images)

        for idx, image in enumerate(images):
            # Save each page as an image
            image_path = os.path.join(output_dir, f"{i}_page_{idx + 1}.png")
            image.save(image_path, 'PNG')
            image_paths.append(image_path)
            i+=1
    
    return image_paths

def images_to_pdf(image_dir=r"output", output_pdf="output.pdf"):
    # Get all image files from the directory
    if not os.path.exists(image_dir):
        print(f"Directory '{image_dir}' does not exist.")
        return

    image_paths = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('png', 'jpg', 'jpeg'))]

    
    if not image_paths:
        print("No image files found in the directory.")
        return

    for i in image_paths:
        img = check_rotate(i)
        cv2.imwrite(i, img)

    # Open each image
    images = [Image.open(image_path) for image_path in image_paths]
    print(images)
    
    # Convert images to RGB if they are in other formats like PNG (RGBA)
    images = [img.convert('RGB') for img in images]
    
    # Save the images as a single PDF
    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    print(f"PDF saved as {output_pdf}")

images_to_pdf("Images")