from django.contrib import admin
from django.urls import include, path
from rest_framework.views import APIView
from rest_framework.response import Response

urlpatterns = [path("admin/", admin.site.urls)]


class APIRoot(APIView):
    def get(self, request, *args, **kwargs):
        apidocs = {
            "user": request.build_absolute_uri("user/"),
            "users": request.build_absolute_uri("users/"),
            "titles": request.build_absolute_uri("titles/"),
            "genres": request.build_absolute_uri("genres/"),
            "categories": request.build_absolute_uri("categories/"),
        }
        return Response(apidocs)


urlpatterns += [
    path(
        "api/v1/",
        include(
            [
                path("", include("ratings.urls")),
                path("", include("users.urls")),
                path("", APIRoot.as_view()),
            ]
        ),
    )
]
