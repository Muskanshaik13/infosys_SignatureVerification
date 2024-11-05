from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.core.files.storage import FileSystemStorage
import os
# auth_app/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'auth_app/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'auth_app/register.html', {'form': form})


# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

# Load the model (do this once when the server starts)
model_path = os.path.join(os.path.dirname(__file__), 'models', 'signature_model.h5')
model = load_model(model_path)

@login_required
def upload(request):
    result = None
    if request.method == 'POST' and request.FILES['signature']:
        # Save the uploaded file
        signature = request.FILES['signature']
        fs = FileSystemStorage()
        filename = fs.save(signature.name, signature)
        file_path = fs.path(filename)

        # Preprocess the image for the model
        img = load_img(file_path, target_size=(224, 224))  # Resize to the model’s expected input size
        img_array = img_to_array(img) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Make prediction
        prediction = model.predict(img_array)
        result = 'real' if prediction[0][0] > 0.5 else 'forged'  # Adjust threshold as per your model

        # Remove the uploaded file after processing
        fs.delete(filename)

    return render(request, 'auth_app/upload.html', {'result': result})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('upload')
    else:
        form = LoginForm()
    return render(request, 'auth_app/login.html', {'form': form})


