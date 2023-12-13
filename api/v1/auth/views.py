from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LogInSerializer, SignUpSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SignUpView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignUpSerializer(),
        responses={201: "User Created Successfully!", 400: "Invalid input"}
    )
    def post(self, request):
        """
        Register a new user.

        This endpoint allows the registration of a new user.
        """
        data = request.data

        context = {}

        serializer = SignUpSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            context['message'] = "User Created Successfully!"

            return Response(context, status=status.HTTP_201_CREATED)

        context['message'] = serializer.errors
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LogInSerializer(),
        responses={200: "Logged in successfully!", 401: "Unauthorized"}
    )
    def post(self, request):
        """
        Log in a user.

        This endpoint allows the user to log in.
        """
        data = request.data

        serializer = LogInSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response({'message': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Successfully logged out!", 400: "Bad request", 404: "Token is invalid!"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def post(self, request):
        """
        Logout a user.

        This endpoint logs out the user by blacklisting the refresh token.
        """
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"message": "refresh token is missing!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': "Successfully LoggedOut!"})
        except:
            return Response({"message": "token is invalid!"}, status=status.HTTP_404_NOT_FOUND)
