from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from be_api_members.models import Organization , Country

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
    

class CountryList(ListView):
    model = Country