from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Folder, UploadImages
from .forms import GalleryImageForm, FolderForm
from django.core.files.base import ContentFile
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
import os


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
        for cloud_folder in get_all_folders:
            folder_name = cloud_folder['name']

            # 1. Create folder in DB if missing
            folder_obj, created = Folder.objects.get_or_create(name=folder_name)

            # 2. Get all images in that folder
            resources = cloudinary.api.resources(
                type='upload',
                prefix=f"wheels-next-the-sea/{folder_name}/",
                max_results=100
            )['resources']

            for image in resources:
                secure_url = image['secure_url']
                unique_title = secure_url.rsplit('/', 1)[1]
                # 3. Check if image is in DB by Cloudinary public_id
                if not UploadImages.objects.filter(url=secure_url, title=unique_title).exists():
                    UploadImages.objects.create(
                        title = unique_title,
                        folder=folder_obj,
                        url=secure_url,  # CloudinaryField supports public_id directly
                        uploaded_by=request.user.username
                    )

                folder_images.append(image)
            
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
        image =  request.FILES.getlist('images')
        if not image:
            return HttpResponse("No file was uploaded.")
        folder_name = request.POST.get("targetFolder")
        try:
            upload_folder = Folder.objects.get(name=folder_name)
        except Folder.DoesNotExist:
            return HttpResponse("Folder not found", status=404)
        image_folder = upload_folder.name
        upload_preset = {
            "folder": f"wheels-next-the-sea/{image_folder}",
            "tags": image_folder,
            "transformation": [
                {"width": 100, "height": 100, "crop": "fill", "gravity": "auto"},
                {"fetch_format": "auto", "quality": "auto"}
            ],
            "auto_tagging": 0.9,
        }
        if form.is_valid():
            for img in request.FILES.getlist('images'):
                new_image = cloudinary.uploader.upload(img, **upload_preset)
                image_url = new_image['secure_url']
                image_title = image_url.rsplit('/', 1)[1]
                UploadImages.objects.create(
                    title = image_title,
                    folder=upload_folder,
                    url=image_url,
                    uploaded_by=request.user.username
                )
            return redirect('gallery')
        else:
            print(form.errors)
            return HttpResponse("Form submission failed. Check console.")
    else:
        form = GalleryImageForm()
    context = {'cloud_signin' : cloud_signin, 'folder':folder} 
    return redirect(reverse('gallery'))

@login_required
@user_passes_test(is_superuser)
@csrf_exempt
def delete_image(request):
    if request.method == "POST" and request.user.is_superuser:
        data = json.loads(request.body)
        image_url = data.get("image_url", "")
        if not image_url.startswith("https://res.cloudinary.com/"):
            return JsonResponse({"error": "Invalid image path"}, status=400)

        try:
            # Assumes format: https://res.cloudinary.com/yourcloud/image/upload/v1234567/folder/image.jpg
            # Extract everything after `/upload/` and remove extension
            path = image_url.split("/upload/")[1]
            parts = path.split("wheels-next-the-sea", 1)
            if len(parts) != 2:
                return JsonResponse({"error": "Unexpected image path format"}, status=400)

            public_id = "wheels-next-the-sea" + parts[1]
            public_id = os.path.splitext(public_id)[0]  # Remove file extension

            # Delete from Cloudinary
            result = cloudinary.uploader.destroy(public_id)
            if result.get("result") == "ok":
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"error": "Failed to delete from Cloudinary"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Unauthorized or invalid request"}, status=403)


@login_required
@user_passes_test(is_superuser)
@csrf_exempt
def delete_folder(request):
    if request.method == "POST":
        data = json.loads(request.body)
        folder_name = data.get("folder")

        if not folder_name:
            return JsonResponse({"error": "Missing folder name"}, status=400)

        # Delete all images in that folder
        images = UploadImages.objects.filter(folder__name=folder_name)
        errors = []

        for image in images:
            try:
                path = image.image.url.split("/upload/")[1]
                public_id = os.path.splitext(path)[0]

                result = cloudinary.uploader.destroy(public_id)
                if result.get("result") != "ok":
                    errors.append(f"Failed to delete {public_id}")
                else:
                    image.delete()
            except Exception as e:
                errors.append(str(e))

        # Try deleting the folder itself in Cloudinary
        try:
            cloudinary.api.delete_folder(folder_name)
        except cloudinary.exceptions.Error as e:
            errors.append(f"Cloudinary folder delete error: {str(e)}")

        # Delete folder model (if using a Folder model)
        try:
            Folder.objects.get(name=folder_name).delete()
        except Folder.DoesNotExist:
            pass

        if errors:
            return JsonResponse({"error": "Some issues occurred", "details": errors}, status=500)

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)