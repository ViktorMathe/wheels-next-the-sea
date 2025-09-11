from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Folder, UploadImages
from .forms import GalleryImageForm, FolderForm
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
import os


def is_superuser(user):
    return user.is_superuser


def gallery(request):
    folders = Folder.objects.all()
    folder_images = {}

    if request.method == 'POST':
        folder_form = FolderForm(request.POST)
        if folder_form.is_valid():
            folder_name = folder_form.cleaned_data['name']
            cloudinary.api.create_folder(f'wheels-next-the-sea/{folder_name}')
            folder_form.save()
            return redirect('gallery')
    else:
        folder_form = FolderForm()
        upload_form = GalleryImageForm()
        get_all_folders = cloudinary.api.subfolders('wheels-next-the-sea')['folders']

        for cloud_folder in get_all_folders:
            folder_name = cloud_folder['name']
            folder_obj, _ = Folder.objects.get_or_create(name=folder_name)

            resources = cloudinary.api.resources(
                type='upload',
                prefix=f"wheels-next-the-sea/{folder_name}/",
                max_results=100
            )['resources']

            images_list = []
            for image in resources:
                secure_url = image['secure_url']
                unique_title = secure_url.rsplit('/', 1)[1]

                upload_img, _ = UploadImages.objects.get_or_create(
                    url=secure_url,
                    title=unique_title,
                    folder=folder_obj,
                    defaults={'uploaded_by': request.user.username}
                )
                images_list.append(upload_img)

            folder_images[folder_obj] = images_list

    context = {
        'folder_form': folder_form,
        'upload_form': upload_form,
        'folders': folders,
        'folder_images': folder_images,
    }
    return render(request, 'gallery.html', context)


def year_gallery(request, folder_name):
    folder = get_object_or_404(Folder, name=folder_name)
    images = folder.images.all()
    return render(request, "year_gallery.html", {
        "folder": folder,
        "images": images,
    })


@login_required
@user_passes_test(is_superuser)
def upload_images(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        folder_name = request.POST.get("targetFolder")

        if not images:
            return HttpResponse("No file uploaded.")

        try:
            upload_folder = Folder.objects.get(name=folder_name)
        except Folder.DoesNotExist:
            return HttpResponse("Folder not found.", status=404)

        if form.is_valid():
            upload_preset = {
                "folder": f"wheels-next-the-sea/{folder_name}",
                "tags": folder_name,
                "transformation": [
                    {"width": "auto", "crop": "auto", "gravity": "auto"},
                    {"fetch_format": "auto", "quality": "auto"}
                ],
                "auto_tagging": 0.9,
            }
            for img in images:
                new_image = cloudinary.uploader.upload(img, **upload_preset)
                image_url = new_image['secure_url']
                image_title = image_url.rsplit('/', 1)[1]
                UploadImages.objects.create(
                    title=image_title,
                    folder=upload_folder,
                    url=image_url,
                    uploaded_by=request.user.username
                )
            return redirect('gallery')
        else:
            return HttpResponse(f"Form submission failed: {form.errors}")
    return redirect('gallery')


@login_required
@user_passes_test(is_superuser)
@csrf_exempt
def delete_image(request):
    if request.method == "POST":
        data = json.loads(request.body)
        image_url = data.get("image_url", "")
        if not image_url.startswith("https://res.cloudinary.com/"):
            return JsonResponse({"error": "Invalid image path"}, status=400)

        try:
            path = image_url.split("/upload/")[1]
            parts = path.split("wheels-next-the-sea", 1)
            public_id = "wheels-next-the-sea" + parts[1]
            public_id = os.path.splitext(public_id)[0]

            result = cloudinary.uploader.destroy(public_id)
            if result.get("result") == "ok":
                UploadImages.objects.filter(url=image_url).delete()
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

        errors = []

        # Delete all images
        images = UploadImages.objects.filter(folder__name=folder_name)
        for image in images:
            try:
                path = image.url.split("/upload/")[1]
                public_id = os.path.splitext(path)[0]
                result = cloudinary.uploader.destroy(public_id)
                if result.get("result") != "ok":
                    errors.append(f"Failed to delete {public_id}")
                else:
                    image.delete()
            except Exception as e:
                errors.append(str(e))

        # Delete Cloudinary folder
        try:
            cloudinary.api.delete_folder(folder_name)
        except cloudinary.exceptions.Error as e:
            errors.append(str(e))

        # Delete Folder model
        Folder.objects.filter(name=folder_name).delete()

        if errors:
            return JsonResponse({"error": "Some issues occurred", "details": errors}, status=500)
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)