from django.conf import settings

from django.urls import path, include, re_path

from rest_framework import permissions


urlpatterns = [
    path('catalogues/', include('catalogue.urls')),
    path('agents/<str:agent_id>/travelers/', include('traveler.urls')),
    path('agents/', include('agent.urls')),
    path('hotels/', include('hotel.urls')),
    
]

if settings.DEBUG:

    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
       openapi.Info(
          title="Volindo API",
          default_version='v1',
          description="Volindo API",
       ),
       public=True,
       permission_classes=[permissions.AllowAny],
    )

    urlpatterns += [re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')]
    urlpatterns += [re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')]
