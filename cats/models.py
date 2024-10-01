from django.db import models
from django.contrib.auth.models import User


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

COLOR_CHOICES = [
    ('grey', 'Grey'),
    ('black', 'Black'),
    ('brown', 'Brown'),
    ('white', 'White'),
    ('red', 'Red'),
    ('yellow', 'Yellow')
]

class Cat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    color = models.CharField(choices=COLOR_CHOICES, max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ['cat', 'user']

    def __str__(self):
        return f"{self.cat} -> {self.user}"
