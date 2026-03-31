from rest_framework import viewsets
from .models import PostEducativo
from .serializers import PostEducativoSerializer

class PostEducativoViewSet(viewsets.ModelViewSet):
    queryset = PostEducativo.objects.all()
    serializer_class = PostEducativoSerializer