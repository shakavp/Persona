from django.conf.urls import patterns, include, url
#from persona_fusion import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Persona.views.home', name='home'),
    # url(r'^Persona/', include('Persona.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^$', views.index, name='index'),
    url(r'^persona_fusion/', include('persona_fusion.urls', namespace='persona_fusion')),
)
