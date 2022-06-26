from rest_framework.generics import CreateAPIView

from accounts.models import User
from .serializers import SignUpSerializer


class SignUpApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
