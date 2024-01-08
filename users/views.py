from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from users.serializers import UserSerializer
from rest_framework import  permissions
from django.contrib.auth import get_user_model
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

User = get_user_model()

@csrf_exempt
@api_view(['GET', 'POST','DELETE', 'PUT'])
@permission_classes([permissions.IsAuthenticated,TokenHasReadWriteScope])
def user(request,id=""):
    q = request.GET.get("q","")
    if request.method == "GET":
        if q != "":
            return filter_user(request,q)
        return get_user(request,id)
    elif request.method == "POST":
        return post_user(request)
    elif request.method == "PUT":
        return update_user(request,id)
    elif request.method == "DELETE":
        return delete_user(id)


def get_user(request,id):
    if id == "":
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
    else:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
    
    return Response(serializer.data,status=status.HTTP_200_OK)

def post_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": "true", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"success": "false", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
def update_user(request,id):
    try:
        user = User.objects.get(id=id)
    except user.DoesNotExist:
        return Response({"success":"false","error":"user does not exists"},status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": "true", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"success": "false", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
def delete_user(id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({"success":"true"},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"success":"false","error":"user does not exists"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"success":"false","error":"unknown error occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def filter_user(request,q):
    try:
        users = User.objects.filter(Q(username__icontains = q) | 
                                    Q(first_name__icontains = q) | 
                                    Q(last_name__icontains = q) | 
                                    Q(email__icontains = q))
    
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
