from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

     # path for about view
    path('about/',views.about, name='about'),

    # path for contact us view
    path('contact/',views.contact, name='contact_us'),

    # path for registration
    path('sign-up/',views.registration_request, name='sign-up'),

    # path for login
    path('login/',views.login_request , name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/<str:full_name>', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('review/<int:dealer_id>/<str:full_name>', views.add_review, name='add_review'),

    path('home/',views.home, name='home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)