from django.shortcuts import render
from .models import Link
from .forms import LinkForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
# Create your views here.
def link_page(request):
    return render(request, 'linkstore/main_page.html', {})

def recent_link(request):
    links=Link.objects.filter(owner=request.user)
    recent_links = links.order_by('access_date').reverse()
    return render(request, 'linkstore/recent_link.html', {'recent_links':recent_links})

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
    return render(request, 'linkstore/link_form.html', {'form': form})

def form_edit(request,pk):
    post = get_object_or_404(Link,pk=pk)
    if request.method == "POST":
        form = LinkForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.access_date = timezone.now()
            post.save()
            return redirect('recent_link')
    else:
        form = LinkForm(instance=post)
    return render(request, 'linkstore/link_form.html', {'form': form})


# def Logout(request):
#     logout(request)
#     return HttpResponseRedirect('linkstore/index.html')