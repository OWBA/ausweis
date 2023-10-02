from django.contrib import admin
from django.contrib.auth.models import Group  # , User
from django.utils.safestring import mark_safe

from .models import Organization, Member

admin.site.site_header = 'Ausweis-Verwaltung'  # top-most title
admin.site.index_title = 'Ausweis'  # title at root
admin.site.site_title = 'Ausweis-Verwaltung'  # suffix to <title>

admin.site.unregister(Group)
# admin.site.unregister(User)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ('name', 'slug', 'member_count')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'slug')

    @admin.display(description='Mitglieder')
    def member_count(self, obj: 'Organization'):
        return obj.members.count()


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'url_link_full')
    list_display = (
        'name', 'member_id', 'valid_since', 'valid_until', 'url_link_short')
    search_fields = ('name', 'member_id')

    @admin.display(description='URL')
    def url_link_short(self, obj: 'Member'):
        return mark_safe(f'<a target="blank" href="{obj.export_url}">Link</a>')

    @admin.display(description='URL')
    def url_link_full(self, obj: 'Member'):
        return mark_safe('<a target="blank" href="{0}">{0}</a>'.format(
            obj.export_url))
