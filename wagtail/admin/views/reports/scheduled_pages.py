import django_filters
from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from wagtail.admin.filters import (
    ContentTypeFilter,
    DateTimeRangePickerWidget,
    WagtailFilterSet,
)
from wagtail.admin.views.reports.base import PageReportView
from wagtail.admin.views.scheduled_pages import get_scheduled_pages_for_user
from wagtail.models import Page
from wagtail.permission_policies.pages import PagePermissionPolicy

from .utils import get_content_types_for_filter


class ScheduledPagesReportFilterSet(WagtailFilterSet):
    schedule_go_live_at = django_filters.DateTimeFromToRangeFilter(
        label=_("Go live at"), widget=DateTimeRangePickerWidget
    )
    content_type = ContentTypeFilter(
        label=_("Page type"), queryset=lambda request: get_content_types_for_filter()
    )
    schedule_type = django_filters.ChoiceFilter(
        label=_("Schedule type"),
        method="filter_schedule_type",
        choices=(
            ("goes_live", _("Goes live")),
            ("expires", _("Expires")),
        ),
        empty_label=_("All"),
        widget=forms.RadioSelect,
    )

    def filter_schedule_type(self, queryset, name, value):
        if value and self.request and self.request.user:
            if value == "goes_live":
                queryset = queryset.filter(_approved_schedule=True)
            elif value == "expires":
                queryset = queryset.filter(expire_at__isnull=False)
        return queryset

    class Meta:
        model = Page
        fields = ["schedule_go_live_at", "content_type"]


class ScheduledPagesView(PageReportView):
    template_name = "wagtailadmin/reports/scheduled_pages.html"
    title = _("Pages scheduled for publishing")
    header_icon = "time"
    filterset_class = ScheduledPagesReportFilterSet

    def get_queryset(self):
        qs = get_scheduled_pages_for_user(self.request.user)
        self.queryset = qs.annotate(
            schedule_go_live_at=F("latest_revision__approved_go_live_at")
        )
        return super().get_queryset()
