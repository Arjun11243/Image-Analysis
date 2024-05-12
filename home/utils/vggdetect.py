import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
from django.conf import settings
import os

facetracker = load_model('../model/facetracker10.h5')


def detect_and_save_face(image_path):
    # Load the facetracker model
    # model_path = os.path.join(settings.BASE_DIR,'home', 'utils','model', 'facetracker10.h5')

    # facetracker = load_model('/model/facetracker10.h5')

    # Load the test image
    test_img_resized = cv2.imread(image_path)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(test_img_resized, cv2.COLOR_BGR2RGB)

    # Resize the image to (120, 120) using TensorFlow
    resized = tf.image.resize(rgb, (120, 120))

    # Predict bounding box coordinates using the facetracker model
    yhat = facetracker.predict(np.expand_dims(resized / 255, 0))
    x_center, y_center, width, height = yhat[1][0]

    # Convert YOLO format coordinates to pixel coordinates
    img_height, img_width, _ = test_img_resized.shape
    x_min = int((x_center - width / 2) * img_width)
    y_min = int((y_center - height / 2) * img_height)
    x_max = int((x_center + width / 2) * img_width)
    y_max = int((y_center + height / 2) * img_height)

    # Crop the face from the original image
    cropped_face = test_img_resized[y_min:y_max, x_min:x_max]

    return cropped_face


# import cv2
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model

# facetracker = load_model('facetracker10.h5')

# test_img = 'Pro.jpg'

# # Load the test image
# test_img_resized = cv2.imread(test_img)

# # Convert BGR to RGB
# rgb = cv2.cvtColor(test_img_resized, cv2.COLOR_BGR2RGB)

# # Resize the image to (120, 120) using TensorFlow
# resized = tf.image.resize(rgb, (120, 120))

# # Predict bounding box coordinates using the facetracker model
# yhat = facetracker.predict(np.expand_dims(resized / 255, 0))
# x_center, y_center, width, height = yhat[1][0]

# # Convert YOLO format coordinates to pixel coordinates
# img_height, img_width, _ = test_img_resized.shape
# x_min = int((x_center - width / 2) * img_width)
# y_min = int((y_center - height / 2) * img_height)
# x_max = int((x_center + width / 2) * img_width)
# y_max = int((y_center + height / 2) * img_height)

# # Crop the face from the original image
# cropped_face = test_img_resized[y_min:y_max, x_min:x_max]

# # Save the cropped face as a new image
# output_path = 'cropped_face.jpg'
# cv2.imwrite(output_path, cropped_face)

# # Display the cropped face
# cv2.imshow('Cropped Face', cropped_face)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



