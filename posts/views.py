from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Post
from .serializers import PostSerializer


# Create your views here.
def index(request):
    return render(request, "posts/index.html")


class PostsViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        posts = Post.objects.order_by("-created_at")[:5]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
