from django.shortcuts import render, get_object_or_404

from blog.models import Post

# home page
def home(request):
    # check if user is auntheticated
    if request.user.is_authenticated:
        # render the user_home page
    
        context = {
        # pass all blog posts
        'posts': Post.objects.all,
        }

        # return home page
        return render(request, 'home.html', context)
    else:
        # return welcome page
        return render(request, 'login.html')

# about page
def about(request):
    return render(request, 'about.html')
