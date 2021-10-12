"""cosmos2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from enroll import views
from django.conf import Settings, settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('signin/',views.Sign_Up,name='signin'),
    path('login/',views.Log_In,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.Log_out,name='logout'),
    path('passchange/',views.ChangePass,name='passchange'),
    path('detail/<int:id>',views.show,name='detail'),
    path('social-auth',include('social_django.urls',namespace='social')),
    path('face_upload/',views.face_section,name='face_upload'),
    path('facebook_form/<int:id>',views.facebook_form,name='facebook_form'),
    path('tweeter/',views.tweeter_upload,name='tweeter'),
    path('delete/<int:id>',views.delete_image,name='delete'),
path('all_social/',views.all_social,name='all_social'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
