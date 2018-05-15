from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.SimpleRouter()

urlpatterns = [
    path('docs/', include_docs_urls(title='Documents Service')),
]

urlpatterns += router.urls
