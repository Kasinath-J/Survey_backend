from rest_framework import serializers
from .models import Layout

#Used for updating tasks regurlarly
class LayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layout
        fields = ['id','format','gsheetId','title']

