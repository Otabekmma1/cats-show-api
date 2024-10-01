from django_filters import rest_framework as django_filters
from .models import COLOR_CHOICES, Breed, Cat

class CatFilter(django_filters.FilterSet):
    breed = django_filters.ModelChoiceFilter(
        queryset=Breed.objects.all(),
        empty_label = 'All'
    )
    color = django_filters.ChoiceFilter(
        choices=COLOR_CHOICES,
        empty_label = 'All'
    )
    age = django_filters.NumberFilter(field_name='age')

    class Meta:
        model = Cat
        fields = ['breed', 'color', 'age']
