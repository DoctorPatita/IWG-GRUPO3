from django.shortcuts import render, get_object_or_404, redirect
from organization.models import Organization, Member
from organization.forms import CreateOrganizationForm
# Create your views here.

def list_organizations_view(request):
	context = {}
	organizations = Organization.objects.all()
	context['organizations'] = organizations
	return render(request, 'organization/list_organizations.html', context)

def detail_organization_view(request, name):
	context = {}
	organization = get_object_or_404(Organization, name=name)
	num_members = Member.objects.filter(organization=organization).count()
	context['organization'] = organization
	context['num_members'] = num_members
	return render(request, 'organization/detail_organization.html', context)

def add_member_view(request, name):
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')
	
	organization = get_object_or_404(Organization, name=name)
	user = request.user.username
	member = Member(organization=organization, user=user)
	member.save()
	return redirect('http://127.0.0.1:8000/organization/'+name)

def remove_member_view(request, name):
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')
	
	organization = get_object_or_404(Organization, name=name)
	user = request.user.username
	member = Member.objects.filter(user=user)
	member.delete()
	return redirect('http://127.0.0.1:8000/organization/'+name)

def create_organization_view(request):

	context = {}

	form = CreateOrganizationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('organizations_list')
	
	context['form'] = form
	return render(request, 'organization/create_organization.html', context)