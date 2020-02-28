from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import auth
from .forms import RegistrationForm, AddMedForm
from .models import Sickness, MedicalInformation
from .choices import duration_choices, sickness_choices


def index(request):
    return render(request, 'accounts/index.html')

def statistics(request):
    if request.user.is_authenticated:
        if request.user.medical_practitioner == "YES":
            queryset_list = MedicalInformation.objects.all()

            if 'sickness' in request.GET:
                sickness = request.GET['sickness']
                if sickness:
                    queryset_list = queryset_list.filter(sickness__id__iexact=sickness)

            if 'duration' in request.GET:
                duration = request.GET['duration']
                if duration:
                    queryset_list = queryset_list.filter(duration__iexact=duration)

            context = {
                'result': queryset_list,
                'duration_choices': duration_choices,
                'sickness_choices': sickness_choices
            }

            return render(request, 'accounts/statistics.html', context)
        else:
            return redirect('homepage')
    else:
        return redirect('homepage')

def medicalRecords(request):
    records = MedicalInformation.objects.all()

    context = {
        'result': records
    }

    return render(request, 'accounts/records.html', context)

def registration_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        context = {}
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                auth.login(request, account)
                return redirect('homepage')
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, "accounts/register.html", context)

def login(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.POST:
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('homepage')
            else:
                return redirect('login')
        else:
            return render(request, 'accounts/login.html')

def logout(request):
    if request.user.is_authenticated:
        if request.POST:
            auth.logout(request)
            return redirect('homepage')
    else:
        return redirect('homepage')

def addrecord(request):
    if request.user.is_authenticated:
        template = 'accounts/addmedrecord.html'
        form = AddMedForm(request.POST or None)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('records')
        else:
            form = AddMedForm()

        context = {
            'form': form,
        }
        return render(request, template, context)
    else:
        return redirect('login')

def about(request):
    return render(request, 'accounts/about.html')

def help(request):
    return render(request, 'accounts/help.html')
    