from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homePage'),
    path('about-us', views.about, name='aboutPage'),
    path('contact', views.contact, name='contactPage'),
    path('courses', views.courses, name='coursesPage'),
    path('courses/<slug:slug>', views.courseDetail, name='courseDetailPage'),
    path('instructors', views.instructors, name='instructorsPage'),
    path('blogs', views.blogs, name='blogsPage'),
    path('blog/<str:slug>', views.blogDetail, name='blogPage'),
    path('blog/sample', views.sampleBlog, name='sampleBlogPage'),
    path('payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('payment/guest-checkout/', views.guest_checkout, name='guest_checkout'),
    path('payment/create/', views.create_payment, name='create_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    # Admin message functionality
    path('admin/send-message/<int:user_id>/', views.send_message_to_user, name='send_message_to_user'),
    # Legal Pages
    path('privacy-policy/', views.privacy_policy, name='privacyPolicy'),
    path('terms-and-conditions/', views.terms_conditions, name='termsConditions'),
    path('shipping-policy/', views.shipping_policy, name='shippingPolicy'),
    path('cancellations-refunds/', views.cancellations_refunds, name='cancellationsRefunds'),
]