from rest_framework import serializers

from .models import Benefit, Organization
# from .models import TestModel

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        exclude = ('used_by_user',)
        # fields = '__all__'

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

# class TestModelSerializer(serializers.ModelSerializer):
#     # name = serializers.CharField(required = True)
#     class Meta:
#         model = TestModel
#         fields = '__all__'

    # def create(self, validated_data):
    #     return TestModel.objects.create(**validated_data)