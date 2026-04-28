from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from .models import User


class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "User created"
            }, status=201)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)


from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login


class LoginAPI(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({
                "status": "error",
                "message": "Invalid credentials"
            }, status=401)

        login(request, user)

        if user.role == "client":
            redirect_url = "/dashboard/client/"

        elif user.role == "employee":
            redirect_url = "/dashboard/employee/"


        elif user.role == "qa":
            redirect_url = "/dashboard/qa/"

        elif user.role == "manager":
            redirect_url = "/dashboard/"

        else:
            redirect_url = "/dashboard/"
        return Response({
            "status": "success",
            "message": "Login success",
            "role": user.role,
            "redirect": redirect_url
        })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
@login_required
def profile_view(request):

    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.mobile = request.POST.get('mobile')
        user.save()

        profile.phone = request.POST.get('phone')
        profile.location = request.POST.get('location')
        profile.bio = request.POST.get('bio')

        profile.designation = request.POST.get('designation')
        profile.department = request.POST.get('department')
        profile.experience = request.POST.get('experience') or None
        profile.skills = request.POST.get('skills')

        profile.company_name = request.POST.get('company_name')
        profile.website = request.POST.get('website')
        profile.industry = request.POST.get('industry')

        if request.FILES.get('photo'):
            new_photo = request.FILES.get('photo')

            if profile.photo:
                profile.photo.delete(save=False)

            profile.photo = new_photo
        profile.save()  
        return redirect('profile_view')

    return render(request, 'frontend/profile.html', {
        'user': user,
        'profile': profile
    })