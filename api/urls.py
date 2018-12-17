from django.urls import path
from rest_framework.documentation import include_docs_urls

from document import views as document_views
from .routers import OptionalSlashRouter

router = OptionalSlashRouter()
router.register(r'document', document_views.DocumentViewSet)

urlpatterns = [
    path('docs/', include_docs_urls(title='Documents Service')),
]

urlpatterns += router.urls
