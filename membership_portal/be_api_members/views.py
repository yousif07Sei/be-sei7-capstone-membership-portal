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

from rest_framework.response import Response
import random
from .serializers import BenefitSerializer, BenefitRESTSerializers, CountrySerializer, OrganizationSerializer, OrganizationRESTSerializers, PlanRESTSerializers, PlanSerializer, ProfileRESTSerializers, UserSerializer, ProfileSerializer, EventSerializer

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
    Get list of all active benefits
    '''
    try:
        benefit_list = Benefit.objects.filter(status = 1, expiry_date__gte = timezone.now().date())
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

@csrf_exempt
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
def user_detail(request):
    email = request.query_params['email']
    profile = get_object_or_404(Profile,email=email)
    username = get_object_or_404(User,id = profile.user_id).username
    # print("user_id", user_id)
    user = get_object_or_404(User,username = username)
    print("profile ", user )
    
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def user_create(request):
    password = request.data.get('password')
    email = request.data.get('email')
    if Profile.objects.filter(email=email).exists():
        return JsonResponse({"response":"fail"})
    role = 3
    dob = request.data.get('dob')
    martial = request.data.get('martial')
    gender = request.data.get('gender')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    image = ""
    job_title = ""
    phoneNumber = request.data.get('phoneNumber')
    randInt = random.randint(1000,9999)
    username = first_name+"-"+last_name+str(randInt)
    # Create user
    user = User.objects.create_user(username=username, password=password)
    data = Profile.objects.create(email=email, user=user, role=role, first_name=first_name, last_name=last_name,dob=dob,martial=martial,gender=gender, image=image, job_title=job_title, phoneNumber=phoneNumber)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_update(request):
    user_id = request.query_params['id']
    try:
        user = Profile.objects.get(pk = int(user_id))
    except ObjectDoesNotExist:
        return JsonResponse({'message': f'Error: Cannot find user with id {user_id}'})
    data = JSONParser().parse(request)
    serializer = ProfileRESTSerializers(user, data = data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({'message': 'Error udpating user'})
    # return Response({'access_token': access_token, 'refresh_token': str(refresh) }, status=status.HTTP_201_CREATED)
    
# @csrf_exempt
# @api_view(['POST'])
# def user_create(request):
#     data = JSONParser.parse(request)
#     serializer = UserSerializer(data=data)
#     return JsonResponse(data)
    # fn = request.body.first_name
    # ln = request.body.last_name
    # email = request.body.email
    # password = request.body.password
    
# @csrf_exempt
# @api_view(['POST'])
# def LoginAPIView(request):
#     serializer = LoginSerializer(request.data, partial = True)

#     return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def organization_list(request):
    '''
    Get list of all registered organizations 
    '''
    try:
        organization_list = Organization.objects.filter(status = 1).order_by('name')
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
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def organization_members(request):
    '''
    Get list of members that belong to an organization
    '''
    organization_id = request.query_params['id']
    members = Profile.objects.filter(organization_id = organization_id, status = 1)
    serializer = ProfileSerializer(members, many = True)
    return JsonResponse(serializer.data, safe = False)

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
    print("HERE!")
    userID = request.data['user_id']
    serializer = OrganizationRESTSerializers(data=request.data)
    if serializer.is_valid():
        print("valid",serializer)
        serializer.save()
        print("org",org_name)
        profile = get_object_or_404(Profile,user_id=userID)
        org = get_object_or_404(Organization,name=org_name)
        profile.organization_id = org.id
        profile.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        print("not valid",serializer)
        return JsonResponse(serializer.errors)

@csrf_exempt
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

csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def plan_list(request):
    '''
    Get list of all plans
    '''
    try:
        plan_list = Plan.objects.all()
        serializer = PlanSerializer(plan_list, many = True)
        response = serializer.data
    except ValidationError as e:
        response = e.message
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def plan_create(request):
    data = JSONParser().parse(request)
    serializer = PlanRESTSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def plan_update(request):
    plan_id = request.query_params['id']
    try:
        plan = Plan.objects.get(pk = int(plan_id))
    except ObjectDoesNotExist:
        return JsonResponse({'message': f'Error: Cannot find plan with id {plan_id}'})
    data = JSONParser().parse(request)
    serializer = PlanRESTSerializers(plan, data = data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({'message': 'Error udpating plan'})

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
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def event_list(request):
    '''
    Get list of all Events
    '''
    try:
        event_list = Event.objects.all()
        serializer = EventSerializer(event_list, many = True)
        response = serializer.data
    except ValidationError as e:
        response = e.message
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def event_add_user(request):
    '''
    Add specific user to a specific event
    '''
    event_id = request.data['event']
    user_id = request.data['user']
    user = Profile.objects.get(user_id = user_id)
    event = Event.objects.get(pk = event_id)
    try:
        event.assign_to_user(user)
        serializer = EventSerializer(event)
        response = serializer.data
    except ValidationError as e:
        response = e.message
    return JsonResponse(response, safe = False)

@csrf_exempt
@api_view(['GET'])
def country_list(request):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many = True)
    return JsonResponse(serializer.data, safe = False)
