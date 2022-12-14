from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.views.generic import View

Agent = get_user_model()


# ..................... All Houses ......................................
class HouseList(ListView):
    model = House
    context_object_name = 'houses'
    template_name = '../templates/index.html'


# ..................... House details ......................................
class HouseDetail(DetailView):
    model = House
    context_object_name = 'house'
    template_name = '../templates/detail.html'


# ..................... Agent profile ......................................
class AgentProfile(DetailView):
    model = Agent
    template_name = '../templates/profile.html'
    context_object_name = 'agent'

    def get_object(self):
        pk = self.kwargs.get('pk')
        agent = Agent.objects.get(username=pk)
        return agent

    def get_context_data(self, **kwargs):
        context = super(AgentProfile, self).get_context_data()
        pk = self.kwargs.get('pk')
        context['agent'] = Agent.objects.get(username=pk)
        context['houses'] = context['agent'].house_set.all()
        return context


# ..................... Profile Update ......................................
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Agent
    form_class = AgentUpdateForm
    template_name = '../templates/profile_update.html'
    login_url = 'login'

    def get_object(self):
        pk = self.kwargs.get('pk')
        agent = Agent.objects.get(username=pk)
        return agent

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect('profile', pk=self.request.user.username)
        return super(ProfileUpdate, self).form_valid(form)


# ..................... House Update ......................................
class HouseUpdate(LoginRequiredMixin, UpdateView):
    model = House
    template_name = '../templates/edit.html'
    form_class = HouseForm
    login_url = 'login'
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect('profile', pk=self.request.user.username)
        return super(HouseUpdate, self).form_valid(form)


# ..................... House Create ......................................
class HouseCreate(LoginRequiredMixin, CreateView):
    model = House
    template_name = '../templates/create.html'
    form_class = HouseForm
    login_url = 'login'
    # fields = '__all__' can not be used because of no exclude attribute
    
    def form_valid(self, form):
        if form.is_valid():
            form.save(commit=False)
            form.instance.agent = self.request.user
            form.save()
            return redirect('profile', pk=self.request.user.username)
        return super(HouseCreate, self).form_valid(form)


# ..................... House Delete ......................................
class HouseDelete(LoginRequiredMixin, DeleteView):
    model = House
    template_name = '../templates/delete.html'
    login_url = 'login'

    def form_valid(self, form):
        if form.is_valid():
            pk = self.kwargs.get('pk')
            house = House.objects.get(id=pk)
            house.delete()
            return redirect('profile', pk=self.request.user.username)
        return super(HouseDelete, self).form_valid(form)


# ..................... Login User ......................................
class LoginUser(LoginView):

    template_name = '../templates/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


# ..................... SignUp User ......................................
class SignUpUser(CreateView):
    form_class = AgentCreationForm
    success_url = reverse_lazy('login')
    template_name = '../templates/signup.html'

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.username = agent.username.lower()
        agent = form.save()
        
        if agent is not None:
            login(self.request, agent)
            return redirect('login')
        return super(SignUpUser, self).form_valid(form)


# ..................... About page ......................................
# class AboutPage(View):
#     # model = House
#     template_name = '../templates/about.html'

def about_page(request):
    context = {}
    return render(request, 'about.html', context)


# ..................... Properties page ......................................
# class PropertyPage(ListView):
#     model = House
#     template_name = '../templates/property.html'

def property_page(request):
    context = {}
    return render(request, 'properties.html', context)


# ..................... Contact page ......................................
# class ContactPage(View):
#     model = House
#     template_name = '../templates/contact.html'

def contact_page(request):
    context = {}
    return render(request, 'contact.html', context)
