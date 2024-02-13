from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .utils import verify
import os
from django.conf import settings

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
            return redirect("upload")
        else:
            return render(request,'login.html')

    return render(request,'login.html')

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

def upload(request):
    result_string = None

    if request.method == 'POST' and 'file1' in request.FILES and 'file2' in request.FILES:
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']

        # Define the folder path where files will be saved
        utils_folder = os.path.join(settings.BASE_DIR, 'home', 'utils')
        
        # Ensure the folder exists, create it if not
        if not os.path.exists(utils_folder):
            os.makedirs(utils_folder)

        # Generate unique file names
        file1_path = os.path.join(utils_folder, 'file1.jpg')
        file2_path = os.path.join(utils_folder, 'file2.jpg')

        # Save the uploaded files to the utils folder
        with open(file1_path, 'wb') as destination:
            for chunk in file1.chunks():
                destination.write(chunk)

        with open(file2_path, 'wb') as destination:
            for chunk in file2.chunks():
                destination.write(chunk)

        # Call the function from the external Python file with file paths
        result_string = verify.ver(file1_path, file2_path)
        print(result_string)

    return render(request, 'upload.html', {'result_string': result_string})

# def upload(request):
#     result_string = None
#     if request.method == 'POST' and 'file1' in request.FILES and 'file2' in request.FILES:
#         file1 = request.FILES['file1']
#         file2 = request.FILES['file2']

#         # Call the function from the external Python file
#         result_string = verify.ver(file1, file2)
#         print(result_string)
#     return render(request, 'upload.html', {'result_string': result_string})