from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'assignment2.views.home', name='home'),
    # url(r'^assignment2/', include('assignment2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    
    
    ###################################################
    # application specific mappings begin here
    # homepage
    url(r'^fieldNoteManager/$', 'fieldNoteManager.views.index'),
    
    # login
    url(r'^fieldNoteManager/login/$', 'fieldNoteManager.views.login'),
    
    # logout
    url(r'^fieldNoteManager/logout/$', 'fieldNoteManager.views.logout'),
    
    # register form
    url(r'^fieldNoteManager/showRegisterForm/$', 'fieldNoteManager.views.showRegisterForm'),

    # register
    url(r'^fieldNoteManager/register/$', 'fieldNoteManager.views.register'),
    
    # showLocationForm
    url(r'^fieldNoteManager/showLocationForm/$', 'fieldNoteManager.views.showLocationForm'),
    
    # showObservationForm
    url(r'^fieldNoteManager/addLocation/$', 'fieldNoteManager.views.addLocation'),
    
    # addSighting
    url(r'^fieldNoteManager/addSighting/$', 'fieldNoteManager.views.addSighting'),
    
    # searchByLocation
    url(r'^fieldNoteManager/searchByLocation/$', 'fieldNoteManager.views.searchByLocation'),
    
    # searchBySpecies
    url(r'^fieldNoteManager/searchBySpecies/$', 'fieldNoteManager.views.searchBySpecies'),
    
    # wildCardSearch
    url(r'^fieldNoteManager/wildCardSearch/$', 'fieldNoteManager.views.wildCardSearch'),
    
    # showMap
    url(r'^fieldNoteManager/showMap/$', 'fieldNoteManager.views.showMap'),
    
    # showMap
    url(r'^fieldNoteManager/showWikipediaLinks/$', 'fieldNoteManager.views.showWikipediaLinks'),
)