from django.conf.urls import url
from wikilinks import views
urlpatterns = [ 
	url(r'^index/', views.index,), 
	url(r'^$', views.home, name='home'),
	url(r'^question/',views.question)
]
#url(r'^wikilinks/', views.home, name='home'), 