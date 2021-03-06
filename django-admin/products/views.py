from rest_framework import viewsets, status
from .models import Product, User
from .serializers import ProductSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .producer import publish
import random

class ProductViewSet(viewsets.ViewSet):
    def list(self, request): # /api/products
        try:
            products = Product.objects.all()
            serializer = ProductSerializers(products, many=True)
            return Response(serializer.data)
        except:             
            return Response('Error in the server')

    def create(self, request): # /api/products
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def retrive(self, request, pk=None): # /api/products/<str:id>
        product = Product.objects.get(id=pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    def update(self, request, pk=None): # /api/products/<str:id>
        product = Product.objects.get(id=pk)
        serializer = ProductSerializers(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
    
    
    def destroy(self, request, pk=None): # /api/products/<str:id>
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status.HTTP_204_NO_CONTENT)
    
class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id,            
        })
