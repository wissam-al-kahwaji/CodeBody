from django.urls import path
from . import views

urlpatterns = [
    # Start home Page
    path('', views.home, name="home"),
    # END home Page

    # Start SSE
    path('WH2005M8D25H@L@', views.Data_notification, name='Data_notification'),
    path('H@L@m2l0ve1859Co/<str:pk>', views.Data_discussion, name='Data_discussion'),
    path('H@L@m2l0ve185', views.Data_home, name='Data_home'),
    # END SSE

    # Start Json Data
    path('Search/', views.Search, name="Search"),
    path('topic_list/', views.topic_list, name="topic_list"),
    path('Notification/', views.Notification, name='Notification'),
    path('topic/', views.topic, name='topic'),
    path('comments/<str:pk>', views.comments, name='comments'),
    path('CreateComment/<str:pk>', views.CreateComment, name='CreateComment'),
    path('CreateReact/<str:pk>', views.CreateReact, name='CreateReact'),
    path('ChackUsername', views.ChackUsername, name='ChackUsername'),
    path('ChackEmail', views.ChackEmail, name='ChackEmail'),
    # END Json Data

    # Start Ajax Page
    path('create-discussion/', views.createDiscussion, name="create-discussion"),
    path('Edit-Discussion/<str:pk>', views.updateDiscussion, name="update-discussion"),
    path('delete-discussion/<str:pk>', views.deleteDiscussion, name="delete-discussion"),
    path('delete-Commints/<str:pk>', views.deleteCommints, name="delete-Commints"),
    path('Followers', views.Followers, name="Followers"),
    path('ChangePassword', views.ChangePassword, name="ChangePassword"),
    # END Ajax Page

    # Start Page 
    path('login/', views.LoginPage, name="login"),
    path('register/', views.RegisterPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:pk>', views.Profile, name="profile"),
    path('Settings/<str:pk>', views.Settings, name="Settings"),
    path('discussion/<str:pk>/', views.discussion, name="discussion"),
    # END Page 
    
]