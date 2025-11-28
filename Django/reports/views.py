import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PatientVariantReport
from .serializers import ReportSerializer
from .dtos import ReportDTO
from variants.models import GeneticVariant

# URL del gateway que expone el microservicio de Clínica
GATEWAY_PATIENT_URL = "http://gateway-service/clinic/patients/"

class ReportListCreateView(APIView):
    def get(self, request):
        reports = PatientVariantReport.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            dto = ReportDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validar paciente en el microservicio de Clínica a través del gateway
        token = request.headers.get("Authorization", "")
        try:
            patient_resp = requests.get(
                GATEWAY_PATIENT_URL + dto.patientId,
                headers={"Authorization": token} if token else {},
                timeout=5,
            )
        except requests.RequestException as exc:
            return Response(
                {"error": f"Error contacting Clinic service: {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if patient_resp.status_code != 200:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validar variante
        try:
            variant = GeneticVariant.objects.get(id=dto.variantId)
        except GeneticVariant.DoesNotExist:
            return Response({"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)

        data = dto.dict()
        data["variant"] = str(variant.id)

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailView(APIView):
    def get_object(self, id):
        try:
            return PatientVariantReport.objects.get(id=id)
        except PatientVariantReport.DoesNotExist:
            return None

    def get(self, request, id):
        report = self.get_object(id)
        if report is None:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def delete(self, request, id):
        report = self.get_object(id)
        if report is None:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatientReportsView(APIView):
    def get(self, request, patientId):
        reports = PatientVariantReport.objects.filter(patientId=patientId)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
