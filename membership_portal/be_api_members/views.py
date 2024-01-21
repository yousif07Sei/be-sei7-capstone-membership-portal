from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from .models import Benefit
from .serializers import BenefitSerializer

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    return JsonResponse({'test': 'test'})

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def benefit_list(request):
    benefit_list = Benefit.objects.all()
    serializer = BenefitSerializer(benefit_list, many = True)
    return JsonResponse(serializer.data, safe = False)

# add user api
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def benefit_add_user(request):
    # request.benefitid and request.userid
    # get the benefit id from request
    
    return JsonResponse({'test': request.body.name})
    # find the benefit from db

    # use benefit.assign_to_user function
    pass

# generate QR code api