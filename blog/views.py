from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Post, PostEdit
from .serializers import PostCreateSerializer, PostListSerializer, PostEditSerializer
from .utils import IsAuthenticatedAdmin


class PostCreateApiView(CreateAPIView):
    """
    Create a post
    Method post
    Authentication: Token based auth is required <br>

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAdmin]
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"message": "post created",
                            "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "post creation failed",
                            "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class AllPostListApiView(ListAPIView):
    """
    Get all posts
    Method get
    Format Json
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAdmin]
    serializer_class = PostListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('tags__name', 'status', 'pub_date', )
    search_fields = ('title', 'slug', )

    def list(self, request, *args, **kwargs):
        query_set = Post.objects.all()
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return Response({
            "message": "All post list",
            "count": self.paginator.count,
            "next": self.paginator.get_next_link(),
            "previous": self.paginator.get_previous_link(),
            "data": serializer.data,
        }, status=status.HTTP_200_OK)


class PostEditApiView(UpdateAPIView):
    """
    Update a post
    Method put
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAdmin]
    queryset = Post.objects.all()
    serializer_class = PostEditSerializer
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if not instance:
            return Response({"message": "post not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            post = serializer.save()
            PostEdit.objects.create(edited_by=request.user, post=post)
            return Response({"message": "post updated",
                            "data": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "post update failed", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class PostDeleteApiView(DestroyAPIView):
    """
    Delete a post
    Method delete
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAdmin]
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        """
        Delete a post record
        """
        return self.destroy(request, *args, **kwargs)


class PostListApiView(ListAPIView):
    """
    Get only published posts
    """
    serializer_class = PostListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('tags__name', 'status', 'pub_date', )
    search_fields = ('title', 'slug', )

    def list(self, request, *args, **kwargs):
        query_set = Post.published_objects.all()
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return Response({
            "message": "All published post list",
            "count": self.paginator.count,
            "next": self.paginator.get_next_link(),
            "previous": self.paginator.get_previous_link(),
            "data": serializer.data,
        }, status=status.HTTP_200_OK)
