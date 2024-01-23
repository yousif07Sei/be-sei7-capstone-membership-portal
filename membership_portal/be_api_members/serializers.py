from rest_framework import serializers

from .models import Benefit, Organization, User, Profile
# from .models import TestModel

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

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
    
class OrganizationRESTSerializers(serializers.Serializer):
    # NOT IMPLEMENTED
    name = serializers.CharField(required = True)
    logo = serializers.ImageField(required = False)
    cr_number = serializers.CharField(required = True)
    phone_number = serializers.CharField(required = True)
    email_address = serializers.EmailField(required = True)
    sector = serializers.CharField(required = True)
    website = serializers.CharField()
    address_one = serializers.CharField()
    address_two = serializers.CharField()
    zip_code = serializers.IntegerField()
    city = serializers.CharField(required = True)
    country_id = serializers.IntegerField(required = True)
    content_info = serializers.CharField(required = True)
    interests = serializers.CharField()

    def create(self, validated_data):
        return Organization.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.title = validated_data.get('title', instance.title)
        instance.expiry_date = validated_data.get('expiry_date', instance.expiry_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = Profile
        fields = ['first_name', 'last_name','image','dob','email','martial','gender','role','nationality_id','status','organization_id']
        
class UserSerializer(serializers.ModelSerializer):
     profile = ProfileSerializer(required = True)
     class Meta:
        model = User
        fields = ['profile', 'username']
    # id = serializers.IntegerField()
    # username = serializers.CharField()
    # profile = serializers.DictField()
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only = True)

# class TestModelSerializer(serializers.ModelSerializer):
#     # name = serializers.CharField(required = True)
#     class Meta:
#         model = TestModel
#         fields = '__all__'

    # def create(self, validated_data):
    #     return TestModel.objects.create(**validated_data)