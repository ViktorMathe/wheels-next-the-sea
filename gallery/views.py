from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Folder, UploadImages
from .forms import GalleryImageForm, FolderForm
import cloudinary.uploader
import cloudinary.api
import json
import os
from urllib.parse import urlparse

# Superuser check
def is_superuser(user):
    return user.is_superuser

def gallery(request):
    folders = Folder.objects.all()
    folder_images = {}
    is_superuser_flag = request.user.is_superuser

    folder_form = FolderForm(request.POST or None)
    upload_form = GalleryImageForm()

    # Handle folder creation
    if request.method == 'POST' and folder_form.is_valid():
        folder_name = folder_form.cleaned_data['name']
        cloudinary.api.create_folder(f'wheels-next-the-sea/{folder_name}')
        folder_form.save()
        return redirect('gallery')

    # Get all folders from Cloudinary
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
            image_title = secure_url.rsplit('/', 1)[1]

            # Use get_or_create with defaults, avoid duplicates
            upload_img, _ = UploadImages.objects.get_or_create(
                folder=folder_obj,
                title=image_title,
                defaults={'url': secure_url, 'uploaded_by': request.user.username}
            )
            images_list.append(upload_img)

        folder_images[folder_obj] = images_list

    context = {
        'folder_form': folder_form,
        'upload_form': upload_form,
        'folders': folders,
        'folder_images': folder_images,
        'is_superuser': is_superuser_flag,
        'get_all_folders': get_all_folders,
    }
    return render(request, 'gallery.html', context)


def year_gallery(request, folder_name):
    folder = get_object_or_404(Folder, name=folder_name)

    # === Sync DB with Cloudinary ===
    try:
        resources = cloudinary.api.resources(prefix=f"wheels-next-the-sea/{folder_name}/")['resources']
        cloud_urls = [r['secure_url'] for r in resources]
        # Delete any UploadImages entries that no longer exist on Cloudinary
        UploadImages.objects.filter(folder=folder).exclude(url__in=cloud_urls).delete()
    except cloudinary.exceptions.Error as e:
        print(f"Cloudinary API error: {e}")

    # Fetch remaining images from DB
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
            return JsonResponse({"success": False, "error": "No file uploaded."})

        try:
            upload_folder = Folder.objects.get(name=folder_name)
        except Folder.DoesNotExist:
            return JsonResponse({"success": False, "error": "Folder not found."}, status=404)

        if not form.is_valid():
            return JsonResponse({"success": False, "error": f"Form submission failed: {form.errors}"})

        uploaded_urls = []

        try:
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
                # Upload to Cloudinary
                new_image = cloudinary.uploader.upload(img, **upload_preset)
                image_url = new_image['secure_url']
                image_title = image_url.rsplit('/', 1)[1]

                # Create or update DB record
                upload_obj, created = UploadImages.objects.get_or_create(
                    folder=upload_folder,
                    title=image_title,
                    defaults={
                        'url': image_url,
                        'uploaded_by': request.user.username
                    }
                )

                if not created:
                    upload_obj.url = image_url
                    upload_obj.save()

                uploaded_urls.append(image_url)

            return JsonResponse({"success": True, "urls": uploaded_urls})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

@login_required
@user_passes_test(is_superuser)
@csrf_exempt
def delete_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        image_url = data.get("image_url")
        if not image_url or not image_url.startswith("https://res.cloudinary.com/"):
            return JsonResponse({"error": "Invalid image URL"}, status=400)

        # Parse Cloudinary public_id
        parsed = urlparse(image_url)
        public_id = os.path.splitext(parsed.path.split("/wheels-next-the-sea/")[1])[0]

        result = cloudinary.uploader.destroy(f"wheels-next-the-sea/{public_id}")

        if result.get("result") != "ok":
            return JsonResponse({"error": "Failed to delete from Cloudinary"}, status=500)

        # Delete from DB
        UploadImages.objects.filter(url=image_url).delete()

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@user_passes_test(is_superuser)
@csrf_exempt
def delete_multiple_images(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            images = data.get("urls", [])  # <-- FIXED
            if not images:
                return JsonResponse({"success": False, "error": "No images provided"})

            for image_url in images:
                try:
                    img = UploadImages.objects.get(url=image_url)
                    # extract correct public_id
                    parsed = urlparse(image_url)
                    public_id = os.path.splitext(parsed.path.split("/wheels-next-the-sea/")[1])[0]
                    cloudinary.uploader.destroy(f"wheels-next-the-sea/{public_id}")
                    img.delete()
                except UploadImages.DoesNotExist:
                    continue

            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


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