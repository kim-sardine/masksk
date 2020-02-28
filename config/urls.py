from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views import defaults as default_views

from mask.stores.views import main_view

urlpatterns = [
    path("", main_view, name="home"),
    path("robots.txt/", TemplateView.as_view(template_name="pages/robots.txt", content_type="text/plain"), name="robots"),
    path("msk-sitemap/", TemplateView.as_view(template_name="pages/sitemap.xml", content_type="text/plain"), name="sitemap"),
    path("favicon.ico/", RedirectView.as_view(url=static_file('images/favicons/mask_emoji.png'), permanent=True)),

    path(settings.ADMIN_URL, admin.site.urls),

    # path("stores/", include("mask.stores.urls")),

    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),

    # path("users/", include("mask.users.urls", namespace="users")),
    # path("accounts/", include("allauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
