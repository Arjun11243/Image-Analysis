from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .utils import verify
from .utils import facedettimeg2
from .utils import vggdetect
from .utils import sample6
from .utils import extract
import os,cv2
from django.conf import settings
from .models import Aadhaar
from .models import Aadhaar_detail
from datetime import datetime
from django.contrib.auth.decorators import login_required
import requests

API_URL = "https://api-inference.huggingface.co/models/dima806/deepfake_vs_real_image_detection"
headers = {"Authorization": "Bearer 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"}

project_id = "529876974990"
location = "us"
processor_id = "35a86c53df6f4b1"  # Create processor before running sample
processor_version = "f1dece949e79896f"  # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
# file_path = "vp3.jpg"
mime_type = "image/jpeg"
output_file = "entities.txt"


# Create your views here.
def index(request):
    return render(request,'index.html')

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect("authentication")
            else:
                return redirect("upload")  # Redirect to the upload page for non-superusers

    return render(request,'login.html')
# def loginUser(request):
#     if request.method=="POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user= authenticate(username=username,password=password)

#         if user is not None:
#             login(request,user)
#             return redirect("upload")
#         else:
#             return render(request,'login.html')

#     return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        # Retrieve user input from the form
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Create a new user
        new_user = User.objects.create_user(username=username, password=password, email=email)
        # Save the user to the database
        new_user.save()

        return redirect('home')

    return render(request, 'home')





def deepfake_detection(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# JPG FILES UPLOADED

def upload(request):
    result_string = None
    deepfake_result = ""

    if request.method == 'POST' and 'file1' in request.FILES and 'file2' in request.FILES:
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']

        # Check if both uploaded files are JPG
        if file1.content_type == 'image/jpeg' and file2.content_type == 'image/jpeg':
            # Define the folder path where files will be saved
            utils_folder = os.path.join(settings.BASE_DIR, 'home', 'utils')

            # Ensure the folder exists, create it if not
            if not os.path.exists(utils_folder):
                os.makedirs(utils_folder)

            # Define the folder path where files will be saved
            saved_folder = os.path.join(utils_folder, 'saved')
            detected_folder = os.path.join(utils_folder, 'detected')

            # Ensure the "saved" folder exists, create it if not
            if not os.path.exists(saved_folder):
                os.makedirs(saved_folder)
            if not os.path.exists(detected_folder):
                os.makedirs(detected_folder)

            # Generate unique file names
            file1_path = os.path.join(saved_folder, 'file1.jpg')
            # file2_path = os.path.join(saved_folder, 'file2.jpg')
            file2_path = os.path.join(saved_folder, 'webcam_image.jpg')

            # Save the uploaded files to the "saved" folder
            with open(file1_path, 'wb') as destination:
                for chunk in file1.chunks():
                    destination.write(chunk)

            with open(file2_path, 'wb') as destination:
                for chunk in file2.chunks():
                    destination.write(chunk)

            deepfake_result = deepfake_detection(file1_path)

            if deepfake_result and isinstance(deepfake_result, list) and deepfake_result[0].get('label'):
                deepfake_result = deepfake_result[0]['label']
            else:
                deepfake_result = "Detection failed"



            detected_face_path = os.path.join(detected_folder, 'detected_face.jpg')
            detected_face = facedettimeg2.detect_faces_in_image(file1_path, confidence_threshold=40)
            cv2.imwrite(detected_face_path, detected_face)

            # Detect and crop face in the second image and save it in the "detected" folder
            # cropped_face_path = os.path.join(detected_folder, 'cropped_face.jpg')
            # # cropped_face = vggdetect.detect_and_save_face(file2_path)
            # cropped_face = facedettimeg2.detect_faces_in_image(file2_path, confidence_threshold=40)
            # cv2.imwrite(cropped_face_path, cropped_face)


            # Call the function from the external Python file with file paths
            result_string = verify.ver(detected_face_path, file2_path)
            print(result_string,deepfake_result)
        else:
            result_string = "Both files must be JPG images."

    # return render(request, 'upload.html', {'result_string': result_string})
    return render(request, 'upload.html', {'verified': result_string , 'deepfake_result': deepfake_result})







def doc_verify(request):
    result_data = {}

    # Extract Aadhaar details using Document AI
    utils_folder = os.path.join(settings.BASE_DIR, 'home', 'utils')
    saved_folder = os.path.join(utils_folder, 'saved')
    file1_path = os.path.join(saved_folder, 'file1.jpg')


    project_id = "529876974990"
    location = "us"
    processor_id = "35a86c53df6f4b1"  # Create processor before running sample
    processor_version = "f1dece949e79896f"  # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
    mime_type = "image/jpeg"
    output_file = "entities.txt"

    sample6.process_document_entity_extraction_sample(project_id, location, processor_id, processor_version,
                                                      file1_path, mime_type, output_file)

    # Read extracted entities from the output file
    entities_data = extract.read_entities_file(output_file)
    aadhar_number = entities_data.get('Adhaar Number', '')
    aadhaar_data = extract.process_aadhaar_number(entities_data, aadhar_number)

    # Check if Aadhaar details were successfully extracted
    if aadhaar_data:
        # Prepare the dictionary for extracted Aadhaar details
        extracted_aadhaar_details = {
            'Aadhaar Number': aadhaar_data.get('Adhaar Number'),
            'Name': aadhaar_data.get('Name'),
            'Date of Birth': aadhaar_data.get('Date of Birth'),
            'Sex': aadhaar_data.get('Sex')
        }

        # Retrieve Aadhaar details from the database based on extracted Aadhaar number
        try:
            db_aadhaar = Aadhaar.objects.get(aadhaar_number=aadhaar_data.get('Adhaar Number'))
        except Aadhaar.DoesNotExist:
            db_aadhaar = None

        sex_mapping = {'M': 'MALE', 'F': 'FEMALE', 'O': 'OTHER'}
        # Check if Aadhaar details were retrieved from the database
        if db_aadhaar:
            # Prepare the dictionary for database Aadhaar details
            db_aadhaar_details = {
                'Aadhaar Number': db_aadhaar.aadhaar_number,
                'Name': db_aadhaar.name,
                'Date of Birth': db_aadhaar.date_of_birth.strftime('%d/%m/%Y'),
                'Sex': sex_mapping.get(db_aadhaar.sex, 'Unknown')
            }

            # Compare the extracted Aadhaar details with the database Aadhaar details
            if (aadhaar_data.get('Name').strip() == db_aadhaar_details['Name'].strip() and
                aadhaar_data.get('Date of Birth') == db_aadhaar_details['Date of Birth'] and
                aadhaar_data.get('Sex').lower() == db_aadhaar_details['Sex'].lower()):
                verification_result = "Verification successful: The extracted Aadhaar details match the database."
            else:
                verification_result = "Verification failed: The extracted Aadhaar details do not match the database."

            # Prepare the result data dictionary
            result_data = {
                'extracted_aadhaar': extracted_aadhaar_details,
                'database_aadhaar': db_aadhaar_details,
                'verification_result': verification_result
            }
        else:
            result_data = {
                'extracted_aadhaar': extracted_aadhaar_details,
                'database_aadhaar': None,
                'verification_result': "Verification failed: No Aadhaar details found in the database for the extracted Aadhaar number."
            }
    else:
        result_data = {
            'extracted_aadhaar': None,
            'database_aadhaar': None,
            'verification_result': "Failed to extract Aadhaar details from the image."
        }

    # Pass the result data to the template and render it
    return render(request, 'doc_verify.html', {'result_data': result_data})






# def doc_verify(request):
#     result_data = {}

#     # Extract Aadhaar details using Document AI
#     utils_folder = os.path.join(settings.BASE_DIR, 'home', 'utils')
#     saved_folder = os.path.join(utils_folder, 'saved')
#     file1_path = os.path.join(saved_folder, 'file1.jpg')


#     project_id = "529876974990"
#     location = "us"
#     processor_id = "35a86c53df6f4b1"  # Create processor before running sample
#     processor_version = "f1dece949e79896f"  # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
#     mime_type = "image/jpeg"
#     output_file = "entities.txt"

#     sample6.process_document_entity_extraction_sample(project_id, location, processor_id, processor_version,
#                                                       file1_path, mime_type, output_file)

#     # Read extracted entities from the output file
#     entities_data = extract.read_entities_file(output_file)
#     aadhar_number = entities_data.get('Adhaar Number', '')
#     aadhaar_data = extract.process_aadhaar_number(entities_data, aadhar_number)

#     # Check if Aadhaar details were successfully extracted
#     if aadhaar_data:
#         # Prepare the dictionary for extracted Aadhaar details
#         extracted_aadhaar_details = {
#             'Aadhaar Number': aadhaar_data.get('Adhaar Number'),
#             'Name': aadhaar_data.get('Name'),
#             'Date of Birth': aadhaar_data.get('Date of Birth'),
#             'Sex': aadhaar_data.get('Sex')
#         }

#         # Retrieve Aadhaar details from the database
#         try:
#             db_aadhaar = Aadhaar.objects.first()  # Assuming you want to retrieve the first Aadhaar entry
#         except Aadhaar.DoesNotExist:
#             db_aadhaar = None

#         sex_mapping = {'M': 'MALE', 'F': 'FEMALE', 'O': 'OTHER'}
#         # Check if Aadhaar details were retrieved from the database
#         if db_aadhaar:
#             # Prepare the dictionary for database Aadhaar details
#             db_aadhaar_details = {
#                 'Aadhaar Number': db_aadhaar.aadhaar_number,
#                 'Name': db_aadhaar.name,
#                 'Date of Birth': db_aadhaar.date_of_birth.strftime('%d/%m/%Y'),
#                 'Sex': sex_mapping.get(db_aadhaar.sex, 'Unknown')
#             }

#             # Compare the extracted Aadhaar details with the database Aadhaar details
#             if (aadhaar_data.get('Adhaar Number').strip() == db_aadhaar_details['Aadhaar Number'].strip() and
#                 aadhaar_data.get('Name').strip() == db_aadhaar_details['Name'].strip() and
#                 aadhaar_data.get('Date of Birth') == db_aadhaar_details['Date of Birth'] and
#                 aadhaar_data.get('Sex') == db_aadhaar_details['Sex']):
#                 verification_result = "Verification successful: The extracted Aadhaar details match the database."
#             else:
#                 verification_result = "Verification failed: The extracted Aadhaar details do not match the database."

#             # Prepare the result data dictionary
#             result_data = {
#                 'extracted_aadhaar': extracted_aadhaar_details,
#                 'database_aadhaar': db_aadhaar_details,
#                 'verification_result': verification_result
#             }
#         else:
#             result_data = {
#                 'extracted_aadhaar': extracted_aadhaar_details,
#                 'database_aadhaar': None,
#                 'verification_result': "Verification failed: No Aadhaar details found in the database."
#             }
#     else:
#         result_data = {
#             'extracted_aadhaar': None,
#             'database_aadhaar': None,
#             'verification_result': "Failed to extract Aadhaar details from the image."
#         }

#     # Pass the result data to the template and render it
#     return render(request, 'doc_verify.html', {'result_data': result_data})





@login_required
def authentication(request):
    if request.user.is_superuser:
        if request.method == "POST":
            # Handle form submission
            approved_details = []
            not_approved_details = []
            for key, value in request.POST.items():
                if key.startswith('approveSwitch') and value == 'on':
                    # Extract Aadhaar detail ID from the key
                    aadhaar_detail_id = int(key.replace('approveSwitch', ''))
                    # Retrieve Aadhaar detail object from the ID
                    aadhaar_detail = Aadhaar_detail.objects.get(id=aadhaar_detail_id)
                    # Add the detail to approved list
                    approved_details.append(aadhaar_detail)
                else:
                    # Extract Aadhaar detail ID from the key
                    aadhaar_detail_id = int(key.replace('approveSwitch', ''))
                    # Retrieve Aadhaar detail object from the ID
                    aadhaar_detail = Aadhaar_detail.objects.get(id=aadhaar_detail_id)
                    # Add the detail to not approved list
                    not_approved_details.append(aadhaar_detail)

            return render(request, 'authentication.html', {'approved_details': approved_details, 'not_approved_details': not_approved_details})

        # If it's a GET request, just render the template with Aadhaar details
        aadhaar_details = Aadhaar_detail.objects.all()
        return render(request, 'authentication.html', {'aadhaar_details': aadhaar_details})
    else:
        # Non-superusers will be redirected or shown an access denied message
        return render(request, 'authentication.html')