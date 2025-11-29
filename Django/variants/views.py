
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeneticVariant
from .serializers import VariantSerializer
from .dtos import VariantDTO
from genes.models import Gene

from drf_spectacular.utils import (
    extend_schema,
    OpenApiRequest,
    OpenApiResponse,
    OpenApiExample,
)

class VariantListCreateView(APIView):
    @extend_schema(
        summary="Listar variantes genéticas",
        responses=OpenApiResponse(VariantSerializer(many=True)),
    )
    def get(self, request):
        variants = GeneticVariant.objects.all()
        serializer = VariantSerializer(variants, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Crear variante genética",
        description="Crea una variante usando VariantDTO. "
                    "El campo geneId debe corresponder a un gen existente.",
        request=OpenApiRequest(VariantDTO),
        responses={
            201: VariantSerializer,
            404: OpenApiResponse(description="Gen no encontrado"),
            400: OpenApiResponse(description="Error de validación"),
        },
        examples=[
            OpenApiExample(
                "Ejemplo de creación de variante",
                value={
                    "geneId": 1,
                    "chromosome": "7",
                    "position": 140453136,
                    "referenceBase": "A",
                    "alternateBase": "T",
                    "impact": "HIGH"
                }
            )
        ]
    )
    def post(self, request):
        try:
            dto = VariantDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gene = Gene.objects.get(id=dto.geneId)
        except Gene.DoesNotExist:
            return Response({"error": "Gen no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = dto.dict()
        data["gene"] = gene.id

        serializer = VariantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VariantDetailView(APIView):
    def get_object(self, id):
        try:
            return GeneticVariant.objects.get(id=id)
        except GeneticVariant.DoesNotExist:
            return None

    @extend_schema(
        summary="Obtener variante por ID",
        responses={
            200: VariantSerializer,
            404: OpenApiResponse(description="Variante no encontrada"),
        }
    )
    def get(self, request, id):
        variant = self.get_object(id)
        if variant is None:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VariantSerializer(variant)
        return Response(serializer.data)

    @extend_schema(
        summary="Actualizar variante genética",
        request=OpenApiRequest(VariantDTO),
        responses={
            200: VariantSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            404: OpenApiResponse(description="Variante o gen no encontrado"),
        }
    )
    def put(self, request, id):
        variant = self.get_object(id)
        if variant is None:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        try:
            dto = VariantDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gene = Gene.objects.get(id=dto.geneId)
        except Gene.DoesNotExist:
            return Response({"error": "Gen no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = dto.dict()
        data["gene"] = gene.id

        serializer = VariantSerializer(variant, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Eliminar variante genética",
        responses={204: OpenApiResponse(description="Variante eliminada")}
    )
    def delete(self, request, id):
        variant = self.get_object(id)
        if variant is None:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
