from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from impactreeapi.views import *
from django.conf.urls import include
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, "user")
router.register(r"milestones", MilestoneViewSet, "milestone")
router.register(r"charitycategories", CharityCategoryViewSet, "charitycategories")
router.register(r"charities", CharityViewSet, "charities")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
]
