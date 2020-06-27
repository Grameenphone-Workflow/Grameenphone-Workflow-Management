"""GPWorkflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.views.static import serve
import WorkflowTool.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('visit/', include('fieldops.urls')),
    path('admin/', admin.site.urls),
    path('login/', WorkflowTool.views.login, name='login'),
    path('reset/', WorkflowTool.views.reset, name='reset'),
    path('onboarding_sla_view/', WorkflowTool.views.onboarding_sla_view, name='onboarding_sla_view'),
    path('__get_onboarding_sla/', WorkflowTool.views.__get_onboarding_sla, name='__get_onboarding_sla'),
    path('__gerp_sla_days/', WorkflowTool.views.__gerp_sla_days, name='__gerp_sla_days'),
    path('__lerp_sla_days/', WorkflowTool.views.__lerp_sla_days, name='__lerp_sla_days'),
    path('__va_sla_days/', WorkflowTool.views.__va_sla_days, name='__va_sla_days'),
    path('__bscode_sla_days/', WorkflowTool.views.__bscode_sla_days, name='__bscode_sla_days'),
    path('__get_onboarding_averages/', WorkflowTool.views.__get_onboarding_averages, name='__get_onboarding_averages'),
    path('__get_onboarding_sla_diff/', WorkflowTool.views.__get_onboarding_sla_diff, name='__get_onboarding_sla_diff'),
    path('__get_pending_tickets_by_days/', WorkflowTool.views.__get_pending_tickets_by_days, name='__get_pending_tickets_by_days'),
    path('get_code/', WorkflowTool.views.get_code, name='get_code'),
    path('delete_request/', WorkflowTool.views.delete_request, name='delete_request'),
    path('send_code/', WorkflowTool.views.send_code, name='send_code'),
    path('change_password/', WorkflowTool.views.change_password, name='change_password'),
    path('send_code_email/', WorkflowTool.views.send_code_email, name='send_code_email'),
    # path('', RedirectView.as_view(url='login/'), name='login'),
    path('', WorkflowTool.views.landing_page, name='landing_page'),
    path('credits', WorkflowTool.views.credits, name='credits'),
    path('logout/', WorkflowTool.views.logout, name='logout'),
    re_path(r'^download/(?P<path>.*)$', WorkflowTool.views.download_file),
    re_path(r'^download_zip/(?P<company_name>.*)$', WorkflowTool.views.download_zip),
    path('__kam_tickets/', WorkflowTool.views.__kam_tickets, name='__kam_tickets'),
    path('fetch_copc_tickets/', WorkflowTool.views.fetch_copc_tickets, name='fetch_copc_tickets'),
    path('tickets/', WorkflowTool.views.tickets, name='tickets'),
    path('requisition_tickets/', WorkflowTool.views.requisition_tickets, name='requisition_tickets'),
    path('task_configuration/', WorkflowTool.views.task_configuration, name='task_configuration'),
    path('onboarding_form/', WorkflowTool.views.onboarding_form, name='onboarding_form'),
    path('product_requisition_form/', WorkflowTool.views.product_requisition_form, name='product_requisition_form'),
    path('dashboard/', WorkflowTool.views.dashboard, name='dashboard'),
    path('fetch_tickets/', WorkflowTool.views.fetch_tickets, name='fetch_tickets'),
    path('fetch_tickets_specific/', WorkflowTool.views.fetch_tickets_specific, name='fetch_tickets_specific'),
    path('fetch_requisition_tickets/', WorkflowTool.views.fetch_requisition_tickets, name='fetch_requisition_tickets'),
    path('fetch_onboarding_tickets/', WorkflowTool.views.fetch_onboarding_tickets, name='fetch_onboarding_tickets'),
    path('start_workflow/', WorkflowTool.views.start_workflow, name='start_workflow'),
    path('onboard/', WorkflowTool.views.onboard, name='onboard'),
    path('product_form/', WorkflowTool.views.product_form, name='product_form'),
    path('__get_all_corp_names/', WorkflowTool.views.__get_all_corp_names, name='__get_all_corp_names'),
    path('check_bs_code/', WorkflowTool.views.check_bs_code, name='check_bs_code'),
    path('__fire_next/', WorkflowTool.views.__fire_next, name='__fire_next'),
    path('__fire_next_requisition/', WorkflowTool.views.__fire_next_requisition, name='__fire_next_requisition'),
    path('__reject_prev/', WorkflowTool.views.__reject_prev, name='__reject_prev'),
    path('fetch_gerp_table/', WorkflowTool.views.fetch_gerp_table, name='fetch_gerp_table'),
    path('fetch_lerp_table/', WorkflowTool.views.fetch_lerp_table, name='fetch_lerp_table'),
    path('fetch_lerp_table_2/', WorkflowTool.views.fetch_lerp_table_2, name='fetch_lerp_table_2'),
    path('fetch_clc_table/', WorkflowTool.views.fetch_clc_table, name='fetch_clc_table'),
    path('fetch_va_table/', WorkflowTool.views.fetch_va_table, name='fetch_va_table'),
    path('clc_form/', WorkflowTool.views.clc_form, name='clc_form'),
    path('__get_sla/', WorkflowTool.views.__get_sla, name='__get_sla'),
    path('o2c_panel/', WorkflowTool.views.o2c_panel, name='o2c_panel'),
    path('__get_all_items/', WorkflowTool.views.__get_all_items, name='__get_all_items'),
    path('__get_all_sla/', WorkflowTool.views.__get_all_sla, name='__get_all_sla'),
    path('__submit_sim_serials/', WorkflowTool.views.__submit_sim_serials, name='__submit_sim_serials'),
    path('__get_onboard_for_bscode/', WorkflowTool.views.__get_onboard_for_bscode, name='__get_onboard_for_bscode'),
    re_path(r'^onboarding_form_draft/(?P<wfid>[\w|\W]+)$', WorkflowTool.views.onboarding_form_draft, name='onboarding_form_draft'),
    re_path(r'^product_requisition_form_draft/(?P<wfid>[\w|\W]+)$', WorkflowTool.views.product_requisition_form_draft, name='product_requisition_form_draft')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)