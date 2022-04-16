from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from server.models import Account
from .serializers import UserSerializer, GroupSerializer, AccountSerializer
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# class RoleViewSet(viewsets.ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = RoleSerializer


class AccountViews(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        if id:
            item = Account.objects.get(id=id)
            serializer = AccountSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Account.objects.all()
        serializer = AccountSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = Account.objects.get(id=id)
        serializer = AccountSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Account, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
