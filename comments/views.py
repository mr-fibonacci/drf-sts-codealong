from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentDetailSerializer, CommentSerializer


class CommentList(generics.ListCreateAPIView):
    """
    List all comments
    Create a new comment if authenticated
    Associate the current logged in user with the comment
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# IN GENERICS, REQUEST PASSED IN BY DEFAULT AS PART OF CONTEXT
    # def get_serializer_context(self):
    #     context = super(CommentList, self).get_serializer_context()
    #     context.update({'request': self.request})
    #     return context


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment
    update or delete a comment if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

# IN GENERICS, REQUEST PASSED IN BY DEFAULT AS PART OF CONTEXT
    # def get_serializer_context(self):
    #     context = super(CommentDetail, self).get_serializer_context()
    #     context.update({'request': self.request})
    #     return context
