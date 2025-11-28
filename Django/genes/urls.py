from django.urls import path
from .views import GeneListCreateView, GeneDetailView

urlpatterns = [
    path("", GeneListCreateView.as_view(), name="gene-list-create"),
    path("<int:id>/", GeneDetailView.as_view(), name="gene-detail"),
]