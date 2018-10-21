from django.urls import path
from .views import Login, Logout, Signup, home, event_create, dashboard, event_detail, event_edit, events

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('create/',event_create ,name='create'),
    path('dashboard/',dashboard ,name='dashboard'),
    path('events/',events ,name='events'),
    path('detail/<int:event_id>/',event_detail ,name='detail'),
    path('edit/<int:event_id>/',event_edit ,name='edit'),
]