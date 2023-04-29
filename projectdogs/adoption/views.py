from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .models import Pet,AdoptionApplication
from .forms import PetForm,PetUpdateForm,ImageUpdateForm,SearchForm,AdoptionApplicationForm
from django.views.generic.base import View

@login_required
def adoption_feed(request):
    pets = Pet.objects.all()
    return render(request, 'adoption/adoption_feed.html', {'pets': pets}) 


class adoptionCreateView(CreateView):
    model=Pet
    fields = ['name','breed','age','gender','location', 'description', 'photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class adoptionListView(ListView):
    model=Pet
    template_name='adoption/adoption_feed.html' # <app>/<model>_<viewtype>.html
    context_object_name='pets'
    ordering=['-adoption_date']


class adoptionDetailView(DetailView):
    model=Pet
    template_name='adoption/adoption_detail.html' # <app>/<model>_<viewtype>.html


@login_required
def adoption_application(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.author == request.user:
        messages.warning(request, 'You cannot adopt your own pet!')
        return redirect('adoption-detail', pk=pk)

    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            adoption_application = form.save(commit=False)
            adoption_application.pet = pet
            adoption_application.author = request.user
            adoption_application.save()
            messages.success(request, 'Your adoption application has been submitted successfully.')
            return redirect('adoption_feed')
    else:
        form = AdoptionApplicationForm()

    return render(request, 'adoption/adoptionapplication_form.html', {'form': form})

    

    
class AdoptionApplicationListView(ListView):
    model = AdoptionApplication
    context_object_name = 'applications'
    template_name = 'adoption_application_list.html'

@login_required
def adoption(request):
    pets = Pet.objects.all()
    query = request.GET.get('q')
    if query:
        pets = pets.filter(
            Q(name__icontains=query) |
            Q(breed__icontains=query) |
            Q(location__icontains=query)
        ).distinct()

    search_form = SearchForm()
    return render(request, 'adoption/adoption_feed.html', {'pets': pets, 'search_form': search_form})

class SearchView(View):
    def get(self, request):
        form = SearchForm()
        return render(request, 'adoption/search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            pets = Pet.objects.filter(name__icontains=query)
            return render(request, 'adoption/search_results.html', {'pets': pets, 'query': query})
        return render(request, 'adoption/search.html', {'form': form})