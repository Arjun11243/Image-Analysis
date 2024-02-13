import cv2
import fitz  # PyMuPDF
from PIL import Image
import os
import numpy as np

def crop_and_save_face(image, face_coordinates, output_path):
    x, y, w, h = face_coordinates
    cropped_face = image[y:y+h, x:x+w]
    cv2.imwrite(output_path, cropped_face)

def detect_faces_in_pdf(pdf_path):
    face_cascade = cv2.CascadeClassifier("frontalface-default.xml")

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        # Extract the current page
        pdf_page = pdf_document[page_number]

        # Convert the PDF page to an image (Pillow format)
        img_pixmap = pdf_page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img = Image.frombytes("RGB", [img_pixmap.width, img_pixmap.height], img_pixmap.samples)

        # Convert the image to OpenCV format
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Convert the image to grayscale
        img_gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img_cv2, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Crop and save the detected face
            output_path = f"face_page_{page_number + 1}.jpg"
            crop_and_save_face(img_cv2, (x, y, w, h), output_path)

        # Resize the image for display
        resized_img = cv2.resize(img_cv2, (800, 600))  # Adjust the size as needed

        # Display the result
        cv2.imshow(f"Page {page_number + 1}", resized_img)
        cv2.waitKey(0)

    # Close the PDF document
    pdf_document.close()
    cv2.destroyAllWindows()

# Example usage
pdf_path = "adhaar.pdf"
detect_faces_in_pdf(pdf_path)