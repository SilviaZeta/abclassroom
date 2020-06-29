# Use include() to add paths from the catalog application 
from django.urls import path, include
from . import views

urlpatterns = [

				path('<username>/', views.profile_view, name='profile_page'),
    			path('<username>/dashboard/', views.profile_view, name='dashboard'),

    			path('<username>/dashboard/join_class/',  views.join_class_view, name='join_class'),
    			path('<username>/dashboard/join_class/<str:pk>/',  views.join_class_view, name='join_class'),

				path('<username>/dashboard/create_class/',  views.create_class_view, name='create_class'),
				path('<username>/dashboard/<str:pk>/update_class/', views.update_class_view, name='update_class'),
				path('<username>/dashboard/<str:pk>/delete_class/', views.delete_class_view, name='delete_class'),

				path('<username>/dashboard/search_class/', views.search_class_view, name='search_class'),

				path('<username>/dashboard/enrolled_users/', views.enrolled_users_view, name='enrolled_users'),

    			path('<username>/dashboard/enrolled_users/add_user/', views.add_user_view, name='add_user'), #default path
    			path('<username>/dashboard/enrolled_users/add_user/<str:pk>/', views.add_user_view, name='add_user'),
    			path('<username>/dashboard/enrolled_users/add_user/<str:pk>/add_user_outcome/', views.add_user_view, name='add_user_outcome'),

    			path('<username>/dashboard/enrolled_users/approve_user/', views.approve_user_view, name='approve_user'),
    			path('<username>/dashboard/enrolled_users/approve_user/<str:pk>/<str:pk1>/', views.approve_user_view, name='approve_user'),

    			path('<username>/dashboard/enrolled_users/remove_user/', views.remove_user_view, name='remove_user'), #default path
    			path('<username>/dashboard/enrolled_users/remove_user/<str:pk>/<str:pk1>/', views.remove_user_view, name='remove_user'),

				path('<username>/<str:pk>/class_dashboard/', views.class_page_view, name='class_dashboard'),
				path('<username>/<str:pk>/class_dashboard/class_invite/', views.class_invite_view, name='class_invite'),
				
				path('<username>/<str:pk>/class_dashboard/priority_invite', views.priority_invite_view, name='priority_invite'),
				path('<username>/<str:pk>/class_dashboard/<str:pk1>/delete_priority/', views.delete_priority_view, name='delete_priority'),
				path('<username>/<str:pk>/class_dashboard/<str:pk1>/assign_priority/', views.assign_priority_view, name='assign_priority'),

				path('<username>/<str:pk>/class_dashboard/invite_confirm/', views.invite_confirm_view, name='invite_confirm'),

				path('<username>/<str:pk>/class_dashboard/grouping_invite', views.grouping_invite_view, name='grouping_invite'),
				path('<username>/<str:pk>/class_dashboard/<str:pk1>/join_group', views.join_group_view, name='join_group'),
				path('<username>/<str:pk>/class_dashboard/<str:pk1>/leave_group', views.leave_group_view, name='leave_group'),
				path('<username>/<str:pk>/class_dashboard/<str:pk1>/delete_group', views.delete_group_view, name='delete_group'),


				]

