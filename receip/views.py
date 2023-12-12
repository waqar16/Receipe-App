from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import *

def receip_view(request):
    if request.method == "POST":
        return _extracted_from_receip_view_3(request)
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
    context = {'queryset':queryset }
    return render(request, 'receipe/receipe.html', context)


# TODO Rename this here and in `receip_view`
def _extracted_from_receip_view_3(request):
    data = request.POST
    receipe_name = data.get('receipe_name')
    receipe_decription = data.get('receipe_description')
    receipe_image = request.FILES.get('receipe_image')

    Receipe.objects.create(receipe_name=receipe_name, receipe_decription=receipe_decription, receipe_image=receipe_image)
    return redirect('/')


def delete_item(request, id):
    if request.method == "POST":
        return _extracted_from_receip_view(request)
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/') 
def _extracted_from_receip_view(request):
    data = request.POST
    receipe_name = data.get('receipe_name')
    receipe_decription = data.get('receipe_description')
    receipe_image = request.FILES.get('receipe_image')

    
    return redirect('/')

def update_item(request, id):
    queryset = Receipe.objects.get(id=id)
    if request.method == "POST":
        return _extracted_from_update_item_4(request, queryset)
    context = {'queryset':queryset }
    return render(request, 'receipe/update_receipe.html', context)


# TODO Rename this here and in `update_item`
def _extracted_from_update_item_4(request, queryset):
    data = request.POST
    receipe_name = data.get('receipe_name')
    receipe_decription = data.get('receipe_description')
    receipe_image = request.FILES.get('receipe_image')


    queryset.receipe_name = receipe_name
    queryset.receipe_decription = receipe_decription
    if receipe_image:
        queryset.receipe_image = receipe_image
    queryset.save()
    return redirect('/')