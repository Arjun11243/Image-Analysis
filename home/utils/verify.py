from deepface import DeepFace

# verification = DeepFace.verify(img1_path = "cropped_face.jpg", model_name=" ",img2_path = "face_page_3.jpg", enforce_detection=False, threshold=0.3)
# print(verification)
def ver(file1,file2):
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    # verification = DeepFace.verify("face_page_2.jpg", "passport.jpg", model_name = models[6])
    # verification = DeepFace.verify("face_page_2.jpg", "face_page_3.jpg", model_name = models[6])
    verification = DeepFace.verify(file1, file2, model_name = models[6])
    # print(verification)
    return verification['verified']

# print(ver("face_page_2.jpg","passport.jpg"))