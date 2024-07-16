from django.shortcuts import render

from .forms import ImageUploadForm
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from io import BytesIO
import os
# from tensorflow.keras.applications.vgg16 import VGG16
# from tensorflow.keras.models import save_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions

# model = VGG16(weights='imagenet')
# save_model(model, 'vgg16.h5')
# model.summary()

def predict(request):
    if request.method == 'GET':
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            img_file = BytesIO(img_file.read())
            img = load_img(img_file, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array.shape
            print(img_array.shape)
            img_array = img_array.reshape((1, 224, 224, 3))
            img_array.shape
            print(img_array.shape)
            img_array = preprocess_input(img_array)
            # img_array = img_array/255
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'vgg16.h5')
            model = load_model(model_path)
            result = model.predict(img_array)
            result
            prediction = decode_predictions(result)

            first_tuple = prediction[0][0]
            second_tuple = prediction[0][1]
            third_tuple = prediction[0][2]
            fourth_tuple = prediction[0][3]
            fifth_tuple = prediction[0][4]

            img_data = request.POST.get('img_data')
            return render(request, 'home.html', {'form': form, 'prediction': prediction, 'img_data': img_data, 'first_tuple': first_tuple, 'second_tuple': second_tuple, 'second_tuple': second_tuple, 'third_tuple': third_tuple, 'fourth_tuple': fourth_tuple, 'fifth_tuple': fifth_tuple })
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})

