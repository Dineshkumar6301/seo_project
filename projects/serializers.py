from rest_framework import serializers
from .models import Project, Service


class ProjectSerializer(serializers.ModelSerializer):

    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'client',
            'services',
            'start_date',
            'status',
            'created_at'
        ]

    def validate(self, data):
        if not data.get('client'):
            raise serializers.ValidationError("Client is required")
        return data

    def create(self, validated_data):
        services = validated_data.pop('services')
        project = Project.objects.create(**validated_data)
        project.services.set(services)
        return project