from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=400
        )
    user = User.objects.create_user(
        username=username,
        password=password
    )
    return Response(
        {"message": "User created successfully"},
        status=201
    )