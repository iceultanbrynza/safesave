from django.shortcuts import render, redirect
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Create your views here.

def login_page(request: HttpRequest):
    return render(request, "auth/loginpage.html")

class LoginView(APIView):
    def post(self, request: HttpRequest):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, email=email, password=password)
        print(user)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        response = redirect("home")
        # response = Response("Successful login")
        response.set_cookie("access", str(refresh.access_token), httponly=True)
        response.set_cookie("refresh", str(refresh), httponly=True)
        return response

class LogoutView(APIView):
    def post(self, request: HttpRequest):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

            except TokenError:
                pass

        response = redirect("loginpage")
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response