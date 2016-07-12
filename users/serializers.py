from rest_framework import serializers
from models import User
from search.custom_serializers import TextAsJsonField


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    short_name = serializers.CharField(source="get_short_name", read_only=True)

    module_access = TextAsJsonField()

    class Meta:
        model = User
        fields = ("email", "short_name", "full_name",
                  'first_name', 'last_name',)
