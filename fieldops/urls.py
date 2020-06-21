from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.views.static import serve
import fieldops.views

urlpatterns = [
    path('visiting_home/', fieldops.views.visiting_home, name="visiting_home"),
    path('__get_companies_for_kam/', fieldops.views.__get_companies_for_kam, name="__get_companies_for_kam"),
    path('__create_new_visit/', fieldops.views.__create_new_visit, name="__create_new_visit"),
    path('__modify_visit/', fieldops.views.__modify_visit, name="__modify_visit"),
    path('__create_manager_visit/', fieldops.views.__create_manager_visit, name="__create_manager_visit"),
    path('__get_visits_for_kam/', fieldops.views.__get_visits_for_kam, name="__get_visits_for_kam"),
    path('__delete_visit/', fieldops.views.__delete_visit, name="__delete_visit"),
    path('__get_companies_for_kam/', fieldops.views.__get_companies_for_kam, name="__get_companies_for_kam"),
    path('complete_visit/', fieldops.views.complete_visit, name="complete_visit"),
    path('__get_current_month_visits/', fieldops.views.__get_current_month_visits, name="__get_current_month_visits"),
    path('__populate_calendar/', fieldops.views.__populate_calendar, name="__populate_calendar"),
    path('__get_kamids/', fieldops.views.__get_kamids, name="__get_kamids"),
    path('__get_kamids_manager/', fieldops.views.__get_kamids_manager, name="__get_kamids_manager"),
    path('__get_kamids_leader/', fieldops.views.__get_kamids_leader, name="__get_kamids_leader"),
    path('download_excel/<kam_id>', fieldops.views.download_excel, name="download_excel"),
    path('download_full_excel/', fieldops.views.download_full_excel, name="download_full_excel"),
]