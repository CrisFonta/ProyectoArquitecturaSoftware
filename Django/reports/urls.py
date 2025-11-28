from django.urls import path
from .views import ReportListCreateView, ReportDetailView, PatientReportsView

urlpatterns = [
    path("", ReportListCreateView.as_view(), name="report-list-create"),
    path("<uuid:id>/", ReportDetailView.as_view(), name="report-detail"),
    path("patient/<uuid:patientId>/", PatientReportsView.as_view(), name="patient-reports"),
]
