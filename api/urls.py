from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from documents import views as document_views
router = routers.SimpleRouter()

router.register(r'documents', document_views.DocumentViewSet)

urlpatterns = [
    path('docs/', include_docs_urls(title='Documents Service')),
]

urlpatterns += router.urls
