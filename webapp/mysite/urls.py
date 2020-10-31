from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mysite.core import views

admin.site.site_header = 'Anti Ragging Administration'
admin.site.site_title = 'Anti Ragging Admin'
admin.site.index_title = 'Anti Ragging Administration'


urlpatterns = [
    path('', views.home, name='home'),
   # path('login',views.admin,name='login'),
    path('home1',views.home1,name='home1'),
    path('home3',views.home3,name='home3'),
    path('home4',views.home4,name='home4'),
    path('complaintregistered',views.complaintregistered,name='complaintregistered'),
    path('students',views.allstudents,name='student'),
    path('addstudent',views.students,name='addstudent'),
    path('filecomplaint',views.filecomplaint,name='filecomplaint'),
    path('studentprofile',views.studentprofile,name='studentprofile'),
    #path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('loggedin',views.login_successful,name='login_successful'),
    path('complaintdetails',views.complaintdetails,name='complaintdetails')
    

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)