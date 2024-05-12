import cv2
import fitz  # PyMuPDF
from PIL import Image
import os
import numpy as np
from django.conf import settings

face_cascade = cv2.CascadeClassifier('../model/frontalface-default.xml')


import cv2

def crop_and_save_face_original_size(image, face_coordinates):
    x, y, w, h = face_coordinates

    # Crop the face from the original image without any resizing
    cropped_face = image[y:y+h, x:x+w]

    return cropped_face


def detect_faces_in_image(image_path, confidence_threshold=40):
    # cascade_path = os.path.join(str(settings.BASE_DIR),'home', 'utils','model', 'frontalface-default.xml')


    # Read the image
    img_cv2 = cv2.imread(image_path)

    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces, scores = face_cascade.detectMultiScale2(img_gray, scaleFactor=1.1, minNeighbors=4)

    # Initialize variable to store detected face
    detected_face = None

    # Draw rectangles around the detected faces
    for (x, y, w, h), score in zip(faces, scores):
        cv2.rectangle(img_cv2, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Check if the confidence score is above the threshold
        if score > confidence_threshold:
            # Crop and save the detected face in original size
            detected_face = crop_and_save_face_original_size(img_cv2, (x, y, w, h))
            print(f"Face detected with accuracy: {score}. Face saved.")
            # Break out of loop once a face above the threshold is found
            break

    return detected_face


# def crop_and_save_face_original_size(image, face_coordinates, output_path):
#     x, y, w, h = face_coordinates

#     # Crop the face from the original image without any resizing
#     cropped_face = image[y:y+h, x:x+w]

#     # Save the cropped face
#     cv2.imwrite(output_path, cropped_face)


# def detect_faces_in_image(image_path, confidence_threshold=70):
#     face_cascade = cv2.CascadeClassifier("frontalface-default.xml")

#     # Read the image
#     img_cv2 = cv2.imread(image_path)

#     # Convert the image to grayscale
#     img_gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

#     # Detect faces in the grayscale image
#     faces, scores = face_cascade.detectMultiScale2(img_gray, scaleFactor=1.1, minNeighbors=4)

#     # Draw rectangles around the detected faces
#     for (x, y, w, h), score in zip(faces, scores):
#         cv2.rectangle(img_cv2, (x, y), (x+w, y+h), (255, 0, 0), 2)

#         # Check if the confidence score is above the threshold
#         if score > confidence_threshold:
#             # Crop and save the detected face in original size
#             output_path = f"detected_face_{x}_{y}.jpg"
#             crop_and_save_face_original_size(img_cv2, (x, y, w, h), output_path)
#             print(f"Face detected with accuracy: {score}. Face saved.")

#     # Display the result
#     cv2.imshow("Detected Faces", img_cv2)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# image_path = "adha.jpg"
# detect_faces_in_image(image_path, confidence_threshold=40)