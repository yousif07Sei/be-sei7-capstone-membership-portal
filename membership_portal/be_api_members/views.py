from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import json
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes, APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from .models import *
# from .models import TestModel

from .serializers import BenefitSerializer, BenefitRESTSerializers, OrganizationSerializer, OrganizationRESTSerializers, UserSerializer, ProfileSerializer
# from .serializers import TestModelSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import parser_classes
# from .serializers import TestModelSerializer
from django.contrib.auth.views import LoginView
import qrcode
import os
from dotenv import load_dotenv
load_dotenv()

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    users = Profile.objects.all()
    serializer = ProfileSerializer(users, many = True)
    return JsonResponse(serializer.data, safe = False)

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
# TODO... modify the function to generate QR link based on frontend url and benefit id
@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def benefit_qrcode(request):
    benefit_url = str(os.getenv('FRONTENDURL'))
    benefit_id = request.query_params['id']
    # if benefit doesnt exist, return an error
    try:
        benefit = Benefit.objects.get(pk = benefit_id)
    except ObjectDoesNotExist as e:
        return JsonResponse({'message': f'Error, benefit with id {benefit_id} does not exist'})
    
    image_dir = settings.MEDIA_ROOT + '/qr/'
    # check if media/qr folder doesnt exist, create it
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    # check if qr code already exists
    if os.path.isfile(image_dir + f'{benefit_id}.png'):
        return JsonResponse({'messge': 'qr code exists'})
    else:
        img = qrcode.make(benefit_url)
        print(benefit_url)
        img.save(image_dir + f'{benefit_id}.png')
        return JsonResponse({'messge': 'qr code saved'})
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def benefit_delete(request):
    benefit_id = request.query_params['id']
    try:
        benefit = Benefit.objects.get(pk = benefit_id)
        benefit.status = '2'
        benefit.save()
        return JsonResponse({'message': f'benefit {benefit_id} has been deleted'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': f'Error: benefit {benefit_id} does not exist'})
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def benefit_create(request):
    # TODO... Validate that expiry date is not older than current date
    # get data from the body
    data = JSONParser().parse(request)
    try:
        organization_id = int(data['organization_id'])
        organization = Organization.objects.get(pk = organization_id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": f"Error: Organization with id {organization_id} does not exist"})
    serializer = BenefitRESTSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse(serializer.errors)

csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def benefit_update(request):
    benefit_id = request.query_params['id']
    try:
        benefit = Benefit.objects.get(pk = int(benefit_id))
    except ObjectDoesNotExist:
        return JsonResponse({'message': f'Error: Cannot find benefit with id {benefit_id}'})
    data = JSONParser().parse(request)
    serializer = BenefitRESTSerializers(benefit, data = data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({'message': 'Error udpating benefit'})

@csrf_exempt
@api_view(['GET'])
def user_details(request):
    email = request.query_params['email']
    profile = get_object_or_404(Profile,email=email)
    username = get_object_or_404(User,id = profile.user_id).username
    # print("user_id", user_id)
    user = get_object_or_404(User,username = username)
    print("profile ", user )
    
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)
# @csrf_exempt
# @api_view(['POST'])
# def LoginAPIView(request):
#     serializer = LoginSerializer(request.data, partial = True)

#     return JsonResponse(serializer.data, safe=False)
    
csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def organization_list(request):
    '''
    Get list of all registered organizations
    '''
    try:
        organization_list = Organization.objects.all()
        serializer = OrganizationSerializer(organization_list, many = True)
        response = serializer.data
    except ValidationError as e:
        response = e.message
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def organization_detail(request):
    '''
    Get details of a specific organization given its id
    '''
    organization_id = request.query_params['id']
    try:
        organization = Organization.objects.get(pk = organization_id)
        # get members of the organization
        # members = Profile.objects.filter(organization_id = organization_id)
        # json_serializer = json.Serializer()
        # members_serialized = json_serializer.serialize(members)
        serializer = OrganizationSerializer(organization).data
        # print('MEMBERS DETAILS=========', members_serialized)
        # serializer['members'] = members_serialized
        response = serializer
    except ObjectDoesNotExist as e:
        response = f"Organization with id {organization_id} does not exist."
    except Exception as e:
        response = str(e)
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def organization_delete(request):
    '''
    Soft delete (hide) an organization from the users
    '''
    organization_id = request.query_params['id']
    try:
        organization = Organization.objects.get(pk = organization_id)
        organization.status = '2'
        organization.save()
        return JsonResponse({'message': f'Organization {organization_id} has been deleted'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': f'Error: organization {organization_id} does not exist'})

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser])
def organization_create(request):
    # Verify that organization does not exist
    org_name = request.data['name']
    if Organization.objects.filter(name__iexact = org_name).exists():
        return JsonResponse({'message': f'Organization {org_name} already exist'})
    serializer = OrganizationRESTSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse(serializer.errors)

csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser])
def organization_update(request):
    organization_id = request.query_params['id']
    try:
        organization = Organization.objects.get(pk = int(organization_id))
    except ObjectDoesNotExist:
        return JsonResponse({'message': f'Error: Cannot find organization with id {organization_id}'})
    serializer = OrganizationRESTSerializers(organization, data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({'message': 'Error udpating organization'})

# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def test_create(request):
#     # get data from the body
#     data = JSONParser().parse(request)
#     serializer = TestModelSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         print('yeeeeey')
#         return JsonResponse(serializer.data, safe = False)
#     # else:
#     #     return JsonResponse({'message': 'Error: failed to create new benefit'})
#     return JsonResponse(serializer, safe=False)