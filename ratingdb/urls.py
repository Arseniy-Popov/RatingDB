from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls)]


urlpatterns += [
    path(
        "api/v1/",
        include(
            [
                path("", include("ratings.urls")),
                path("users/", include("users.urls")),
                path("api-auth/", include("rest_framework.urls")),
            ]
        ),
    )
]
