from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gene
from .serializers import GeneSerializer
from .dtos import GeneDTO

class GeneListCreateView(APIView):
    def get(self, request):
        genes = Gene.objects.all()
        serializer = GeneSerializer(genes, many=True)
        return Response(serializer.data)

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

    def get(self, request, id):
        gene = self.get_object(id)
        if gene is None:
            return Response({"error": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GeneSerializer(gene)
        return Response(serializer.data)

    def put(self, request, id):
        gene = self.get_object(id)
        if gene is None:
            return Response({"error": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            dto = GeneDTO(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GeneSerializer(gene, data=dto.dict())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        gene = self.get_object(id)
        if gene is None:
            return Response({"error": "Gene not found"}, status=status.HTTP_404_NOT_FOUND)
        gene.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
