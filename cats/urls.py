from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include



router = DefaultRouter()
router.register(r'breeds', BreedViewSet)
router.register(r'cats', CatViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

