import re
import os
import joblib
import string
import json
import pickle
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
from django.shortcuts import render 
from django.urls import reverse
from django.conf import settings
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from Dashboard.models import Complaint
from django.contrib.auth.decorators import login_required
import numpy as np
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences #***
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input#***
from tensorflow.keras.preprocessing.text import tokenizer_from_json#***

MIN_COMPLAINT_LENGTH = 40
MAX_CAPTION_LENGTH=63

DEPARTMENTS = {
    0: 'Road Construction and Management',
    1: 'Water Supply and Management',
    2: 'Electricity Department',
    3: 'Waste Management',
    4: 'Revenue Department',
    5: 'Real Estate and Management',
    6: 'Nature and Environment',
    7: 'Health Department',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
text_model_path = os.path.join(BASE_DIR, 'SavedModels', 'text_classifier_model.pkl')
text_vectorizer_path = os.path.join(BASE_DIR, 'SavedModels', 'text_vectorizer.pkl')
text_model = joblib.load(text_model_path)
text_vectorizer = joblib.load(text_vectorizer_path)
# image_caption_model_path = os.path.join(BASE_DIR, 'SavedModels', 'final_model.h5')
image_caption_model_path = os.path.join(BASE_DIR, 'SavedModels', 'trained_model.h5')
tokenizer_path = os.path.join(BASE_DIR, 'SavedModels', 'tokenizer.json')
image_caption_model = load_model(image_caption_model_path)
with open(tokenizer_path, 'r') as f:
    tokenizer_json = json.load(f)
tokenizer = tokenizer_from_json(tokenizer_json)
@login_required(login_url='/login/')
def dashboard(request):
    user = request.user
    status_count=get_status_count(user)
    complaints=get_complaints(user)
    data = {'user': user, 'status_count': status_count,'complaints':complaints,'departments':DEPARTMENTS}
    return render(request, 'dashboard.html', data)

@login_required(login_url='/login/')
def new_complaint(request):
    if request.method == 'POST':
        user = request.user
        if 'text' in request.POST:
            text = request.POST.get('text')
            if is_valid_complaint(text):
                predicted_label = predict_text_label(text)
                set_complaint(user, text, predicted_label)
                messages.success(request, "New complaint registered successfully!!!")
            else:
                messages.error(request, "Invalid complaint: Too short or meaningless")
                return redirect('new_complaint')
        if 'image_complaint' in request.FILES:
            image = request.FILES['image_complaint']
            text = image_complaint(image)
            predicted_label = predict_text_label(text)
            set_complaint(user, text, predicted_label, image)
            messages.success(request, "New complaint registered successfully!!!")
        return redirect('dashboard')
    return render(request, 'new_complaint.html')

def get_complaints(user, *args):
    if user.role == "staff" and args:
        department_name = DEPARTMENTS[args[0]]
        complaints = Complaint.objects.filter(department=department_name).values()
    else:
        complaints = user.complaint_set.all().values()
    return complaints

def department_complaints(request,id):
    user=request.user
    complaints=get_complaints(user,id);
    department_name=DEPARTMENTS[id]
    data={'complaints':complaints,'department_name':department_name}
    return render(request, 'department_complaints.html',data)

def get_status_count(user):
      if user.role == 'staff':
        total_count=Complaint.objects.all().count()
        pending_count = Complaint.objects.filter(status='Pending').count()
        resolved_count = Complaint.objects.filter(status='Resolved').count()
        rejected_count = Complaint.objects.filter(status='Rejected').count()
      else:
        total_count=user.complaint_set.count()
        pending_count = user.complaint_set.filter(status='Pending').count()
        resolved_count = user.complaint_set.filter(status='Resolved').count()
        rejected_count = user.complaint_set.filter(status='Rejected').count()
      return {'total_count': total_count, 'pending_count': pending_count, 'resolved_count': resolved_count,'rejected_count': rejected_count}
    
def view_details(user,id):
    complaint =Complaint.objects.get(id=id).values()
    return complaint  
        
def set_complaint(user, complaint, predicted_label,*args):
    if len(args) == 1:
        image = args[0]
        Complaint.objects.create(user=user, complaint=complaint, department=predicted_label,image=image)
    elif len(args) == 0:
        Complaint.objects.create(user=user, complaint=complaint, department=predicted_label)
    
      
def predict_text_label(text):
         vectorized_text = text_vectorizer.transform([text])
         prediction = text_model.predict(vectorized_text)
         return str(prediction[0])
     
def user_logout(request):
    logout(request)
    return render(request, 'home.html')

def is_valid_complaint(text):
    if len(text) <= MIN_COMPLAINT_LENGTH:
        return False
    else:
        common_words = ['urgent', 'not working', 'broken', 'issue', 'problem', 'please', 'help', 'emergency', 'broken', 'fix', 'trouble', 'malfunction', 'inconvenience', 'unacceptable', 'dissatisfaction']
        pattern = r'\b(?:' + '|'.join(common_words) + r')\b'  # Word boundary \b ensures whole word matching
        regex = re.compile(pattern, flags=re.IGNORECASE | re.UNICODE | re.MULTILINE | re.DOTALL)
        match = regex.search(text)
        return match is not None 
    return True

def get_word_from_index(index, tokenizer):
    return next((word for word, idx in tokenizer.word_index.items() if idx == index), None)

def predict_caption(model, image_features, tokenizer, max_caption_length):
    caption = 'startseq'
    for _ in range(max_caption_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences([sequence], maxlen=max_caption_length)
        yhat = model.predict([image_features, sequence], verbose=0)
        predicted_index = np.argmax(yhat)
        predicted_word = get_word_from_index(predicted_index, tokenizer)
        caption += " " + predicted_word
        if predicted_word is None or predicted_word == 'endseq':
            break
    caption = caption.replace('startseq', '').replace('endseq', '').strip()
    return caption


def extract_features(image_file):
    vgg_model = VGG16()
    model = Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)
    img = Image.open(image_file)
    img = img.resize((224, 224))
    img_data = np.asarray(img, dtype=np.uint8)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    feature = model.predict(img_data, verbose=0)
    return feature

def image_complaint(image):
    if isinstance(image, InMemoryUploadedFile):
        image_features = extract_features(io.BytesIO(image.read()))
        predicted_caption = predict_caption(image_caption_model, image_features, tokenizer, MAX_CAPTION_LENGTH)
        return predicted_caption
    else:
        raise ValueError("Invalid image object")
