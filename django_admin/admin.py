from django.apps import apps
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.text import capfirst

from .admin_model_nav import NAV_MENU_ORDER


class CompanyAdminSite(admin.AdminSite):
    site_header = "Company Admin"

    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        Overriden by
        """
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            "title": f"Hi {request.user.username}, welcome to the Company admin panel!",
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )

    def get_app_list(self, request):
        know_how = {
            "name": "Know how",
            "models": [
                {
                    "name": "Documentation",
                    "admin_url": "/admin/doc/",
                    "view_only": True,
                },
            ],
        }
        return [know_how] + self.get_custom_app_list(
            NAV_MENU_ORDER, self._registry, request
        )

    def get_custom_app_list(self, nodes, registry, request, app_list=None):
        if app_list is None:
            app_list = []

        for node in nodes:
            try:
                node_model = apps.get_model(
                    node.get("app_name"), node.get("model_name")
                )
                has_model_perms = registry[node_model].get_model_perms(request)
                admin_url = reverse(
                    f"admin:{node_model._meta.app_label}_{node_model._meta.model_name}_changelist"
                )
                add_url = reverse(
                    f"admin:{node_model._meta.app_label}_{node_model._meta.model_name}_add"
                )
            except LookupError:
                node_model = None
                admin_url = None
                add_url = None
                has_model_perms = {}
            if request.user.has_perms(f"view_{node.get('model_name')}"):
                app_list.append(
                    {
                        "app_label": node.get("app_name"),
                        "admin_url": admin_url,
                        "add_url": add_url,
                        "name": capfirst(node.get("menu_name")),
                        "object_name": node.get("model_name"),
                        "has_module_perms": has_model_perms.get("view"),
                        "perms": has_model_perms,
                        "view_only": False,
                        "models": self.get_custom_app_list(
                            node["models"], registry, request
                        ),
                    }
                )

        return app_list
