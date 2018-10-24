from django.urls import path
from .views import (Login, Logout, Signup, home, 
 event_create, dashboard, 
 event_detail, event_edit, 
 events, event_delete,
 event_book, no_access, 
 profile_edit, profile, 
 profiles)

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
    path('delete/<int:event_id>/',event_delete ,name='delete'),
    path('book/<int:event_id>/',event_book ,name='book'),
    path('noaccess/',no_access ,name='no-access'),
    path('profile/<int:user_id>/',profile ,name='profile'),
    path('profile/edit/',profile_edit ,name='profile-edit'),
    path('profiles/',profiles ,name='profiles'),
]