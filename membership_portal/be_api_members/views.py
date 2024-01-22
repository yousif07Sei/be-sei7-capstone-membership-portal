from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from .models import Benefit, Profile
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
    '''
    Get list of all available benefits
    '''
    try:
        benefit_list = Benefit.objects.all()
        serializer = BenefitSerializer(benefit_list, many = True)
        response = serializer.data
    except ValidationError as e:
        response = e.message
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def benefit_add_user(request):
    '''
    Add specific user to a specific benefit
    '''
    benefit_id = request.data['benefit']
    user_id = request.data['user']
    user = Profile.objects.get(user_id = user_id)
    benefit = Benefit.objects.get(pk = benefit_id)
    try:
        benefit.assign_to_user(user)
        serializer = BenefitSerializer(benefit)
        response = serializer.data
    except ValidationError as e:
        response = e.message
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def benefit_detail(request):
    '''
    Get details of a specific benefit given its id
    '''
    benefit_id = request.query_params['id']
    try:
        benefit = Benefit.objects.get(pk = benefit_id)
        response = BenefitSerializer(benefit).data
    except ObjectDoesNotExist as e:
        response = f"Benefit with id {benefit_id} does not exist."
    except Exception as e:
        response = str(e)
    return JsonResponse(response, safe = False)

# generate QR code api
def benefit_qrcode(request):
    pass