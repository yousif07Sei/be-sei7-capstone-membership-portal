from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from be_api_members.models import Organization , Country , Plan, PlanFeature , Profile , Event
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.db.models import Q
from django import forms
from django.forms import ModelForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from datetime import datetime

# Create your views here.
def home(request):
    return render(request ,'home.html')

class OrganizationList(ListView):
    model = Organization

class OrganizationUpdate(UpdateView):
    model = Organization
    fields = '__all__'
    success_url = '/organization/'
    def post(self, request, pk, *args,**kwargs):
        obj = get_object_or_404(Organization, pk=pk)

        # Update the object with the new data
        obj.name = request.POST.get('name')
        if 'logo' in request.FILES:
            obj.logo = request.FILES['logo']
            
        # obj.logo = request.POST.get('logo')
        obj.phone_number = request.POST.get('phone_number')
        obj.email_address = request.POST.get('email_address')
        obj.sector = request.POST.get('sector')
        obj.website = request.POST.get('website')
        obj.address_one = request.POST.get('address_one')
        obj.address_two = request.POST.get('address_two')
        obj.country = Country.objects.get(pk=request.POST.get('country'))
        obj.zip_code = request.POST.get('zip_code')
        obj.content_info = request.POST.get('content_info')
        obj.interests = request.POST.get('interests')
        obj.status = request.POST.get('status')
        # Save the updated object
        obj.save()
        return redirect('bussines_portal_app:organization_index')
    
 # Yousif added the plan views
class PlanList(ListView):
    model=Plan


class PlanDetail(DetailView):
    model=Plan
    


class PlanCreate(CreateView):
    model= Plan
    fields= '__all__'
    success_url = '/plan/'

    def get_context_data(self, **kwargs):
        print("some")
        context = super().get_context_data(**kwargs)
        plan_feature_list = PlanFeature.objects.all()
        print(plan_feature_list)
        context["planfeature"] = plan_feature_list
        return context



class PlanUpdate(UpdateView):
    model= Plan
    fields= '__all__'
    
    def get_context_data(self, **kwargs):
        print("some")
        context = super().get_context_data(**kwargs)
        plan_feature_list = PlanFeature.objects.all()
        print(plan_feature_list)
        context["planfeature"] = plan_feature_list
        return context
    



class PlanDelete(DeleteView):
    model= Plan
    success_url = '/plan/'
   
    
class OrganizationDelete(DeleteView):
    model = Organization
    success_url = '/organization/'

def OrganizationDetail(request,pk):
    organization = Organization.objects.get(id = pk)
    users = Profile.objects.filter(organization = pk)
    usersList = []
    print(users[0].status)
    for i in users:
        if i.status != 2:
            usersList.append(i)
            
    return render(request,'be_api_members/organization_detail.html' , {'organization':organization, 'users':usersList})
    
class ProfileUpdate(UpdateView):
    model = Profile
    fields = '__all__'
    success_url = "/organization/"
    def post(self,request,pk):
        obj = get_object_or_404(Profile,pk=pk)
        
        obj.first_name = request.POST.get('first_name')
        obj.last_name = request.POST.get('last_name')
        obj.martial = request.POST.get('martial')
        obj.nationality = Country.objects.get(pk=request.POST.get('nationality'))
        obj.gender = request.POST.get('gender')
        obj.job_title = request.POST.get('job_title')
        obj.status = request.POST.get('status')
        if 'image' in request.FILES:
            obj.image = request.FILES['image']
        # obj. = request.POST.get('')
        obj.save()
        return redirect('/organization/'+request.POST.get('orgId')+'/')
class ProfileList(ListView):
    model = Profile
class CountryList(ListView):
    model = Country

def remove_member(request,user_id,organization_id):
    # Profile.objects.filter(id=user_id).values()[0]
    obj = get_object_or_404(Profile,pk=user_id)
    # Profile.objects.get(id=user_id).organization = None
    obj.status = 2
    obj.save()
    # print(Profile.objects.get(id=user_id).organization)
    print(obj.organization)
    return redirect('/organization/'+str(organization_id)+'/')

class EventList(ListView):
    model=Event


class EventDetail(DetailView):
    model=Event
    

# def add_event(request, event_id):
#     event_form = EventForm(request.POST)

#     if event_form.is_valid():
#         new_event = event_form.save(commit=False)
#         new_event.event_id = event_id
#         new_event.save()
        # return redirect('cats_detail', cat_id)
   


class EventCreate(CreateView):
    model = Event
    fields = '__all__'
    
    template_name = 'be_api_members/event_form.html'  # replace with your actual template name
    success_url = '/events/'  # replace with your actual success URL 
    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DateTimePickerInput()
        form.fields['end_date'].widget = DateTimePickerInput(range_from="start_date")
        return form



class EventUpdate(UpdateView):
    model= Event
    fields= ['title','description','location','sponsor','start_date','end_date']
    success_url = '/events/'
    
    



class EventDelete(DeleteView):
    model= Event
    success_url = '/events/'

class ManageLogin(LoginView):
    template_name = 'fs_business_mvt/templates/registration/login.html'
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = get_object_or_404(User,username = username)
        profile = get_object_or_404(Profile,user_id = user.id)
        print("user",profile.first_name)
        if profile.role <= 2:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    