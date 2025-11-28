
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeneticVariant
from .serializers import VariantSerializer
from .dtos import VariantDTO
from genes.models import Gene

class VariantListCreateView(APIView):
    def get(self, request):
        variants = GeneticVariant.objects.all()
        serializer = VariantSerializer(variants, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            dto = VariantDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gene = Gene.objects.get(id=dto.geneId)
        except Gene.DoesNotExist:
            return Response({"error": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)

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

    def get(self, request, id):
        variant = self.get_object(id)
        if variant is None:
            return Response({"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VariantSerializer(variant)
        return Response(serializer.data)

    def put(self, request, id):
        variant = self.get_object(id)
        if variant is None:
            return Response({"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            dto = VariantDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gene = Gene.objects.get(id=dto.geneId)
        except Gene.DoesNotExist:
            return Response({"error": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)

        data = dto.dict()
        data["gene"] = gene.id

        serializer = VariantSerializer(variant, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        variant = self.get_object(id)
        if variant is None:
            return Response({"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
