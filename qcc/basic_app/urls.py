from django.conf.urls import url
from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    #url(r'^other/$',views.other,name='other'),
    url(r'^user_login/$',views.LoginView.as_view(),name='user_login'),
    url(r'^home/$',views.HomeView.as_view(),name='home'),
    #url(r'^home/(?P<pk>\d+)/$', views.SubjectView.as_view(), name='subject_detail'),
    path('home/<int:pk>/', views.SubjectView.as_view(), name='subject_detail'),
    path('home/<int:sid>/<int:tid>', views.FrameView.as_view(), name='frame'),
    path('home/<int:sid>/<int:tid>/test', views.TestView.as_view(), name='test'),
    path('home/<int:sid>/<int:tid>/test/<int:testSaved>', views.TestView.as_view(), name='test'),
]