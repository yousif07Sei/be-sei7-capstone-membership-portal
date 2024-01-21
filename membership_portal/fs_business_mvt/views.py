from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from be_api_members.models import Organization , Country , Profile

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
        # Save the updated object
        obj.save()
        return redirect('bussines_portal_app:organization_index')
    
class OrganizationDelete(DeleteView):
    model = Organization
    success_url = '/organization/'

def OrganizationDetail(request,pk):
    organization = Organization.objects.get(id = pk)
    users = Profile.objects.filter(organization = pk)
    
    return render(request,'be_api_members/organization_detail.html' , {'organization':organization, 'users':users})
    
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
    obj =  Profile.objects.get(id=user_id)
    obj.organization = None
    print(obj.organization)
    return redirect('/organization/'+str(organization_id)+'/')