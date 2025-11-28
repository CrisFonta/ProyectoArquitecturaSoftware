from django.urls import path
from .views import VariantListCreateView, VariantDetailView

urlpatterns = [
    path("", VariantListCreateView.as_view(), name="variant-list-create"),
    path("<uuid:id>/", VariantDetailView.as_view(), name="variant-detail"),
]
