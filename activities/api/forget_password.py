from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from accounts.models import PasswordResetToken, PasswordResetRequestLog

User = get_user_model()

class ForgotPasswordAPI(APIView):

    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"message": "If account exists, email sent"}, status=200)

        # 🔥 CHECK LAST REQUEST
        last_request = PasswordResetRequestLog.objects.filter(
            email=email
        ).order_by('-created_at').first()

        # 🚫 IF WITHIN 60 SECONDS → DO NOT SEND AGAIN
        if last_request and (timezone.now() - last_request.created_at) < timedelta(seconds=60):
            return Response({
                "message": "Reset link already sent. Check your email."
            }, status=200)

        # ✅ LOG REQUEST
        PasswordResetRequestLog.objects.create(email=email)

        # DELETE OLD TOKENS
        PasswordResetToken.objects.filter(email=email).delete()

        token = get_random_string(64)

        PasswordResetToken.objects.create(
            email=email,
            token=token
        )

        base_url = request.build_absolute_uri('/').rstrip('/')
        reset_link = f"{base_url}/?email={email}&token={token}"

        # ✅ HTML EMAIL
        html_content = render_to_string("email/reset_password.html", {
            "reset_link": reset_link,
            "user": user
        })

        msg = EmailMultiAlternatives(
            subject="Reset Your Password",
            body="Click the link to reset your password.",
            to=[email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response({"message": "Reset link sent"}, status=200)