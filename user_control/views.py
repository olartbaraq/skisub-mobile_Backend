from .serializers import User, SignUpSerializer, LoginSerializer, UpdatePasswordSerializer, DeleteUserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class SignUpView(generics.GenericAPIView):
    """The class that represents the sign up api view

    Args:
        generics (_type_): _description_
    """

    serializer_class = SignUpSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [' fullname']


    @swagger_auto_schema(
            operation_summary= "Create a User"
    )
    def post(self, request: Request):
        """post method that handle the sign up request

        Args:
            request (Request): _description_
        """

        data = request.data
        valid_request = self.serializer_class(data=data)

        if valid_request.is_valid():
            valid_request.save()

            response = {
                "message": "User created successfully",
                "data": valid_request.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=valid_request.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(generics.GenericAPIView):
    """This class represents the login api view

    Args:
        APIView (_type_): _description_
    """

    serializer_class = LoginSerializer
    permission_classes = []


    @swagger_auto_schema(
            operation_summary= "Login a User"
    )
    def post(self, request: Request):
        """post method to authenticate the user

        Args:
            request (Request): _description_
        """


        data = request.data
        valid_request = self.serializer_class(data=data)
        valid_request.is_valid(raise_exception=True)

        email = valid_request.validated_data.get('email')
        password = valid_request.validated_data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            response = {
                "message": "User Authentication Successful",
                "data": {
                    "email": user.email,
                    "fullname": user.fullname,
                    "mobile": user.mobile,
                    "account_number": user.account_number
                },
                "Authorization": f"Token {user.auth_token.key}"
            }

            return Response(data=response, status=status.HTTP_202_ACCEPTED)
        
        error_response = {
            "message": "Invalid email or password"
        }

        return Response(data=error_response, status=status.HTTP_401_UNAUTHORIZED)
    

class GetUserView(generics.GenericAPIView):
    """This class represents the login api view

    Args:
        APIView (_type_): _description_
    """

    serializer_class = LoginSerializer
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(
            operation_summary= "Check Individual user with their authorization token, Only by Admin permission"
    )
    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "token": str(request.auth)
        }

        return Response(data=content, status=status.HTTP_200_OK)
    
    
class UpdatePasswordView(generics.GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        user = User.objects.filter(email = valid_request.validated_data["email"])
        
        if not user:
            return Response(
            {"error": "User not found"},
            status=status.HTTP_400_BAD_REQUEST
            )
        
        user = user[0]
        user.set_password(valid_request.validated_data["password"])
        user.save()
         
        return Response(
            {"message": "User password changed successfully"},
            status=status.HTTP_200_OK
        )
        

class DeleteUserView(generics.GenericAPIView):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """
    serializer_class = DeleteUserSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request):
        """method to delete a user

        Args:
            request (Request): _description_
        """
        
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        user = User.objects.filter(email = valid_request.validated_data["email"])
        
        if not user:
            #raise Exception("User not found")
        
            return Response(
            {"error": "User not found"},
            status=status.HTTP_400_BAD_REQUEST
            )
        
        user = user[0]
        user.delete()
         
        return Response(
            {"message": "User account deleted successfully"},
            status=status.HTTP_200_OK
        )