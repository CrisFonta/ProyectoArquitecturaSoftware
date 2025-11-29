import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PatientVariantReport
from .serializers import ReportSerializer
from .dtos import ReportDTO
from variants.models import GeneticVariant

from drf_spectacular.utils import (
    extend_schema,
    OpenApiRequest,
    OpenApiResponse,
    OpenApiExample,
)

# URL del gateway que expone el microservicio de Clínica
GATEWAY_PATIENT_URL = "http://clinica-app-service:3000/api/v1/clinica/gestion-pacientes/searchPatient?document="
# GATEWAY_PATIENT_URL = "http://localhost:60855/api/v1/clinica/gestion-pacientes/searchPatient?document="

class ReportListCreateView(APIView):
    @extend_schema(
        summary="Listar reportes clínicos",
        responses=OpenApiResponse(ReportSerializer (many=True)),
    )
    def get(self, request):
        reports = PatientVariantReport.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Crear reporte clínico",
        request=OpenApiRequest(ReportDTO),
        description="Crea un reporte de variante detectada en un paciente. "
                    "Valida el paciente a través del gateway y la variante en la BD local.",
        responses={
            201: ReportSerializer,
            400: OpenApiResponse(description="Validación fallida"),
            404: OpenApiResponse(description="Paciente o variante no encontrado"),
            502: OpenApiResponse(description="Error con el microservicio de clínica"),
        },
        examples=[
            OpenApiExample(
                "Ejemplo de reporte clínico",
                value={
                    "patientId": "P-12345",
                    "variantId": "10",
                    "detectionDate": "2024-01-20",
                    "alleleFrequency": 0.42
                }
            )
        ]
    )
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
                {"error": f"Error al contactar la clinica: {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if patient_resp.status_code != 200:
            return Response({"error": "Paciente no encontrado"}, status=status.HTTP_404_NOT_FOUND)


        # Validar variante
        try:
            variant = GeneticVariant.objects.get(id=dto.variantId)
        except GeneticVariant.DoesNotExist:
            return Response({"error": "Variante genética no encontrada "}, status=status.HTTP_404_NOT_FOUND)

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

    @extend_schema(
        summary="Obtener reporte por ID",
        responses={
            200: ReportSerializer,
            404: OpenApiResponse(description="Reporte no encontrado"),
        }
    )
    def get(self, request, id):
        report = self.get_object(id)
        if report is None:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    @extend_schema(
        summary="Eliminar reporte",
        responses={204: OpenApiResponse(description="Reporte eliminado")}
    )
    def delete(self, request, id):
        report = self.get_object(id)
        if report is None:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatientReportsView(APIView):
    @extend_schema(
        summary="Listar reportes de un paciente",
        parameters=[
            {
                "name": "patientId",
                "in": "path",
                "required": True,
                "description": "ID del paciente en el sistema clínico",
                "schema": {"type": "string"}
            }
        ],
        responses=OpenApiResponse(ReportSerializer (many=True)),
    )
    def get(self, request, patientId):
        reports = PatientVariantReport.objects.filter(patientId=patientId)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
