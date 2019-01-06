from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (SignUpSerializer, SignInSerializer)
from .renderers import UserJsonRender


class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJsonRender, )

    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignInView(APIView):
    renderer_classes = (UserJsonRender,)
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
