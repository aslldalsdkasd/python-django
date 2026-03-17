from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request:HttpRequest):
    context = {}
    return render(request, 'shopapp/base.html', context=context)

def file_upload(request:HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        if file.size > 1048576:
            file_too_big = True
            context = {
                "file_too_big": file_too_big,
            }
            return render(request, 'shopapp/file_upload.html', context=context)

        else:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

    return render(request, 'shopapp/file_upload.html')

