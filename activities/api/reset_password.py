from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import PasswordResetToken

User = get_user_model()

class ResetPasswordAPI(APIView):

    def post(self, request):
        email = request.data.get("email")
        token = request.data.get("token")
        password = request.data.get("password")

        record = PasswordResetToken.objects.filter(
            email=email,
            token=token
        ).first()

        if not record:
            return Response({"error": "Invalid link"}, status=400)

        if timezone.now() > record.created_at + timedelta(minutes=5):
            record.delete()
            return Response({"error": "Link expired"}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.set_password(password)
        user.save()

        record.delete() 

        return Response({"message": "Password updated"}, status=200)