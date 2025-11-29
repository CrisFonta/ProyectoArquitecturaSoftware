from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gene
from .serializers import GeneSerializer
from .dtos import GeneDTO
from drf_spectacular.utils import (
    extend_schema,
    OpenApiRequest,
    OpenApiResponse,
    OpenApiExample,
)

class GeneListCreateView(APIView):
    @extend_schema(
        summary="Obtener lista de genes",
        description="Retorna todos los genes almacenados en el sistema.",
        responses=OpenApiResponse(GeneSerializer(many=True)),
    )
    def get(self, request):
        genes = Gene.objects.all()
        serializer = GeneSerializer(genes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Crear un gen",
        description="Crea un nuevo registro de gen usando GeneDTO (Pydantic) como body.",
        request=OpenApiRequest(GeneDTO),
        responses={
            201: OpenApiResponse(GeneSerializer),
            400: OpenApiResponse(description="Error de validación"),
        },
        examples=[
            OpenApiExample(
                "Ejemplo de creación de gen",
                value={
                    "symbol": "BRCA1",
                    "fullName": "Breast cancer type 1 susceptibility protein",
                    "functionSummary": "DNA repair mechanism"
                }
            )
        ]
    )
    def post(self, request):
        try:
            dto = GeneDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GeneSerializer(data=dto.model_dump())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GeneDetailView(APIView):
    def get_object(self, id):
        try:
            return Gene.objects.get(id=id)
        except Gene.DoesNotExist:
            return None

    @extend_schema(
        summary="Obtener un gen por ID",
        responses={
            200: GeneSerializer,
            404: OpenApiResponse(description="Gen no encontrado"),
        }
    )
    def get(self, request, id):
        gene = self.get_object(id)
        if gene is None:
            return Response({"error": "Gen no encontrato"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GeneSerializer(gene)
        return Response(serializer.data)

    @extend_schema(
        summary="Actualizar un gen",
        request=OpenApiRequest(GeneDTO),
        responses={
            200: GeneSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            404: OpenApiResponse(description="Gen no encontrado"),
        }
    )
    def put(self, request, id):
        gene = self.get_object(id)
        if gene is None:
            return Response({"error": "Gen no encontrato"}, status=status.HTTP_404_NOT_FOUND)

        try:
            dto = GeneDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GeneSerializer(gene, data=dto.dict())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Eliminar gen",
        responses={204: OpenApiResponse(description="Gen eliminado")}
    )
    def delete(self, request, id):
        gene = self.get_object(id)
        if gene is None:
            return Response({"error": "Gen no encontrato"}, status=status.HTTP_404_NOT_FOUND)
        gene.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
