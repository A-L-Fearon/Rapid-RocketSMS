from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
#from rapidsms.backends.Rocket.views import RocketBackendView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    (r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', 'rapidsms.views.dashboard', name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    #(r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('rapidsms.contrib.registration.urls')),
    (r'^rocket/', include('rapidsms.backends.Rocket.urls')),
    #MY Backend
    #url(r'^backend/message_tester/$', RocketBackendView.as_view(backend_name='message_tester')),
    #(r'^rockettest/', include('rapidsms.backends.database.urls')),	
   	
    #url(r'^backends/Rocket/$',
        #RocketBackendView.as_view(backend_name='rocketbackend')),


    # Third party URLs
    (r'^selectable/', include('selectable.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
