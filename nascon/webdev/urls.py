from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('UserProfileView/' , views.UserProfileView , name='UserProfileView'),
    path('RegisterEvent/' , views.RegisterEvent , name='RegisterEvent'),
    path('Buy/' , views.Buy , name='Buy'),
    path('libraryItems/' , views.libraryItems , name='libraryItems'),
    path('Sell/' , views.Sell , name='Sell'),
    path('JoinCommunity/' , views.JoinCommunity , name='JoinCommunity'),
    path('CreateTopic/' , views.CreateTopic , name='CreateTopic'),
    path('JoinTopic/' , views.JoinTopic , name='JoinTopic'),
    path('PerformActivity/' , views.PerformActivity , name='PerformActivity'),
    path('Like/' , views.Like , name='Like'),
    path('ShowProject/' , views.ShowProject , name='ShowProject'),
    path('AddProject/' , views.AddProject , name='AddProject'),
    path('ShowTopics/' , views.ShowTopics , name='ShowTopics'),
    path('TopicMessages/' , views.TopicMessages , name='TopicMessages'),
    path('UpcomingEvents/' , views.UpcomingEvents , name='UpcomingEvents'),

    path('GetProjets/' , views.GetProjets , name='GetProjets'),
    path('GetEventDetails/' , views.GetEventDetails , name='GetEventDetails'),
    path('JoinEvent/' , views.JoinEvent , name='JoinEvent'),
    path('MarketPlace/' , views.MarketPlace , name='MarketPlace'),


]