from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homePage'),
    path('about-us', views.about, name='aboutPage'),
    path('contact', views.contact, name='contactPage'),
    path('courses', views.courses, name='coursesPage'),
    path('instructors', views.instructors, name='instructorsPage'),
    path('blogs', views.blogs, name='blogsPage'),
    path('blog/<str:slug>', views.blogDetail, name='blogPage'),
    path('blog/sample', views.sampleBlog, name='sampleBlogPage'),
]