from atexit import register
import profile
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import Account
from server.models import Profile

#creating a Account serializer which will get the details from models.py
class AccountSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(default=0)
    profile = serializers.CharField(max_length=200)
    user = serializers.CharField(max_length=200)
    class Meta:
        model = Account
        fields = ['role', 'user', 'profile']

#Serializer to view the username and email id.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

