from rest_framework import serializers
from .models import Project, Service, ProjectService


class ProjectSerializer(serializers.ModelSerializer):

    services = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "client",
            "services",
            "start_date",
            "created_at",
        ]

    def get_services(self, obj):
        return list(
            obj.project_services.values_list("service_id", flat=True)
        )

    def validate(self, data):
        if not data.get("client"):
            raise serializers.ValidationError("Client is required")
        return data

    def create(self, validated_data):
        services = self.initial_data.get("services", [])

        project = Project.objects.create(**validated_data)

        for service_id in services:
            ProjectService.objects.create(
                project=project,
                service_id=service_id
            )

        return project