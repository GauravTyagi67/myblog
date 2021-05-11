from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create HTML Pages
def home(request):
    return render(request,"home/home.html")

def about(request):
    return render(request,"home/about.html")

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone,content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
        	messages.error(request,"Please fill the form correctly")
        else:
        	contact=Contact(name=name,email=email,phone=phone,content=content)
        	contact.save()
        	messages.success(request,"Your messages has been sent successfully")

    return render(request, "home/contact.html")

#This is a Authentication API
#This is a search functionality validations
def search(request):
    query=request.GET['query']
    if len(query) > 100:
        allPosts = Post.objects.none()
    #allPosts=Post.objects.all()
    else:
        #This is a post in title search validations
        allPostsTitle=Post.objects.filter(title__icontains=query)
        #This is a post in content search validations
        allPostsContent=Post.objects.filter(content__icontains=query)
        #This is a post in title and content combine search validations
        allPosts=allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request,"No search results found.Please refine your query...")
    params = {'allPosts':allPosts, 'query':query}
    return render(request, "home/search.html",params)

def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameters
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #Check forerrorneous inputs
        #Username should be 10 character validations
        if len(username) < 10:
            messages.error(request,"Username must be under 10 characters")
            return redirect("home")

        #Alpha numeric characters validations
        if not username.isalnum():
            messages.error(request, " Username should be only contain letters and numbers")
            return redirect('home')

        #Password check validations    
        if (pass1!= pass2):
            messages.error(request,"Password do not match!Please try again")
            return redirect("home")
        
        #Create the user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your account has been created successfully")
        return redirect("home")

    else:
        return HttpResponse('Not allowed! Please try again')

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        usernames=request.POST['usernames']
        passs=request.POST['passs']
        user=authenticate(username= usernames, password= passs)

        #user not registered validations
        if user is not None:
            login(request, user)
            messages.success(request, "Your account has been successfully login")
            return redirect("home")
        else:
            messages.error(request, "Not allowed! Please try again")
            return redirect("home")

    return HttpResponse("Not allowed!Please try again")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')