from django.shortcuts import render
from .models import Link
from .forms import LinkForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

@login_required
def link_page(request):
    return render(request, 'linkstore/main_page.html', {})

@login_required
def recent_link(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(link__icontains=query) | Q(description__icontains=query) \
                      | Q(category__icontains=query)
            links = Link.objects.filter(lookups).distinct()
            context = {'recent_links': links,
                       'active': 'recent_links'}

            return render(request, 'linkstore/recent_link.html', context)

    links = Link.objects.filter(owner=request.user)
    recent_links = links.order_by('access_date').reverse()[:5]
    return render(request, 'linkstore/recent_link.html', {'recent_links': recent_links,
                                                          'active': 'recent_links'})
@login_required
def add_link(request):
    if request.method == "POST":
        form = LinkForm(request.POST)        
        if form.is_valid():
            #print("Reqyest User --> ",request.user)
            post = form.save(commit=False)
            post.access_date = timezone.now()
            post.owner = request.user
            post.save()
            return redirect('recent_link')
    else:
        form = LinkForm()
    return render(request, 'linkstore/link_form.html', {'form': form,
                                                        'active': 'add_link',
                                                        'header': "Add Link"})
@login_required
def form_edit(request,pk):
    post = get_object_or_404(Link, pk=pk)
    if request.method == "POST":
        form = LinkForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.access_date = timezone.now()
            post.save()
            return redirect('recent_link')
    else:
        form = LinkForm(instance=post)
    return render(request, 'linkstore/link_form.html', {'form': form,
                                                        'header': "Edit Link"
                                                        })
@login_required
def delete_link(request,pk):
    link = get_object_or_404(Link, pk=pk)
    link.delete()
    return redirect('recent_link')

@login_required
def category_link(request, category):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(link__icontains=query) | Q(description__icontains=query) \
                      | Q(category__icontains=query)
            links = Link.objects.filter(lookups).distinct()
            context = {'recent_links': links,
                       'active': 'category_links',
                       'active_category': category,}
            return render(request, 'linkstore/links.html', context)
    links = Link.objects.filter(owner=request.user)
    if category != 'all' and category != 'favorites':
        links = links.filter(category=category)
    elif category == 'favorites':
        links = links.filter(favorite=True)

    return render(request, 'linkstore/links.html', {'recent_links': links,
                                                    'active_category': category,
                                                    'active': 'category_links'})




# def Logout(request):
#     logout(request)
#     return HttpResponseRedirect('linkstore/index.html')