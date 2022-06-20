from django.urls import path, include

from wagtail.admin.views import scheduled_pages

from wagtail.admin.views.scheduled_pages import publish_all_scheduled, publish_all_scheduled_confirm, publish

app_name = "wagtailadmin_scheduled_pages"

urlpatterns = [
    path("<int:page_id>/publish/", publish, name='publish'),
    path("publish_all/", publish_all_scheduled, name='publish_all'),
    path("publish_all/confirm/", publish_all_scheduled_confirm, name='publish_all_confirm'),
]
