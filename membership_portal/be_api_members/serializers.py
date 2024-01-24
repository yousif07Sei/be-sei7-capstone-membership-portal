from rest_framework import serializers
from .models import Benefit, Organization, PlanFeature, User, Profile, Plan, Event, Interest, Country

# from .models import TestModel
class PlanFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeature
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    plan_feature = PlanFeatureSerializer(many = True)
    class Meta:
        model = Plan
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    country_short_name = serializers.SerializerMethodField()
    country_flag = serializers.SerializerMethodField()
    plan = PlanSerializer()
    plan_name = serializers.SerializerMethodField()
    # plan_feature_name = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id', 'name', 'logo', 'cr_number', 'phone_number', 'email_address', 'sector', 'website', 'address_one', 'address_two', 'city', 'zip_code', 'content_info', 'interests', 'status', 'country', 'country_name', 'country_short_name', 'country_flag', 'plan_id', 'plan', 'plan_name']
    
    def get_country_name(self, obj):
        return obj.country.name if obj.country else None
    
    def get_country_short_name(self, obj):
        return obj.country.short_name if obj.country else None
    
    def get_country_flag(self, obj):
        return obj.country.flag if obj.country else None
    
    def get_plan_name(self, obj):
        return obj.plan.name if obj.country else None
    
    # def get_plan_name(self, obj):
    #     if hasattr(obj, 'plan') and obj.plan is not None and hasattr(obj.plan, 'name') and obj.plan.name is not None:
    #         return obj.plan.name
    #     else:
    #         return None
        
    def get_plan_feature_name(self, obj):
        # get the plan feature
        pass
        # serialize plan feature and return it
        
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
    
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['interest']

class OrganizationRESTSerializers(serializers.Serializer):

    #interests = InterestSerializer(many=True)
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), read_only=False,many=True)
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
    # interests = serializers.ManyRelatedField()

    def get_validation_exclusions(self, *args, **kwargs):
        print("EXCLUDES")
        exclusions = super(OrganizationRESTSerializers, self).get_validation_exclusions()
        return exclusions + ['interests']

    def create(self, validated_data):
        interestsData = validated_data.pop('interests')
        # print('After', validated_data)
        # print("int DATA",interestsData)
        # splitedData = interestsData.split(',')
        # interestsArr = []
        # for i in splitedData:
        #     interestsArr.append(int(i))
        # print("Array HERE!",interestsArr)
        # interests = Interest.objects.filter(**interestsData)
        # print(interests)
        org = Organization.objects.create( **validated_data)
        org.interests.set(interestsData)
        # user = self
        # print("user",user)
        return org
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.cr_number = validated_data.get('cr_number', instance.cr_number)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email_address = validated_data.get('email_address', instance.email_address)
        instance.sector = validated_data.get('sector', instance.sector)
        instance.website = validated_data.get('website', instance.website)
        instance.address_one = validated_data.get('address_one', instance.address_one)
        instance.address_two = validated_data.get('address_two', instance.address_two)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.city = validated_data.get('city', instance.city)
        instance.country_id = validated_data.get('country_id', instance.country_id)
        instance.content_info = validated_data.get('content_info', instance.content_info)

        instance.interests = validated_data.get('interests', instance.interests)

        # interests_data = validated_data.get('interests', [])
        # instance.interests.set(interests_data)
        
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class ProfileRESTSerializers(serializers.Serializer):
    dob = serializers.DateField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phoneNumber = serializers.CharField()
    email = serializers.CharField()
    martial = serializers.CharField()
    nationality = serializers.CharField()
    gender = serializers.CharField()
    job_title = serializers.CharField()

    def create(self, validated_data):
        return Benefit.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.dob = validated_data.get('dob', instance.dob)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
        instance.email = validated_data.get('email', instance.email)
        instance.martial = validated_data.get('martial', instance.martial)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.save()
        return instance

class SignUpProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','image','dob','email','martial','gender','role','nationality_id','status','organization_id','user_id']
        
    def create(self, validated_data):
        User.objects.create()
        return Profile.objects.create(**validated_data)
    
class ProfileSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name','image','dob','email','martial','gender','role','nationality_id','status','organization_id', 'organization_name']
    
    def get_organization_name(self, obj):
        if hasattr(obj, 'organization') and obj.organization is not None and hasattr(obj.organization, 'name') and obj.organization.name is not None:
            return obj.organization.name
        else:
            return None


        
    def create(self, validated_data):
        User.objects.create()
        return Profile.objects.create(**validated_data)
class UserSerializer(serializers.ModelSerializer):
     profile = SignUpProfileSerializer(required = True)
     
     def create(self, validated_data):
        return User.objects.create(**validated_data)
     class Meta:
        model = User
        fields = ['profile', 'username']
    # id = serializers.IntegerField()
    # username = serializers.CharField()
    # profile = serializers.DictField()



class PlanRESTSerializers(serializers.Serializer):
    name = serializers.CharField(required = True)
    price = serializers.IntegerField(required = True)
    member_number = serializers.IntegerField()
    status = serializers.BooleanField()

    def create(self, validated_data):
        return Plan.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.member_number = validated_data.get('member_number', instance.member_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

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
class EventSerializer(serializers.ModelSerializer):
    attendees = ProfileSerializer(many = True)
    class Meta:
        model = Event
        fields = ['id', 'title','description','location','sponsor','start_date','end_date', 'attendees']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'