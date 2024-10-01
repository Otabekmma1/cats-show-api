from rest_framework import permissions, status, viewsets, filters
from rest_framework.response import Response
from django_filters import rest_framework as django_filters

from .models import *
from .serializers import *
from .filters import CatFilter
from .permissions import IsAdminOrReadOnly

class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAdminOrReadOnly]

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    search_fields = ['name', 'breed', 'age', 'color']
    filterset_class = CatFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''filter by breed'''
        breed = self.request.query_params.get('breed', None)
        queryset = Cat.objects.all()
        if breed:
            queryset = queryset.filter(breed_name=breed)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        '''only the owner can update the data'''
        cat = self.get_object()
        if cat.owner != request.user:
            '''will throw an error if the owner does not match the request user'''
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(CatViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        '''only the owner can delete the data'''
        cat = self.get_object()
        if cat.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(CatViewSet, self).destroy(request, *args, **kwargs)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




