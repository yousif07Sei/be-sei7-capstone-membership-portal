from rest_framework import serializers

from .models import Benefit, Organization
# from .models import TestModel

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name']

class BenefitSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()
    class Meta:
        model = Benefit
        # exclude = ('used_by_user',)
        # fields = '__all__'
        fields = ['id', 'organization', 'organization_name', 'title', 'description', 'created_date', 'expiry_date', 'status', 'used_by_user']

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None

class BenefitRESTSerializers(serializers.Serializer):
    organization_id = serializers.IntegerField()
    description = serializers.CharField(required = True)
    title = serializers.CharField(required = True)
    expiry_date = serializers.DateField()
    status = serializers.CharField()

    def create(self, validated_data):
        return Benefit.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.title = validated_data.get('title', instance.title)
        instance.expiry_date = validated_data.get('expiry_date', instance.expiry_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

# class TestModelSerializer(serializers.ModelSerializer):
#     # name = serializers.CharField(required = True)
#     class Meta:
#         model = TestModel
#         fields = '__all__'

    # def create(self, validated_data):
    #     return TestModel.objects.create(**validated_data)