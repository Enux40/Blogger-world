from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse_lazy

from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        # get user form
        form = UserRegisterForm(request.POST)

        # validate form
        if form.is_valid():
            # get username
            username = form.cleaned_data.get('username')

            # save the user data to database
            form.save()

            # toast success
            messages.success(request, f'Hi {username}, Your Account has been created. You are now able to login.')

            # send to login page
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class MyLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        # get logged in user username
        username = self.request.user.username

        # redirect them their posts
        next_url = reverse_lazy('home', kwargs={'username': username})
        return next_url


class MyLogoutView(auth_views.LogoutView):
    template_name = 'logout.html'

    def get(self, request):
        # logout
        logout(request)

        # redirect to home
        return redirect('home')

    
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)

