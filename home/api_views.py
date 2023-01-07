from .models import *
from .serializers import *
from rest_framework import viewsets
import django_filters.rest_framework
from rest_framework import generics
from rest_framework import filters




# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category', 'subcategory',  'brand', 'stock']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price','id']