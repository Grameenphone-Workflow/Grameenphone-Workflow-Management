from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.core import serializers
from datetime import datetime
from WorkflowTool.models import GPUser, Onboarding, KAMTable
from .models import Visit, Purpose
import xlsxwriter

# Create your views here.


def visiting_home(request):
    user_phone_number = request.session['user_phone_number']
    user = GPUser.objects.get(phone_number=user_phone_number)
    purposes = Purpose.objects.all()
    context = {
        'role': user.role,
        'username': user.username,
        'user': user,
        'purposes': purposes,
    }
    return render(request, 'visiting_home.html', context)

def download_excel(request, kam_id):
    workbook = xlsxwriter.Workbook('data/visiting_excels/{0}_{1}_{2}.xlsx'.format(kam_id, datetime.now().strftime("%B"), datetime.now().year))
    worksheet = workbook.add_worksheet()

    companies = Onboarding.objects.filter(kam_name=kam_id)
    data = []
    for company in companies:
        completed_visit_count = len(list(Visit.objects.filter(kam_id=kam_id, company_name=company.corporate_name, visited=True)))
        planned_visit_count = len(list(Visit.objects.filter(kam_id=kam_id, company_name=company.corporate_name, visited=False)))
        data.append({
            'company_name': company.corporate_name,
            'completed_visit_count': completed_visit_count,
            'planned_visit_count': planned_visit_count,
        })

    my_list = data

    cell_format1 = workbook.add_format()
    cell_format1.set_pattern()  # This is optional when using a solid fill.
    cell_format1.set_bg_color('red')

    cell_format2 = workbook.add_format()
    cell_format2.set_pattern()  # This is optional when using a solid fill.
    cell_format2.set_bg_color('#99FF99')

    worksheet.write(0, 0, 'Company')
    worksheet.write(0, 1, 'Completed')
    worksheet.write(0, 2, 'Planned')
    worksheet.write(0, 3, 'Expected')
    worksheet.write(0, 4, 'Status')

    for row_num, data in enumerate(my_list):
        selected_format = ""

        if data['completed_visit_count'] < 10:
            selected_format = cell_format1
        else:
            selected_format = cell_format2

        worksheet.write(row_num + 1, 0, data['company_name'])
        worksheet.write(row_num + 1, 1, data['completed_visit_count'])
        worksheet.write(row_num + 1, 2, data['planned_visit_count'])
        worksheet.write(row_num + 1, 3, 10)
        worksheet.write(row_num + 1, 4, '', selected_format)
    
    workbook.close()

    response = HttpResponse(open('data/visiting_excels/{0}_{1}_{2}.xlsx'.format(kam_id, datetime.now().strftime("%B"), datetime.now().year), 'rb'), content_type='vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{0}_{1}_{2}.xlsx"'.format(kam_id, datetime.now().strftime("%B"), datetime.now().year)
    return response

def download_full_excel(request):
    workbook = xlsxwriter.Workbook('data/visiting_excels/{0}_{1}.xlsx'.format(datetime.now().strftime("%B"), datetime.now().year))
    worksheet = workbook.add_worksheet()

    visits = Visit.objects.filter(date_of_visit__month__gte=datetime.now().month)

    
    data = []
    for visit in visits:
        data.append({
            'kam_id': visit.kam_id,
            'kam_name': "TODO",
            'segment': "TODO",
            'company_name': visit.company_name,
            'date': visit.date_of_visit.strftime('%d-%m-%Y'),
            'purpose': visit.visit_type,
            'visited': "Completed" if visit.visited else "Planned",
            'post_visit_feedback': visit.status,
            'visit_start_remark': visit.visit_start_remark,
            'visit_close_remark': visit.visit_close_remark,
        })

    my_list = data

    worksheet.write(0, 0, 'KAM Name')
    worksheet.write(0, 1, 'KAM ID')
    worksheet.write(0, 2, 'Segment')
    worksheet.write(0, 3, 'Company')
    worksheet.write(0, 4, 'Visit Date')
    worksheet.write(0, 5, 'Status')
    worksheet.write(0, 6, 'Purpose')
    worksheet.write(0, 7, 'Feedback')
    worksheet.write(0, 8, 'Initial Remark')
    worksheet.write(0, 9, 'Closing Remark')

    for row_num, data in enumerate(my_list):
        worksheet.write(row_num + 1, 0, data['kam_name'])
        worksheet.write(row_num + 1, 1, data['kam_id'])
        worksheet.write(row_num + 1, 2, data['segment'])
        worksheet.write(row_num + 1, 3, data['company_name'])
        worksheet.write(row_num + 1, 4, data['date'])
        worksheet.write(row_num + 1, 5, data['visited'])
        worksheet.write(row_num + 1, 6, data['purpose'])
        worksheet.write(row_num + 1, 7, data['post_visit_feedback'])
        worksheet.write(row_num + 1, 8, data['visit_start_remark'])
        worksheet.write(row_num + 1, 9, data['visit_close_remark'])
    
    workbook.close()

    response = HttpResponse(open('data/visiting_excels/{0}_{1}.xlsx'.format(datetime.now().strftime("%B"), datetime.now().year), 'rb'), content_type='vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{0}_{1}.xlsx"'.format( datetime.now().strftime("%B"), datetime.now().year)
    return response


def __get_companies_for_kam(request):
    # kam_id = request.GET.get('kam_id')
    # companies = list(Onboarding.objects.values())
    # print(companies)
    # return JsonResponse(companies, safe=False)

    qs = Onboarding.objects.filter(kam_name=request.GET.get('kam_id'))
    data = []
    for onboarding in qs:
        data.append({
            'company_name': onboarding.corporate_name
        })

    return JsonResponse(data, safe=False)

def __get_kamids(request):

    qs = GPUser.objects.filter(role="KAM")
    data = []
    for user in qs:
        data.append({
            'kam_id': user.phone_number
        })
    print(data)
    return JsonResponse(data, safe=False)

def __get_kamids_manager(request):

    qs = GPUser.objects.filter(role="KAM")
    data = []
    for user in qs:
        try:
            if KAMTable.objects.get(username=user.phone_number).manager == request.GET.get('manager'):
                data.append({
                    'kam_id': user.phone_number
                })
        except:
            print("Entry in KAM table for this user does not exist")

    return JsonResponse(data, safe=False)

def __get_kamids_leader(request):

    qs = GPUser.objects.filter(role="KAM")
    leader = GPUser.objects.get(phone_number=request.GET.get('leader'))
    data = []
    for user in qs:
        try:
            if user.segment == leader.segment:
                data.append({
                    'kam_id': user.phone_number
                })
        except:
            print(user.segment)
            print(leader.segment)
            print("Entry in KAM table for this user does not exist")

    return JsonResponse(data, safe=False)

def __create_new_visit(request):

    kam_id = request.GET.get('kam_id')
    company_name = request.GET.get('corporate_name')
    visit_id = "VST" + datetime.now().strftime('%d%m%Y%H%M%S')
    date_of_visit = request.GET.get('date')
    # end_date = request.GET.get('end_date')
    visit = Visit()
    visit.visit_start_remark = request.GET.get('visit_remark')
    visit.visit_id = visit_id
    visit.visit_type = request.GET.get('visit_type')
    visit.company_name = company_name
    visit.kam_id = kam_id
    visit.first_initiated = datetime.now()
    visit.date_of_visit = date_of_visit
    # visit.end_date = end_date
    visit.visited = False
    visit.manager = False
    visit.save()

    return HttpResponse('Done')

def __modify_visit(request):

    visit_id = request.GET.get('visit_id')
    visit = Visit.objects.get(visit_id = visit_id)
    date_of_visit = request.GET.get('date')
    visit.visit_type = request.GET.get('visit_type')
    visit.last_updated = datetime.now()
    visit.date_of_visit = date_of_visit
    visit.save()

    return HttpResponse('Done')

def __create_manager_visit(request):

    kam_id = request.GET.get('kam_id')
    company_name = request.GET.get('corporate_name')
    visit_id = "VST" + datetime.now().strftime('%d%m%Y%H%M%S')
    date_of_visit = request.GET.get('date')
    # end_date = request.GET.get('end_date')
    visit = Visit()
    visit.visit_start_remark = request.GET.get('visit_remark')
    visit.visit_id = visit_id
    visit.visit_type = request.GET.get('visit_type')
    visit.company_name = company_name
    visit.kam_id = kam_id
    visit.first_initiated = datetime.now()
    visit.date_of_visit = date_of_visit
    visit.manager = True
    # visit.end_date = end_date
    visit.visited = False
    visit.save()

    return HttpResponse('Done')

def __get_visits_for_kam(request):
    visits = list(Visit.objects.filter(kam_id=request.GET.get('kam_id'), visited=False))
    data = []
    for i, visit in zip(range(1, len(visits) + 1), visits):
        data.append(
            {
                'id': str(i),
                'calendarId': '1',
                'title': visit.company_name,
                'category': 'time',
                'dueDateClass': '',
                'start': visit.date_of_visit,
                'end': visit.end_date,
                'visiting_id': visit.visit_id,
                'purpose': visit.visit_type,
                'remarks': visit.visit_start_remark,
            }
        )
    return JsonResponse(data, safe=False)

def __populate_calendar(request):
    visits = list(Visit.objects.filter(kam_id=request.GET.get('kam_id')))
    data = []
    current_month = datetime.now().month
    for i, visit in zip(range(1, len(visits) + 1), visits):
        # print("Visiting data: " + str(visit.date_of_visit.month))
        # print("Current month: " + str(current_month))
        # if visit.date_of_visit.month == current_month:
        data.append(
            {
                'id': str(i),
                'calendarId': str(i),
                'title': visit.company_name,
                'category': 'time',
                'body': generate_body_markup(visit),
                'start': visit.date_of_visit.date(),
                'visiting_id': visit.visit_id,
                'isPending': visit.visited,
                'color': "purple" if visit.manager else "red",
            }
        )
    return JsonResponse(data, safe=False)

def generate_body_markup(visit):
    time = ""
    if visit.last_updated:
        time = visit.last_updated.strftime('%d-%m-%Y %H:%M:%S')
    markup = """
        <h6>Last Updated: {0}</h6>
        <h6>Visit Type: {1}</h6>
        <h6>Visit Purpose: {2}</h6>
        <h6>Visit Remark: {3}</h6>
        <h6>Visited: {4}</h6>
        <a href="{5}" target="__blank">
            <img src="{5}" alt="No Image Available" height="250" width="250" data-toggle="tooltip" title="Click to view full image">
        </a>
    """.format(time, visit.visit_type, visit.visit_start_remark, visit.visit_close_remark, str(visit.visited), visit.visit_image_url)
    return markup
    
def __get_current_month_visits(request):
    companies = Onboarding.objects.filter(kam_name=request.GET.get('kam_id'))
    data = []
    for company in companies:
        completed_visit_count = len(list(Visit.objects.filter(kam_id=request.GET.get('kam_id'), company_name=company.corporate_name, visited=True, date_of_visit__month__gte=datetime.now().month)))
        planned_visit_count = len(list(Visit.objects.filter(kam_id=request.GET.get('kam_id'), company_name=company.corporate_name, visited=False, date_of_visit__month__gte=datetime.now().month)))
        data.append({
            'company_name': company.corporate_name,
            'completed_visit_count': completed_visit_count,
            'planned_visit_count': planned_visit_count,
        })
    
    return JsonResponse(data, safe=False)

def __delete_visit(request):
    visit = Visit.objects.filter(visit_id = request.GET.get('visit_id'))
    visit.delete()
    return JsonResponse({'Status': 'Done'}, safe=False)

def complete_visit(request):
    visit_id = request.POST.get('visit_id')
    visit = Visit.objects.get(visit_id=visit_id)

    if 'visit_image' in request.FILES:
        visit_image = request.FILES['visit_image']
        fs = FileSystemStorage()
        filename = fs.save('visit_images/' + visit_id + '/' + visit_image.name, visit_image)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        visit.visit_image_url = uploaded_file_url
    else:
        print("----No file found----")
    visit.visited = True
    visit.visit_close_remark = request.POST.get('visit_complete_remark')
    visit.last_updated = datetime.now()
    visit.status = request.POST.get('visit_success')
    visit.save()
    return redirect('visiting_home')
