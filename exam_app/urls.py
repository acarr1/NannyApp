from django.conf.urls import url
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    url(r'^$', views.index), #This connects the urls and views pages. 
    url(r'^register$', views.register), # This registers users.
    url(r'^book/new$', views.book), # This allows all users to add new jobs.
    url(r'^book/process$', views.new_book_process),
    url(r'^dash$', views.dash), # This shows the dashboard for the users.
    url(r'^book/(?P<bookid>\d+)$', views.view_book),  # This allows users to see the jobs for all users. 
    url(r'^login$', views.login), # This logs in the users.
    url(r'^logout$', views.logout), # This allows users to logout. 
    url(r'^book/(?P<bookid>\d+)/delete$', views.delete), # This allows users to delete jobs they posted.
    url(r'^book/edit/(?P<bookid>\d+)$', views.edit_book), # This allows us to change the job/description.
    url(r'^edit_book_process/(?P<bookid>\d+)$', views.edit_book_process), # This allows 
    url(r'^profile/(?P<userid>\d+)$', views.profile),  # This allows users to see the jobs for all users.
    url(r'^calender$', views.calender), 
]
