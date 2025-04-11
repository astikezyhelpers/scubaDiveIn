from django.shortcuts import render

def home(request):
    return render(request, 'mainSite/index.html')

def about(request):
    return render(request, 'mainSite/about-us.html')

def contact(request):
    return render(request, 'mainSite/contact.html')

def courses(request):
    return render(request, 'mainSite/courses.html')

def instructors(request):
    return render(request, 'mainSite/instructors.html')

def blogs(request):
    return render(request, 'mainSite/blogs.html')

def blogDetail(request,slug):
    return render(request, 'mainSite/blogDetail.html')

def sampleBlog(request):
    return render(request, 'mainSite/blogDetail.html')