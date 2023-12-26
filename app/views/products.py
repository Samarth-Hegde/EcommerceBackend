from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q

from app.models import Product
from app.serializers import ProductSerializer

@api_view(['GET', 'POST','DELETE', 'PUT'])
@parser_classes([MultiPartParser, FormParser])
def product(request,product_id=""):
    q = request.GET.get("q","")
    if request.method == "GET":
        if q != "":
            return filter_product(request,q)
        return get_product(request,product_id)
    elif request.method == "POST":
        return post_product(request)
    elif request.method == "DELETE":
        return delete_product(request,product_id)
    elif request.method == "PUT":
        return update_product(request,product_id)

def get_product(request,product_id):
    try:
        if product_id == "":
            product = Product.objects.all()
            serializer = ProductSerializer(product,many=True)
        else:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def post_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_product(request,product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_product(request,product_id):
    if product_id == "":
        return Response({"error":"Invalid product"},status=status.HTTP_400_BAD_REQUEST)
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response({"status":"success","message":"product deleted successfully"}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def filter_product(request,q):
    try:
        product = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        serializer = ProductSerializer(product,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def add_to_cart(request):
    pass

def clear_cart(request):
    pass

def place_order(request):
    pass

