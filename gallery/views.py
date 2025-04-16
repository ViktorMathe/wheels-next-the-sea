from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from cloudinary.forms import cl_init_js_callbacks
from .models import Folder, UploadImages
from .forms import GalleryImageForm, FolderForm
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
import cloudinary
import json


def gallery(request):
    folder = Folder.objects.all()
    if request.method == 'POST':
        folder_form = FolderForm(request.POST)
        image_folder = folder_form['name'].value()
        if folder_form.is_valid():
            create_folder = cloudinary.api.create_folder(f'wheels-next-the-sea/{image_folder}')
            folder_form.save()
            return redirect('gallery')
    else:
        folder_form = FolderForm()
        upload_form = GalleryImageForm()
        get_all_folders = cloudinary.api.subfolders('wheels-next-the-sea')['folders']
        get_folder = {}
        folder_images = []
        for x in get_all_folders:
            get_folder =  x['name']
            folder_images += cloudinary.api.resources_by_tag(get_folder)['resources']
            
    context = {'folder_form':folder_form, 'upload_form': upload_form, 'get_all_folders':get_all_folders, 'folder_images': folder_images, 'folder':folder}
    return render(request, 'gallery.html', context)

# Superuser check
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def upload_images(request):
    folder = Folder.objects.all()
    cloud_signin = cloudinary.utils.api_sign_request({
        'cloud_name' : settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        'api_key' : settings.CLOUDINARY_STORAGE['API_KEY'],
        'signature_algorithm' : "sha256",
        'timestamp': 1315060510
    }, settings.CLOUDINARY_STORAGE['API_SECRET'])
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        cloudinary.api_key = settings.CLOUDINARY_STORAGE['API_KEY']
        image =  request.FILES.get('images', None)
        if not image:
            return HttpResponse("No file was uploaded.")
        image_folder_id = request.POST.get('folder')
        upload_folder = Folder.objects.get(pk=image_folder_id)
        image_folder = upload_folder.name
        upload_preset = {"folder": f"wheels-next-the-sea/{image_folder}",
                                 "tags": image_folder,
                                 "transformation": [
                                                {"width": 500, "height": 500, "crop": "fill"},
                                                        ],
                                 "auto_tagging": 0.9}
        if form.is_valid():
            new_image = cloudinary.uploader.upload(image, **upload_preset)
            image_url = new_image['secure_url']
            print(image_url)
            UploadImages.objects.create(
                  folder=upload_folder,
                  pic=image_url
            )
            form.save()
            return redirect('gallery')
        else:
            print(form.errors)
            return HttpResponse("Form submission failed. Check console.")
    else:
        form = GalleryImageForm()
    context = {'cloud_signin' : cloud_signin, 'folder':folder} 
    return redirect(reverse('gallery'))
