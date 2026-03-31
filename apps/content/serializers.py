from rest_framework import serializers
from .models import PostEducativo

class PostEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostEducativo
        fields = '__all__'