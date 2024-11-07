from django.shortcuts import render

# Create your views here.
# verification/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UploadForm
from .models import SignatureUpload
import random
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.prediction_label, upload.prediction_accuracy = predict_signature(upload.image)
            upload.save()
            return redirect('results')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def results(request):
    uploads = SignatureUpload.objects.filter(user=request.user)
    return render(request, 'results.html', {'uploads': uploads})

# Mock prediction function
def predict_signature(image):
    # Simulate a prediction result without using a neural network
    label = random.choice(['Real', 'Forged'])
    accuracy = round(random.uniform(75, 99), 2)  # Random accuracy between 75-99%
    return label, accuracy
