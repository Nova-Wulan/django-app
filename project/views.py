from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Project, Rating

# Halaman utama (index)
def index(request):
    searchTitle = request.GET.get('title')  # Ambil parameter pencarian
    projects = Project.objects.filter(title__icontains=searchTitle) if searchTitle else None
    return render(request, 'index.html', {'searchTitle': searchTitle, 'projects': projects})

# Halaman About
def about(request):
    return render(request, 'about.html')

# Halaman Contact
def contact(request):
    return render(request, 'contact.html')

# Halaman My Projects
def myproject(request):
    projects = Project.objects.all()
    return render(request, 'myproject.html', {'projects': projects})

# Detail Proyek dengan Rating

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    reviews = project.reviews.all()

    if request.method == "POST":
        # Ambil data dari form
        name = request.POST.get('nama')
        caption = request.POST.get('caption')
        try:
            rating_value = int(request.POST.get("rating", 0))
        except ValueError:
            rating_value = 0

        # Validasi data
        if not name:
            error_message = "Nama harus diisi!"
        elif not (1 <= rating_value <= 5):
            error_message = "Rating harus antara 1 hingga 5!"
        else:
            # Simpan data jika valid
            Rating.objects.create(
                name=name,
                caption=caption,
                rating=rating_value,
                project=project
            )
            # Redirect ke halaman yang sama untuk mencegah pengiriman ulang data
            return redirect('project_detail', project_id=project_id)

        return render(request, 'project_detail.html', {
            'project': project,
            'reviews': reviews,
            'average_rating': round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1),
            'error': error_message
        })

    # Hitung rata-rata rating
    average_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1)

    return render(request, 'project_detail.html', {
        'project': project,
        'reviews': reviews,
        'average_rating': average_rating
    })