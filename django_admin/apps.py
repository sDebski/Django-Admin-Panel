from django.contrib.admin.apps import AdminConfig


class CompanyAdminConfig(AdminConfig):
    default_site = "django_admin.admin.CompanyAdminSite"