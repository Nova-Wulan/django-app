from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='project/images')

    def __str__(self):
        return self.title
    
class Rating(models.Model):
    name = models.CharField(max_length=100)
    caption = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating dari 1 sampai 5"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="reviews"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project.title} - {self.rating} Stars"
