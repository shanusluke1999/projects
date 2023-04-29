from django.urls import path
from . views  import (adoptionListView,
                      adoptionDetailView,
                      adoptionCreateView,SearchView,adoption_application)

urlpatterns = [
    # other URL patterns...
    path('adoption/', adoptionListView.as_view(),name='adoption-feed'),
    path('adoption/<int:pk>/', adoptionDetailView.as_view(),name='adoption-detail'),
    path('adoption/new/', adoptionCreateView.as_view(),name='adoption-create'),
    path('adoption/<int:pk>/apply/', adoption_application, name='adoption_application'),
    
    # path('search/', SearchView.as_view(), name='search')
]
