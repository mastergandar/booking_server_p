from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.safestring import mark_safe

from file_manager.models import LinkedImages
from properties.enums import Status
from properties.models import Properties
from social.enums import ReportStatus, NotifyCode
from social.models import Review, Notify, Report, ReportList, Favorite


class ImageInline(GenericTabularInline):
    model = LinkedImages
    extra = 0
    readonly_fields = ["rendered_image"]
    fields = ["title", "image", "rendered_image", "user"]

    def rendered_image(self, obj):
        if obj.image:
            url = obj.image.storage.url(name=obj.image.name)
            return mark_safe(
                f"""<img src="{url}" width=320 height=240 />"""
            )
        return ""


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'content_type',
        'object_id',
        'description',
        'purity',
        'location',
        'communication',
        'price_quality',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'user',
                'content_type',
                'object_id',
                'description',
                'purity',
                'location',
                'communication',
                'price_quality',
            ]
        }),
    )

    inlines = [ImageInline]

    def rendered_image(self, obj):
        if obj.image:
            url = obj.image.storage.url(name=obj.image.name)
            return mark_safe(
                f"""<img src="{url}" width=320 height=240 />"""
            )
        return ""


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'app_label',
        'model',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'app_label',
                'model',
            ]
        }),
    )


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'code',
        'user',
        'payload',
        'created_at',
        'is_viewed',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'code',
                'user',
                'payload',
                'created_at',
                'is_viewed',
            ]
        }),
    )
    readonly_fields = ['created_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'status',
        'content_type',
        'object_id',
        'description',
        'report_type',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'user',
                'content_type',
                'object_id',
                'description',
                'report_type',
                'status',
            ]
        }),
        ('ACTIONS', {
            "fields": [('report_in_progress', 'report_resolved', 'report_rejected')]
        }),
    )
    readonly_fields = ['status', 'report_in_progress', 'report_resolved', 'report_rejected']
    change_form_template = 'admin/social/reports/reports_change.html'
    list_filter = ['status', 'report_type', 'content_type']
    inlines = [ImageInline]

    def report_in_progress(self, obj):
        if not obj.pk:
            obj.pk = 0
        if obj.status == ReportStatus.REJECTED or ReportStatus.RESOLVED:
            return mark_safe(
                f"""<a class="btn disabled" href="#" disabled>In progress</a>"""
            )
        else:
            return mark_safe(
                f"""<a class="btn btn-primary" href="{reverse("admin:report_in_progress", args={obj.pk})}" disabled>In progress</a>"""
            )

    def report_resolved(self, obj):
        if not obj.pk:
            obj.pk = 0
        if obj.status == ReportStatus.REJECTED or ReportStatus.RESOLVED:
            return mark_safe(
                f"""<a class="btn disabled" href="#" disabled>Resolved</a>"""
            )
        else:
            Properties.objects.get(pk=obj.object_id).status = Status.ARCHIVED.value
            return mark_safe(
                f"""<a class="btn btn-danger" href="{reverse("admin:report_resolved", args={obj.pk})}">Resolved</a>"""
            )

    def report_rejected(self, obj):
        if not obj.pk:
            obj.pk = 0
        if obj.status == ReportStatus.REJECTED or ReportStatus.RESOLVED:
            return mark_safe(
                f"""<a class="btn disabled" href="#" disabled>Rejected</a>"""
            )
        else:
            Properties.objects.get(pk=obj.object_id).status = Status.ARCHIVED.value
            return mark_safe(
                f"""<a class="btn btn-danger" href="{reverse("admin:report_rejected", args={obj.pk})}">Rejected</a>"""
            )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('report_in_progress/<int:pid>', self.admin_site.admin_view(self.report_move_to_progress),
                           name="report_in_progress"),
            path('report_resolved/<int:pid>', self.admin_site.admin_view(self.report_resolve),
                           name="report_resolved"),
            path('report_rejected/<int:pid>', self.admin_site.admin_view(self.report_reject),
                           name="report_rejected")]
        # Список отображаемых столбцов
        return custom_urls + urls

    @transaction.atomic
    def report_move_to_progress(self, request, pid):
        report = Report.objects.get(pk=pid)
        report.status = ReportStatus.IN_PROGRESS.value
        report.save()
        return HttpResponseRedirect(reverse('admin:social_report_change', args=(pid,)))

    @transaction.atomic
    def report_resolve(self, request, pid):
        report = Report.objects.get(pk=pid)
        report.status = ReportStatus.RESOLVED.value
        report.content_object.status = Status.ARCHIVED.value
        Notify.objects.create(
            code=NotifyCode.REPORT_RESOLVED.value,
            user=report.user,
            payload={
                'report_id': report.pk,
                'report_type': report.report_type,
                'content_type': report.content_type,
                'object_id': report.object_id,
            }
        )
        Notify.objects.create(
            code=NotifyCode.REPORT_RESOLVED.value,
            user=report.content_object.user,
            payload={
                'report_id': report.pk,
                'report_type': report.report_type,
                'content_type': report.content_type,
                'object_id': report.object_id,
            }
        )
        report.save()
        return HttpResponseRedirect(reverse('admin:social_report_change', args=(pid,)))

    @transaction.atomic
    def report_reject(self, request, pid):
        report = Report.objects.get(pk=pid)
        report.status = ReportStatus.REJECTED.value
        Notify.objects.create(
            code=NotifyCode.REPORT_REJECTED.value,
            user=report.user,
            payload={
                'report_id': report.pk,
                'report_type': report.report_type,
                'content_type': report.content_type,
                'object_id': report.object_id,
            }
        )
        report.save()
        return HttpResponseRedirect(reverse('admin:social_report_change', args=(pid,)))

class ReportListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

    class Meta:
        model = Report
        fields = "__all__"


class ReportListAdmin(ReportAdmin):
    form = ReportListForm
    list_display = (
        "report_list",
        "property_link",
        "property_id",
        "property_title",
        "property_user",
        "reports_count",
    )

    def report_list(self, obj):
        return mark_safe(
            f'<a href="https://api.roompesa.goodbit.dev/admin/social/report/?content_type__id__exact=12&object_id={obj.object_id}">View Reports</a>'
        )

    def property_link(self, obj):
        return mark_safe(
            f'<a href="https://api.roompesa.goodbit.dev/admin/properties/properties/{obj.object_id}/change/">View Property</a>'
        )

    def property_id(self, obj):
        return obj.object_id

    def property_title(self, obj):
        return obj.content_object.title

    def property_user(self, obj):
        return obj.content_object.user

    def reports_count(self, obj):
        return Report.objects.filter(content_type=obj.content_type, object_id=obj.object_id).count()


admin.site.register(ReportList, ReportListAdmin)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "content_type",
        "object_id",
    )
    list_filter = ["user", "content_type"]
    search_fields = ["user"]
    readonly_fields = ["created_at"]
