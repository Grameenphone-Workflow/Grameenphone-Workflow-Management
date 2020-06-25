from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render
from .forms import LoginForm
from .models import GPUser, Ticket, Onboarding, TaskVsWFID, SLA, ProductRequisition, KAMTable, Item
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect
from random import randint
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from email.mime.application import MIMEApplication
from os.path import basename
from statistics import mean
import os
import pytz
import string

from pathlib import Path
import json

from zipfile import ZipFile

import imaplib
import smtplib
import email
import io
from bs4 import BeautifulSoup
import csv
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPException
import mimetypes
import random

def login(request):
    if 'user_phone_number' not in request.session:
        return render(request, 'login.html')
    else:
        return redirect('dashboard')

def clc_form(request):
    return render(request, 'clc_form.html')

def o2c_panel(request):
    return render(request, 'o2c_panel.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def download_file(request, path):
    print(path)
    print(request)
    # fill these variables with real values
    print(path)
    fl_path = Path(path)
    print(fl_path)
    print(fl_path.name)
    print(fl_path.is_file())
    filename = fl_path.name
    mime_type, _ = mimetypes.guess_type(fl_path.name)

    print("Before modifying: " + str(fl_path))

    if '/media' in str(fl_path):
        fl_path = Path(str(fl_path).replace('/media', 'data'))
        print("After modifying: " + str(Path(str(fl_path).replace('/media', 'data'))))
    
    try:
        response = FileResponse(open(fl_path, 'rb'))
    except:
        response = HttpResponse("<h1>The file does not exist</h1>")
    # print("TYPE- - -- - - - -- - ", type(fl))
    # print("TYPE- - -- - - - -- - ", fl.readlines())
    # response = HttpResponse(fl, content_type=mime_type)
    # response['Content-Disposition'] = "attachment; filename=%s" % filename
    # response['Content-Disposition'] = "inline"
        
    return(response)

def download_zip(request, company_name):
    print("Zipping for " + company_name)
    if company_name != "":
        print("Trying to make a zip file")
        zipObj = ZipFile('data/' + company_name + '.zip', 'w')
        for folderName, subfolders, filenames in os.walk("data/" + company_name):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                print("Adding file to zip." + filename)
                zipObj.write(filePath, filename)
        zipObj.close()
        # mime_type, _ = mimetypes.guess_type(zipf.name)
        # old = "data/" + company_name + ".zip"
        # print(company_name)
        # translator = str.maketrans('', '', string.punctuation)
        # company_name = company_name.translate(translator)
        # new = "data/" + company_name + ".zip"
        # print(company_name)
        # print(old)
        # print(new)
        # os.rename(old, new)

        response = HttpResponse(open('data/' + company_name + '.zip', 'rb'), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="' + company_name + '.zip"'
        return response

        # response = FileResponse(open(new, 'rb'), content_type='application\zip')
    else:
        response = HttpResponse("Error.")
    return(response)


def __submit_sim_serials(request):
    # TODO: use the starts, lasts and quantities to update the sim kit model
    wfid = request.GET.get('wfid')
    ticket = Ticket.objects.get(WFID=wfid)
    ticket.current_stage = "POD Generation"
    ticket.save()

# $.get("../__submit_sim_serials/",
#                 {
#                     wfid: wfid,
#                     starts: startSerials,
#                     lasts: lastSerials,
#                     quantitie: quantities,
#                 },

def reset(request):
    return render(request, 'reset_password.html')

def change_password(request):
    phone_number = request.POST.get('phone_number')
    code = request.POST.get('code')
    new = request.POST.get('new_password')
    if GPUser.objects.filter(phone_number=phone_number).exists():
        user = GPUser.objects.get(phone_number=phone_number)
        if user.pass_change_code == code:
            user.password = new
            user.pass_change_code = ""
            user.save()
    return redirect('login')

def send_code(request):
    phone = request.GET.get('phone_number')
    if GPUser.objects.filter(phone_number=phone).exists():
        user = GPUser.objects.get(phone_number=phone)
        random_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        user.pass_change_code = str(random_id)
        user.save()
        send_code_email(user.pass_change_code, user.phone_number)
        return HttpResponse("PASS")
    else:
        return HttpResponse("FAIL")

def get_code(request):
    phone = request.GET.get('phone_number')
    if GPUser.objects.filter(phone_number=phone).exists():
        user = GPUser.objects.get(phone_number=phone)
        if user.code == request.GET.get('code'):
            return HttpResponse("PASS")
        else:
            return HttpResponse("FAIL")
    else:
            return HttpResponse("FAIL")

def logout(request):
    if 'user_phone_number' not in request.session:
        return redirect('login')
    else:
        del request.session['user_phone_number']
        return redirect('login')

def task_configuration(request):
    print("hello world")

def start_workflow(request):
    if request.method == "POST":
        selected_workflow_type = request.POST.get('selected_workflow_type')
        print(selected_workflow_type)
    
    if selected_workflow_type == "ONBOARDING":
        return redirect('onboarding_form')
    elif selected_workflow_type == "PRODUCT_REQUISITION":
        return redirect('product_requisition_form')

def onboarding_form(request):
    phone = request.session.get('user_phone_number')
    user = GPUser.objects.get(phone_number=phone)
    context = {
        'role': request.session.get('role'),
        'customer': Onboarding(),
        'workflow_type': "Onboarding",
        'username': GPUser.objects.get(phone_number=phone).username,
        'phone': phone,
        'user': user
    }

    return render(request, 'onboarding_form.html', context)

def delete_request(request):
    wfid = request.GET.get('wfid')
    remark = request.GET.get('remark')
    kam_owner = Ticket.objects.get(WFID=wfid).kam_owner
    
    try:
        corp = TaskVsWFID.objects.get(wfid=wfid).task_identifier
        TaskVsWFID.objects.get(wfid=wfid).delete()
        Ticket.objects.get(WFID=wfid).delete()
        Onboarding.objects.get(corporate_name=corp).delete()
        SLA.objects.get(wfid=wfid).delete()
        send_delete_mail("COPC", "Onboarding", wfid, kam_owner, corp, remark)
        return HttpResponse('Deleted.')
    except:
        return HttpResponse('Something went horribly wrong.')
    

def product_requisition_form(request):
    phone = request.session.get('user_phone_number')
    print(GPUser.objects.get(phone_number=phone).username)
    user = GPUser.objects.get(phone_number=phone)
    kam_user = KAMTable.objects.get(username=user.username)
    context = {
        'role': request.session.get('role'),
        'product': ProductRequisition(),
        'workflow_type': "Product Requisition",
        'username': GPUser.objects.get(phone_number=phone).username,
        'phone': phone,
        'user': user,
        'kam_user': kam_user
    }

    return render(request, 'product_requisition.html', context)


def product_requisition_form_draft(request, wfid):
    thing = wfid
    crop = TaskVsWFID.objects.get(wfid=thing).task_identifier
    phone = request.session.get('user_phone_number')
    product = ProductRequisition.objects.get(wfid=thing, corporate_name=crop)
    ticket = Ticket.objects.get(WFID=thing)

    context = {
        'role': request.session.get('role'),
        'product': product,
        'workflow_type': "Product Requisition",
        'workflow_id': thing,
        'username': GPUser.objects.get(phone_number=phone).username,
        'user': GPUser.objects.get(phone_number=phone),
        'phone': phone,
        'current_stage': ticket.current_stage
    }
    if ticket.current_stage == "Drafting Form":
        return render(request, 'product_requisition.html', context)
    else:
        return render(request, 'o2c_panel.html', context)

def onboarding_form_draft(request, wfid):
    thing = wfid
    crop = TaskVsWFID.objects.get(wfid=thing).task_identifier
    phone = request.session.get('user_phone_number')
    customer = Onboarding.objects.get(corporate_name=crop)
    ticket = Ticket.objects.get(WFID=thing)
    print(customer.address1)
    print(ticket.current_stage)

    context = {
        'role': request.session.get('role'),
        'customer': customer,
        'workflow_type': "Onboarding",
        'workflow_id': thing,
        'completed_stages': ticket.completed_stages,
        'user': GPUser.objects.get(phone_number=phone),
        'phone': phone,
        'current_stage': ticket.current_stage
    }
    return render(request, 'onboarding_form.html', context)

def onboarding_sla_view(request):
    phone = request.session['user_phone_number']
    user = GPUser.objects.get(phone_number=phone)
    context = {
        'role': user.role,
        'username': user.username,
        'user': user
    }
    if user.role == "Superadmin":
        return render(request, 'sla_viz.html', context)
    else:
        return HttpResponse("<h1>You are not allowed to view this page.</h1>")


def dashboard(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = request.POST.get('phone_number')
            password = request.POST.get('password')

            if GPUser.objects.filter(phone_number=phone).exists():
                user = GPUser.objects.get(phone_number=phone)
                if user.password == str(password):
                    request.session['user_phone_number'] = user.phone_number
                    context = {
                        'role': user.role,
                        'username': user.username,
                        'user': user
                    }
                    print(user.username )
                    if user.role == "Superadmin":
                        for key, value in request.session.items():
                            print('{} => {}'.format(key, value))
                        return render(request, 'leaderdash.html', context)
                    else:
                        return render(request, 'dashboard.html', context)
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            return redirect('login')
    elif 'user_phone_number' not in request.session:
        return redirect('login')
    else:
        user_phone_number = request.session['user_phone_number']
        user = GPUser.objects.get(phone_number=user_phone_number)
        context = {
            'role': user.role,
            'username': user.username,
            'user': user
        }
        if user.role == "Superadmin":
            return render(request, 'leaderdash.html', context)
        else:
            return render(request, 'dashboard.html', context)


def fetch_tickets(request):
    
    tickets = Ticket.objects.all()
    data = []
    for ticket in tickets:
        taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
        data.append({
            "WFID": ticket.WFID,
            "Workflow Type": ticket.WFType,
            "BS Code": ticket.bs_code,
            "Company Name": taskvswfid.task_identifier,
            "Global Status": ticket.global_status,
            "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
            "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
            "Current Stage": ticket.current_stage,
            "Pending To": ticket.pending_to,
            "Remarks": ticket.remarks
        })
    thing = {"data": data }

    return JsonResponse(thing, safe=False)

def fetch_requisition_tickets(request):
    
    tickets = Ticket.objects.all()
    data = []
    for ticket in tickets:
        taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
        if ticket.WFType == "Product Requisition" and ticket.current_stage != "Drafting Form":
            data.append({
                "WFID": ticket.WFID,
                "Workflow Type": ticket.WFType,
                "BS Code": ticket.bs_code,
                "Company Name": taskvswfid.task_identifier,
                "Global Status": ticket.global_status,
                "KAM Owner": ticket.kam_owner,
                "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                "Current Stage": ticket.current_stage,
                "Pending To": ticket.pending_to,
                "Remarks": ticket.remarks
            })
    thing = {"data": data }

    return JsonResponse(thing, safe=False)

def fetch_onboarding_tickets(request):
    
    tickets = Ticket.objects.all()
    data = []
    for ticket in tickets:
        taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
        if ticket.WFType == "Onboarding" and ticket.current_stage != "Drafting Form":
            data.append({
                "WFID": ticket.WFID,
                "Workflow Type": ticket.WFType,
                "BS Code": ticket.bs_code,
                "Company Name": taskvswfid.task_identifier,
                "Global Status": ticket.global_status,
                "KAM Owner": ticket.kam_owner,
                "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                "Current Stage": ticket.current_stage,
                "Pending To": ticket.pending_to,
                "Remarks": ticket.remarks
            })
    thing = {"data": data }

    return JsonResponse(thing, safe=False)

def fetch_tickets_specific(request):
    
    tickets = Ticket.objects.all()
    role = request.GET.get('role')
    username = request.GET.get('username')
    data = [] 
    if role == "KAM":
        for ticket in tickets:
            if ticket.kam_owner == username and ticket.current_stage == "Drafting Form":
                taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
                data.append({
                    "WFID": ticket.WFID,
                    "Workflow Type": ticket.WFType,
                    "BS Code": ticket.bs_code,
                    "Company Name": taskvswfid.task_identifier,
                    "Global Status": ticket.global_status,
                    "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                    "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                    "Current Stage": ticket.current_stage,
                    "Pending To": ticket.pending_to,
                    "Remarks": ticket.remarks
                })
        thing = {"data": data}
    elif role == "COPC":
            for ticket in tickets:
                if ticket.current_stage == "Onboarding Request":
                    taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
                    data.append({
                        "WFID": ticket.WFID,
                        "Workflow Type": ticket.WFType,
                        "BS Code": ticket.bs_code,
                        "Company Name": taskvswfid.task_identifier,
                        "Global Status": ticket.global_status,
                        "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                        "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                        "Current Stage": ticket.current_stage,
                        "Pending To": ticket.pending_to,
                        "Remarks": ticket.remarks
                    })
    thing = {"data": data }
    return JsonResponse(thing, safe=False)

def fetch_copc_tickets(request):
    tickets = Ticket.objects.all()
    data = []
    for ticket in tickets:
        taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
        data.append({
            "WFID": ticket.WFID,
            "Workflow Type": ticket.WFType,
            "KAM Owner": ticket.kam_owner,
            "BS Code": ticket.bs_code,
            "Company Name": taskvswfid.task_identifier,
            "Global Status": ticket.global_status,
            "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
            "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
            "Current Stage": ticket.current_stage,
            "Pending To": ticket.pending_to,
            "Remarks": ticket.remarks
        })
    thing = {"data": data }

    return JsonResponse(thing, safe=False)


def tickets(request):
    print(request.session)
    phone = request.session['user_phone_number'] 
    print(phone)
    user = GPUser.objects.get(phone_number=phone)
    context = {
        'role': user.role,
        'username': user.username,
        'user': user
    }
    return render(request, 'tickets.html', context)

def requisition_tickets(request):
    print(request.session)
    phone = request.session['user_phone_number'] 
    print(phone)
    user = GPUser.objects.get(phone_number=phone)
    context = {
        'role': user.role,
        'username': user.username,
        'user': user
    }
    return render(request, 'requisition_tickets.html', context)

def __kam_tickets(request):
    
    tickets = Ticket.objects.all()
    role = request.GET.get('role')
    username = request.GET.get('username')
    requested_type = request.GET.get('requested_type')
    data = []
    for ticket in tickets:
        if ticket.kam_owner == username and ticket.WFType == requested_type:
            taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
            data.append({
                "WFID": ticket.WFID,
                "Workflow Type": ticket.WFType,
                "BS Code": ticket.bs_code,
                "Company Name": taskvswfid.task_identifier,
                "Global Status": ticket.global_status,
                "First Issued": ticket.first_issued_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                "Last Updated": ticket.last_update_datetime.strftime("%d-%b-%Y (%H:%M:%S)"),
                "Current Stage": ticket.current_stage,
                "Pending To": ticket.pending_to,
                "Remarks": ticket.remarks
            })
    thing = {"data": data}

    return JsonResponse(thing, safe=False)


def fetch_gerp_table(request):
    
    tickets = Ticket.objects.all()
    data = []
    for ticket in tickets:
        if "BS Code Publish" in ticket.completed_stages and "GERP Code Creation" not in ticket.completed_stages:
            taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
            corp = taskvswfid.task_identifier
            if Onboarding.objects.filter(corporate_name=corp).exists():
                customer = Onboarding.objects.get(corporate_name=corp)
                data.append({
                    "Date": ticket.last_update_datetime.date(),
                    "Time": ticket.last_update_datetime.time(),
                    "WFID": ticket.WFID,
                    "Request Task": "Customer Creation",
                    "Customer Number": "BD" + str(ticket.bs_code),
                    "Customer Name": str(customer.corporate_name).upper(),
                    "Vendor Type": "Domestic",
                    "Customer Type": "External",
                    "Tax Payer ID": "",
                    "Tax Registration Number (VAT)": "",
                    "Customer Address 1": str(customer.gerp_address).upper(),
                    "Customer Address 2": "",
                    "Customer Address 3": "",
                    "City": str(customer.city).upper(),
                    "Postal Code": customer.zip_code,
                    "Country": "Bangladesh",
                })
    thing = {"data": data}


    return JsonResponse(thing, safe=False)


def fetch_lerp_table(request):
    print("Here I am ")
    
    tickets = Ticket.objects.all()
    
    data = []
    for ticket in tickets:
        if "GERP Code Creation" in ticket.completed_stages and "LERP Code Creation" not in ticket.completed_stages:
            taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
            corp = taskvswfid.task_identifier
            customer = Onboarding.objects.get(corporate_name=corp)
            data.append({
                "Date": ticket.last_update_datetime.date(),
                "Time": ticket.last_update_datetime.time(),
                "WFID": ticket.WFID,
                "Partner Number": "BD" + str(ticket.bs_code),
                "Partner Name": str(customer.corporate_name),
                "Partner Category": "CORPORATE CLIENT",
                "Partner Type": "CORP",
                "Address": str(customer.address1),
                "Country": "BANGLADESH",
                "City": customer.thana,
                "District": customer.district,
            })
    thing = {"data": data}
    # print(data)

    return JsonResponse(thing, safe=False)


def fetch_lerp_table_2(request):
    tickets = Ticket.objects.all()
    
    data = []
    for ticket in tickets:
        if "GERP Code Creation" in ticket.completed_stages and "LERP Code Creation" not in ticket.completed_stages:
            taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
            corp = taskvswfid.task_identifier
            customer = Onboarding.objects.get(corporate_name=corp)
            data.append({
                "Date": ticket.last_update_datetime.date(),
                "Time": ticket.last_update_datetime.time(),
                "WFID": ticket.WFID,
                "Company Code": customer.corporate_short_name,
                "Company Name": customer.corporate_name,
                "BSCODE": customer.bscode,
                "Company Context": "GP CORPORATE SALES",
                "VAT Reg Num": "7802" + str(customer.bscode),
                "Company Address": customer.address1,
                "Employee ID": "",
                "Entry Date": ticket.first_issued_datetime,
                "District": customer.district,
                "ERP Cust Num": "BD" + str(customer.bscode),
                "Disable Date": "",
            })
    thing = {"data": data}
    # print(data)

    return JsonResponse(thing, safe=False)

def fetch_clc_table(request):
    
    tickets = Ticket.objects.all()
    
    data = []
    for ticket in tickets:
        taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
        corp = taskvswfid.task_identifier
        if ("OBD" in ticket.WFID):
            continue
        if ProductRequisition.objects.filter(corporate_name=corp):
            product = ProductRequisition.objects.get(corporate_name=corp)
            data.append({
                "WFID": ticket.WFID,
                "KAM ID": product.kam_id,
                "KAM Name": product.kam_name,
                "Mobile No": product.kam_mobile,
                "Description": product.description,
                "QTY": product.quantity,
                "Item Type": product.item_type,
                "Remarks": ticket.remarks,
                "ERP Code": product.erp_code,
            })
    thing = {"data": data}
    # print(data)

    return JsonResponse(thing, safe=False)

def fetch_va_table(request):
    
    tickets = Ticket.objects.all()
    
    data = []
    for ticket in tickets:
        try:
            if "VA Code Creation" not in ticket.completed_stages and "BS Code Publish" in ticket.completed_stages:
                taskvswfid = TaskVsWFID.objects.get(wfid=ticket.WFID)
                corp = taskvswfid.task_identifier
                customer = Onboarding.objects.get(corporate_name=corp)
                data.append({
                    "Date": ticket.last_update_datetime.date(),
                    "Time": ticket.last_update_datetime.time(),
                    "WFID": ticket.WFID,
                    "KAM": str(customer.kam_name),
                    "Company Type": customer.corporate_type,
                    "BS Code": str(customer.bscode),
                    "Company Type": customer.corporate_type,
                    "Company Name": customer.corporate_name,
                    "Remarks": "SCB/City",
                    "VA Code (Usage)": "7802" + str(customer.bscode),
                    "VA Code (Start-up)": "7812" + str(customer.bscode),
                })
        except:
            pass
    thing = {"data": data}
    # print(thing)
    return JsonResponse(thing, safe=False)

def onboard(request):
    print(request.POST)
    corp = request.POST.get('corporate_name')
    corporate_name = request.POST.get('corporate_name')
    bs_code = request.POST.get('bs_code')
    
    # Create or update an onboarding object based on the request.
    onboarding_cu(request)

    workflow_id = request.POST.get('workflow_id')

    if workflow_id is "":
        # Generate a unique workflow ID.
        workflow_id = "OBD" + datetime.now().strftime('%d%m%Y%H%M%S')


    # Generate a ticket.
    ticket = Ticket()
    taskvswfid = ""
    if Ticket.objects.filter(WFID=workflow_id).exists():
        ticket = Ticket.objects.get(WFID=workflow_id)
    else: 
        ticket = Ticket()
        ticket.first_issued_datetime = datetime.now()
        ticket.WFID = workflow_id
        ticket.WFType = "Onboarding"
        ticket.global_status = "Pending"
        ticket.completed_stages = ""
    ticket.bs_code = bs_code
    ticket.kam_owner = request.POST.get('kam_name')

    if ticket.completed_stages == "":
        ticket.current_stage = "Drafting Form"

    ticket.last_update_datetime = datetime.now()
    ticket.pending_to = request.POST.get('kam_name')
    ticket.corporate_name = request.POST.get('corporate_name')
    # ticket.completed_stages = ""

    ticket.save()

    if TaskVsWFID.objects.filter(wfid=workflow_id).exists():
        print("WFID already exists. updating")
        taskvswfid = TaskVsWFID.objects.get(wfid=workflow_id)
    else: 
        print("Nothing found")
        taskvswfid = TaskVsWFID()
    
    taskvswfid.task_identifier = corporate_name
    taskvswfid.wfid = ticket.WFID
    taskvswfid.workflow_type = ticket.WFType
    taskvswfid.save()
    
    return redirect('dashboard')

def __fire_next(request):
    # Request has, at the moment.
    # The remark, the wfid, and the role.

    requested_wfid = request.GET.get('wfid')
    role = request.GET.get('role')
    remark = request.GET.get('submit_remark')


    ticket = Ticket.objects.get(WFID=requested_wfid)
    taskvswfid = TaskVsWFID.objects.get(wfid=requested_wfid)
    old_stage = ticket.current_stage

    corporate_name = taskvswfid.task_identifier

    if (role == "KAM"):
        ticket.current_stage = "Onboarding Request"
        if "Onboarding Request" not in ticket.completed_stages:
            ticket.completed_stages += "Onboarding Request"
    elif (role == "COPC"):
        ticket.current_stage = "BS Code Publish"
        if "BS Code Publish" not in ticket.completed_stages:
            ticket.completed_stages += "BS Code Publish"
    elif (role == "GERP"):
        ticket.current_stage = "GERP Code Creation"
        if "GERP Code Creation" not in ticket.completed_stages:
            ticket.completed_stages += "GERP Code Creation"
    elif (role == "LERP"):
        ticket.current_stage = "LERP Code Creation"
        if "LERP Code Creation" not in ticket.completed_stages:
            ticket.completed_stages += "LERP Code Creation"
            company = Onboarding.objects.get(corporate_name=corporate_name)
            company.erp_company_code = request.GET.get('erp_code')
            company.save()
    elif (role == "VA"):
        ticket.current_stage = "VA Code Creation"
        if "VA Code Creation" not in ticket.completed_stages:
            ticket.completed_stages += "VA Code Creation"
    
    stages = ["Onboarding Request", 
            "BS Code Publish",
            "GERP Code Creation",
            "LERP Code Creation",
            "VA Code Creation",
            ]

    ticket.global_status = "Completed"
    Onboarding.objects.get(corporate_name=corporate_name).onboarded = True
    
    for stage in stages:
        if stage not in ticket.completed_stages:
            ticket.global_status = "Pending"
            Onboarding.objects.get(corporate_name=corporate_name).onboarded = False

    
    ticket.remarks = remark

    # ticket.last_update_datetime = datetime.now()
    ticket.pending_to = request.GET.get('username')
    ticket.last_update_datetime = datetime.now()
    ticket.save()

    if SLA.objects.filter(wfid=requested_wfid, task=old_stage, workflow_type="Onboarding").exists():
        sla = SLA.objects.get(wfid=requested_wfid, task=old_stage, workflow_type="Onboarding")
        sla.completion_time = datetime.now()
        duration = sla.completion_time - sla.fire_time
        duration = duration.total_seconds()
        sla.actual_difference = duration
        if (sla.actual_difference < sla.expected_difference):
            sla.status = True
        else:
            sla.status = False
        sla.save()
    
    sla = SLA()
    sla.wfid = requested_wfid
    sla.task = ticket.current_stage
    sla.workflow_type = "Onboarding"
    sla.fire_time = datetime.now()
    sla.expected_difference =  86400.0
    sla.user_identifier = request.GET.get('username')
    sla.status = False
    sla.save()

    try:
        send_test_email(role=role, wftype="Onboarding", requested_wfid=requested_wfid, old_stage=old_stage, kam_owner=ticket.kam_owner, bscode=ticket.bs_code, company=corporate_name)
    except:
        print("mail sending failed")
        pass
    # if (role == "COPC"):
        # send_lerp_csv()
        # TODO: Fix this.

    return HttpResponse("")

def __reject_prev(request):
    requested_wfid = request.GET.get('wfid')
    taskvswfid = TaskVsWFID.objects.get(wfid=requested_wfid)
    corporate_name = taskvswfid.task_identifier
    role = request.session.get('role')

    # I now have the wfid and onboarding form.
    # Now I need the ticket.

    ticket = Ticket.objects.get(WFID=requested_wfid)

    ticket.remarks = request.GET.get('rejection_remark')
    print(ticket.remarks)
    
    ticket.last_update_datetime = datetime.now()
    ticket.save()
    # sla = SLA()
    # sla.wfid = ticket.WFID
    # sla.fire_time = ticket.last_update_datetime
    # sla.completion_time = datetime.now()
    # sla.stage = ticket.current_stage
    # sla.save()

    return HttpResponse("")

def __get_all_corp_names(request):
    
    passed_name = request.GET['corp_name']
    
    if Onboarding.objects.filter(corporate_name=passed_name).exists():
        return HttpResponse("Exists")
    else:
        return HttpResponse("Unique")
    
def check_bs_code(request):
    
    bscode = request.GET['bscode']
    
    if Onboarding.objects.filter(bscode=bscode).exists():
        return HttpResponse("Exists")
    else:
        return HttpResponse("Unique")

def __get_onboard_for_bscode(request):
    bscode = request.GET.get('bscode')
    oboarding = ""
    if Onboarding.objects.filter(bscode=bscode).exists():
        onboarding = Onboarding.objects.get(bscode=bscode)
        data = []
        data.append({
            'customer': onboarding.corporate_name,
            'subsegment': onboarding.subsegment,
            'zone': onboarding.zone,
            'region': onboarding.bs_customer_region,
        })
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Unique")
    return HttpResponse("")

def send_code_email(code, username):
    print("Trying to send an email.")
    text = "Your reset code is " + code + "."
    message = MIMEMultipart(
        "alternative", None, [MIMEText(text)])
    me = open('.me').readline()
    password = open('.password').readline()
    server = open('.mailserver').readline()
    message['Subject'] = "Workflow Lite password change requested."
    message['From'] = me
    message['To'] = username + '@grameenphone.com'
    print(message['To'])
    message["Cc"] = me
    server = smtplib.SMTP(server)
    # server.connect()
    server.set_debuglevel(True)
    server.ehlo()
    # server.starttls()
    # server.login(me, password)
    server.sendmail(me, message["To"], message.as_string())
    server.quit()
    print("An email has been sent")

def send_test_email(role, wftype, requested_wfid, kam_owner, old_stage, bscode, company):
    print("Trying to send an email.")
    text = get_mail_text(role=role, wftype="Onboarding", requested_wfid=requested_wfid, old_stage=old_stage, kam_owner=kam_owner, bscode=bscode, company=company)
    message = MIMEMultipart(
        "alternative", None, [MIMEText(text)])
    me = open('.me').readline()
    password = open('.password').readline()
    server = open('.mailserver').readline()
    you = open('.recievers').readline()
    print("KAM Owner:" + kam_owner)
    message['Subject'] = "[" + bscode + "]" + " " + old_stage + " done for "  + company
    message['From'] = me
    message['To'] = kam_owner + '@grameenphone.com'
    print(message['To'])
    message["Cc"] = me
    server = smtplib.SMTP(server)
    # server.connect()
    server.set_debuglevel(True)
    server.ehlo()
    # server.starttls()
    # server.login(me, password)
    server.sendmail(me, [message["To"], me], message.as_string())
    server.quit()
    print("An email has been sent")

def send_delete_mail(role, wftype, requested_wfid, kam_owner, company, remark):
    print("Trying to send an email.")
    text = requested_wfid + " has been deleted. Company Name: " + company + " , KAM Owner: " + kam_owner + ", Remark: " + remark
    message = MIMEMultipart(
        "alternative", None, [MIMEText(text)])
    me = open('.me').readline()
    password = open('.password').readline()
    server = open('.mailserver').readline()
    you = open('.recievers').readline()
    print("KAM Owner:" + kam_owner)
    message['Subject'] = "Ticket " + requested_wfid + "deleted for "  + company
    message['From'] = me
    message['To'] = kam_owner + '@grameenphone.com'
    print(message['To'])
    message["Cc"] = me
    server = smtplib.SMTP(server)
    # server.connect()
    server.set_debuglevel(True)
    server.ehlo()
    # server.starttls()
    # server.login(me, password)
    server.sendmail(me, [message["To"], me], message.as_string())
    server.quit()
    print("An email has been sent")

def send_requisition_email(
    wfid,
    previous_stage,
    bscode,
    company_name,
    kam_owner,
    current_pending_stage,
    role_owner,
    remarks,
):

    html = """
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>O2C Status Table</title>
    <style type="text/css" media="screen">
        table{
            empty-cells:hide;
            background-color: white;
        }
    </style>
    </head>

    <html><body>
    <p>O2C Reference Number: %s</p>
    <table border="1"> 
    <tr>
        <td>BSCODE</td>
        <td>COMPANY NAME</td>
        <td>KAM OWNER</td>
        <td>Current Pending Stage</td>
        <td>ROLE OWNER</td>
        <td>Remarks</td>
    </tr>
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
    </table>
    <p>Regards,</p>
    <p>Workflow<sup class="font-weight-light">Lite</sup></p>
    </body></html>""" % (wfid, bscode, company_name, kam_owner, current_pending_stage, role_owner, remarks)


    message = MIMEMultipart("alternative", None, [MIMEText(html, 'html')])

    me = open('.me').readline()
    password = open('.password').readline()
    server = open('.mailserver').readline()
    you = open('.recievers').readline()

    message['Subject'] = "'" + previous_stage + "' done for '" + company_name + "'"
    message['From'] = me
    message['To'] = kam_owner + '@grameenphone.com'
    server = smtplib.SMTP(server)
    server.ehlo()
    # server.starttls()
    # server.login(me, password)
    server.set_debuglevel(True)
    server.sendmail(me, message['To'], message.as_string())
    server.quit()
    print("mail sent")

def product_form(request):
    print(request.POST)

    workflow_id = request.POST.get('workflow_id')

    if workflow_id is "" or workflow_id is None:
        workflow_id = "O2C" + datetime.now().strftime('%d%m%Y%H%M%S')

    corporate_name = request.POST.get('corporate_name')

    product_requisition = ProductRequisition()
    if (ProductRequisition.objects.filter(wfid=workflow_id, corporate_name=corporate_name).exists()):
        product_requisition = ProductRequisition.objects.get(wfid=workflow_id, corporate_name=corporate_name)
    else:
        product_requisition.corporate_name = request.POST.get('corporate_name')
        product_requisition.wfid = workflow_id
        
    # KAM Information
    product_requisition.kam_id = request.POST.get('kam_id')
    product_requisition.kam_name = request.POST.get('kam_name')
    product_requisition.kam_mobile = request.POST.get('kam_mobile')
    # product_requisition.kam_designation = request.POST.get('kam_designation')
    # product_requisition.kam_email = request.POST.get('kam_email')
    product_requisition.kam_location = request.POST.get('kam_location')
    product_requisition.kam_department = request.POST.get('kam_department')

    # Company Information
    # Company Information
    product_requisition.bs_code = request.POST.get('bs_code')
    product_requisition.corporate_name = request.POST.get('corporate_name')
    product_requisition.sub_segment = request.POST.get('sub_segment')
    product_requisition.zone = request.POST.get('zone')
    product_requisition.product_name = request.POST.get('product_name')
    product_requisition.erp_code = request.POST.get('erp_code')
    product_requisition.quantity = request.POST.get('quantity')
    product_requisition.unit_price = request.POST.get('unit_price')
    product_requisition.total_price = request.POST.get('total_price')

    # Client contact person information
    product_requisition.client_contact_person = request.POST.get('client_contact_person')
    product_requisition.client_mobile_number = request.POST.get('client_mobile_number')
    product_requisition.product_delivery_address = request.POST.get('product_delivery_address')

    # Authorized person information
    product_requisition.authorized_person_name = request.POST.get('authorized_person_name')
    product_requisition.authorized_person_contact_no = request.POST.get('authorized_person_contact_no')
    product_requisition.authorized_person_email = request.POST.get('authorized_person_email')
    product_requisition.authorized_person_designation = request.POST.get('authorized_person_designation')
    product_requisition.authorized_person_nid_number = request.POST.get('authorized_person_nid_number')
    
    
    product_requisition.remarks = request.POST.get('remarks')
    
    product_requisition.total_employee = request.POST.get('total_employee')
    product_requisition.total_sim = request.POST.get('total_sim')
    product_requisition.bsm_authorized_person_name = request.POST.get('bsm_authorized_person_name')
    product_requisition.bsm_authorized_person_nid_number = request.POST.get('bsm_authorized_person_nid_number')
    product_requisition.applicable_district = request.POST.get('applicable_district')
    product_requisition.bde_name = request.POST.get('bde_name')
    product_requisition.bde_pos_code = request.POST.get('bde_pos_code')
    product_requisition.sales_credit_option = request.POST.get('sales_credit_option')
    product_requisition.btrc_approval_type = request.POST.get('btrc_approval_type')
    product_requisition.btrc_approval_option = request.POST.get('btrc_approval_option')
    product_requisition.btrc_approval_taken_option = request.POST.get('btrc_approval_taken_option')


    if request.method == 'POST' and 'work_order_application' in request.FILES:
        wo_file = request.FILES['work_order_application']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/wo/' + corporate_name + '_' + wo_file.name, wo_file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.work_order_application = uploaded_file_url

    if request.method == 'POST' and 'btrc_form_20191000' in request.FILES:
        btrc_form_20191000 = request.FILES['btrc_form_20191000']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/btrc_form_20191000/' + corporate_name + '_' + btrc_form_20191000.name, btrc_form_20191000)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.btrc_form_20191000 = uploaded_file_url
    
    if request.method == 'POST' and 'poc_id' in request.FILES:
        poc_id = request.FILES['poc_id']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/poc_id/' + corporate_name + '_' + poc_id.name, poc_id)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.poc_id = uploaded_file_url

    
    if request.method == 'POST' and 'btrc_form_20191001' in request.FILES:
        btrc_form_20191001 = request.FILES['btrc_form_20191001']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/btrc_form_20191001/' + corporate_name + '_' + btrc_form_20191001.name, btrc_form_20191001)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.btrc_form_20191001 = uploaded_file_url

    
    if request.method == 'POST' and 'btrc_form_20191002' in request.FILES:
        btrc_form_20191002 = request.FILES['btrc_form_20191002']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/btrc_form_20191002/' + corporate_name + '_' + btrc_form_20191002.name, btrc_form_20191002)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.btrc_form_20191002 = uploaded_file_url

    if request.method == 'POST' and 'nid_kcp' in request.FILES:
        nid_kcp = request.FILES['nid_kcp']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/nid_kcp/' + corporate_name + '_' + nid_kcp.name, nid_kcp)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.nid_kcp = uploaded_file_url
    
    if request.method == 'POST' and 'poc_billing_address' in request.FILES:
        poc_billing_address = request.FILES['poc_billing_address']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/poc_billing_address/' + corporate_name + '_' + poc_billing_address.name, poc_billing_address)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.poc_billing_address = uploaded_file_url
    
    if request.method == 'POST' and 'agreement_copy' in request.FILES:
        agreement_copy = request.FILES['agreement_copy']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/agreement_copy/' + corporate_name + '_' + agreement_copy.name, agreement_copy)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.agreement_copy = uploaded_file_url

    if request.method == 'POST' and 'ams_start_up' in request.FILES:
        ams_start_up = request.FILES['ams_start_up']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/ams_start_up/' + corporate_name + '_' + ams_start_up.name, ams_start_up)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.ams_start_up = uploaded_file_url

    if request.method == 'POST' and 'ams_rate_plan' in request.FILES:
        ams_rate_plan = request.FILES['ams_rate_plan']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/ams_rate_plan/' + corporate_name + '_' + ams_rate_plan.name, ams_rate_plan)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.ams_rate_plan = uploaded_file_url


    if request.method == 'POST' and 'ams_both' in request.FILES:
            ams_both = request.FILES['ams_both']
            fs = FileSystemStorage()
            filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/ams_both/' + corporate_name + '_' + ams_both.name, ams_both)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            product_requisition.ams_both = uploaded_file_url

    if request.method == 'POST' and 'other' in request.FILES:
        other = request.FILES['other']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/other/' + corporate_name + '_' + other.name, other)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.other = uploaded_file_url

    if request.method == 'POST' and 'previous_btrc_form_20191000' in request.FILES:
        previous_btrc_form_20191000 = request.FILES['previous_btrc_form_20191000']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/previous_btrc_form_20191000/' + corporate_name + '_' + previous_btrc_form_20191000.name, previous_btrc_form_20191000)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.previous_btrc_form_20191000 = uploaded_file_url

    if request.method == 'POST' and 'previous_btrc_form_20191003' in request.FILES:
        previous_btrc_form_20191003 = request.FILES['previous_btrc_form_20191003']
        fs = FileSystemStorage()
        filename = fs.save('product/' + workflow_id + '/' + corporate_name + '/previous_btrc_form_20191003/' + corporate_name + '_' + previous_btrc_form_20191003.name, previous_btrc_form_20191003)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        product_requisition.previous_btrc_form_20191003 = uploaded_file_url

    product_requisition.save()

    test_wfid = workflow_id
    print(workflow_id)
    # Generate a ticket.
    ticket = Ticket()
    taskvswfid = ""
    if Ticket.objects.filter(WFID=workflow_id).exists():
        ticket = Ticket.objects.get(WFID=workflow_id)
    else: 
        ticket = Ticket()
        ticket.first_issued_datetime = datetime.now()
        ticket.WFID = workflow_id
        ticket.WFType = "Product Requisition"
        ticket.global_status = "Pending"
        ticket.completed_stages = ""

    ticket.bs_code = product_requisition.bs_code
    ticket.kam_owner = request.POST.get('kam_name')

    if ticket.completed_stages == "":
        ticket.current_stage = "Drafting Form"

    ticket.last_update_datetime = datetime.now()
    ticket.pending_to = request.POST.get('kam_name')
    ticket.corporate_name = request.POST.get('corporate_name')
    ticket.completed_stages = ""

    ticket.save()

    if TaskVsWFID.objects.filter(wfid=workflow_id).exists():
        print("WFID already exists. updating")
        taskvswfid = TaskVsWFID.objects.get(wfid=workflow_id)
    else: 
        print("Nothing found")
        taskvswfid = TaskVsWFID()
    
    taskvswfid.task_identifier = corporate_name
    taskvswfid.wfid = ticket.WFID
    taskvswfid.workflow_type = ticket.WFType
    taskvswfid.save()
    
    return redirect('dashboard')

def __fire_next_requisition(request):

    requested_wfid = request.GET.get('wfid')
    remark = request.GET.get('submit_remark')
    next_stage = request.GET.get('next_stage')


    ticket = Ticket.objects.get(WFID=requested_wfid)
    taskvswfid = TaskVsWFID.objects.get(wfid=requested_wfid)
    old_stage = request.GET.get('previous_stage')

    previous_stage = ticket.current_stage
    print("Previous Stage: " + previous_stage)
    corporate_name = taskvswfid.task_identifier

    if next_stage is None:
        print("Did not find a next stage")
        ticket.current_stage = "Product Requisition by KAM"
        next_stage = "Product Requisition by KAM"
    else:
        ticket.current_stage = next_stage

    if next_stage == "Completed":
        ticket.current_stage = "Completed"
        ticket.global_status = "Completed"
    
    # if ticket.current_stage == "Drafting Form":
    #     ticket.current_stage = "Product Requisition"
    #     if "Drafting Form" not in ticket.completed_stages:
    #         ticket.completed_stages += "Drafting Form"
    # elif ticket.current_stage == "Product Requisition":
    #     ticket.current_stage = "Product Approval"
    #     if "Product Requisition" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Requisition"
    # elif ticket.current_stage == "Product Approval":
    #     ticket.current_stage = "Product Allocation"
    #     if "Product Approval" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Approval"
    # elif ticket.current_stage == "Product Approval":
    #     ticket.current_stage = "POD Generation"
    #     if "Product Allocation" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Allocation"
    # elif ticket.current_stage == "POD Generation":
    #     ticket.current_stage = "Request for BTRC Approval"
    #     if "POD Generation" not in ticket.completed_stages:
    #         ticket.completed_stages += "POD Generation"
    # elif ticket.current_stage == "Request for BTRC Approval":
    #     ticket.current_stage = "Document Received for BTRC Approval"
    #     if "Request for BTRC Approval" not in ticket.completed_stages:
    #         ticket.completed_stages += "Request for BTRC Approval"   
    # elif ticket.current_stage == "Document Received for BTRC Approval":
    #     ticket.current_stage = "Submit to BTRC"
    #     if "Document Received for BTRC Approval" not in ticket.completed_stages:
    #         ticket.completed_stages += "Document Received for BTRC Approval" 
    # elif ticket.current_stage == "Submit to BTRC":
    #     ticket.current_stage = "BTRCApproval"
    #     if "Submit to BTRC" not in ticket.completed_stages:
    #         ticket.completed_stages += "Submit to BTRC"
    # elif ticket.current_stage == "BTRCApproval":
    #     ticket.current_stage = "Sales Order"
    #     if "BTRCApproval" not in ticket.completed_stages:
    #         ticket.completed_stages += "BTRCApproval"   
    # elif ticket.current_stage == "Sales Order":
    #     ticket.current_stage = "MR Creation Request"
    #     if "Sales Order" not in ticket.completed_stages:
    #         ticket.completed_stages += "Sales Order"
    # elif ticket.current_stage == "MR Creation Request":
    #     ticket.current_stage = "MR Created"
    #     if "MR Creation Request" not in ticket.completed_stages:
    #         ticket.completed_stages += "MR Creation Request"
    # elif ticket.current_stage == "MR Created":
    #     ticket.current_stage = "Product Delivery Request"
    #     if "MR Created" not in ticket.completed_stages:
    #         ticket.completed_stages += "MR Created"
    # elif ticket.current_stage == "Product Delivery Request":
    #     ticket.current_stage = "Delivery Request Approval"
    #     if "Product Delivery Request" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Delivery Request"
    # elif ticket.current_stage == "Delivery Request Approval":
    #     ticket.current_stage = "Product Delivery to GP Representative"
    #     if "Delivery Request Approval" not in ticket.completed_stages:
    #         ticket.completed_stages += "Delivery Request Approval"
    # elif ticket.current_stage == "Product Delivery to GP Representative":
    #     ticket.current_stage = "Product Delivery Request to Deliver Agency"
    #     if "Product Delivery to GP Representative" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Delivery to GP Representative"
    # elif ticket.current_stage == "Product Delivery Request to Deliver Agency":
    #     ticket.current_stage = "Product Received by Agency/KAM/ZM"
    #     if "Product Delivery Request to Deliver Agency" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Delivery Request to Deliver Agency"
    # elif ticket.current_stage == "Product Received by Agency/KAM/ZM":
    #     ticket.current_stage = "POS Code Assign"
    #     if "Product Received by Agency/KAM/ZM" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Received by Agency/KAM/ZM"
    # elif ticket.current_stage == "POS Code Assign":
    #     ticket.current_stage = "Product Delivered to Customer"
    #     if "POS Code Assign" not in ticket.completed_stages:
    #         ticket.completed_stages += "POS Code Assign"
    # elif ticket.current_stage == "Product Delivered to Customer":
    #     ticket.current_stage = "BTRC Form No - 20191003 with User Info"
    #     if "Product Delivered to Customer" not in ticket.completed_stages:
    #         ticket.completed_stages += "Product Delivered to Customer"
    # elif ticket.current_stage == "BTRC Form No - 20191003 with User Info":
    #     ticket.current_stage = "Biometric and KCP Creation"
    #     if "BTRC Form No - 20191003 with User Info" not in ticket.completed_stages:
    #         ticket.completed_stages += "BTRC Form No - 20191003 with User Info"
    # elif ticket.current_stage == "Biometric and KCP Creation":
    #     ticket.current_stage = "Activation"
    #     if "Biometric and KCP Creation" not in ticket.completed_stages:
    #         ticket.completed_stages += "Biometric and KCP Creation"
    # elif ticket.current_stage == "Activation":
    #     ticket.current_stage = "Document Archiving"
    #     if "Activation" not in ticket.completed_stages:
    #         ticket.completed_stages += "Activation"
    # elif ticket.current_stage == "Document Archiving":
    #     ticket.current_stage = "Document Archiving"
    #     if "Document Archiving" not in ticket.completed_stages:
    #         ticket.completed_stages += "Document Archiving"
    #         ticket.global_status = "Completed"

    ticket.remarks = remark

    # ticket.last_update_datetime = datetime.now()
    ticket.pending_to = request.GET.get('username')
    ticket.last_update_datetime = datetime.now()
    ticket.save()

    if SLA.objects.filter(wfid=requested_wfid, task=old_stage, workflow_type="Product Requisition").exists():
        print("sla already exists, updating")
        sla = SLA.objects.get(wfid=requested_wfid, task=old_stage, workflow_type="Product Requisition")
        sla.completion_time = datetime.now()
        duration = sla.completion_time - sla.fire_time
        duration = duration.total_seconds()
        sla.actual_difference = duration
        if (sla.actual_difference < sla.expected_difference):
            sla.status = True
        else:
            sla.status = False

        if old_stage == "Product Requisition by KAM":
            sla.completion_time = sla.fire_time
        sla.save()

    if SLA.objects.filter(wfid=requested_wfid, task=next_stage, workflow_type="Product Requisition").exists():
        print("sla already exists, updating")
        sla = SLA.objects.get(wfid=requested_wfid, task=next_stage, workflow_type="Product Requisition")
        sla.fire_time = datetime.now()
    else:
        print("creating a new SLA")
        sla = SLA()
        sla.wfid = requested_wfid
        sla.task = next_stage
        sla.workflow_type = "Product Requisition"
        sla.fire_time = datetime.now()
        sla.expected_difference =  86400.0
        sla.user_identifier = request.GET.get('username')
        sla.status = False

        if next_stage == "Activation Completed":
            sla.completion_time = sla.fire_time
        sla.save()

    role_owner = "Error"

    if next_stage in ["Request to submit Hard Copy Docs for BTRC Approval",
        "BTRC Rejected & Request for Resubmission",
        "BTRC Approval Done & Request for Product Delivery: Sales Order, MR",
        "Activation Request Received & Processing",
    ]:
        role_owner = "KAM"
    else:
        role_owner = "COPC"

    if old_stage is None:
        old_stage = "Drafting Form"

    send_requisition_email(requested_wfid, old_stage, ticket.bs_code, corporate_name, ticket.kam_owner, next_stage, role_owner, ticket.remarks)

    return HttpResponse("")

def __get_onboarding_averages(request):
    data = {}

    tickets = Ticket.objects.filter(WFType="Onboarding")
    bscode_times = []
    gerp_times = []
    lerp_times = []
    va_times = []
    for ticket in tickets:
        row = {}

        row.update({ "WFID": ticket.WFID })
        row.update({ "BS Code": ticket.bs_code })
        row.update({ "Company": ticket.corporate_name })
        row.update({ "KAM": ticket.kam_owner })
        row.update({ "Sub Segment": Onboarding.objects.get(corporate_name=ticket.corporate_name).subsegment })
        slas = SLA.objects.filter()
        for sla in slas:
            if sla.task == "Onboarding Request":
                row.update({ "Onboarding Request": sla.fire_time })
            if sla.task == "BS Code Publish":
                row.update({ "BS Code Publish": sla.fire_time })
            if sla.task == "GERP Code Creation":
                row.update({ "GERP Code Creation": sla.fire_time })
            if sla.task == "LERP Code Creation":
                row.update({ "LERP Code Creation": sla.fire_time })
            if sla.task == "VA Code Creation":
                row.update({ "VA Code Creation": sla.fire_time })
            
        stages = [
            "Onboarding Request",
            "BS Code Publish",
            "GERP Code Creation",
            "LERP Code Creation",
            "VA Code Creation",
        ]

        for stage in stages:
            if stage not in row:
                row.update({ stage: 0 })

        differences = {}
        try:
            time = (row["Onboarding Request"] - row["BS Code Publish"]).total_seconds() / 3600
            differences.update({ "BS Code Publish":  "{0:.2f}".format(time) })
            bscode_times.append(time)
            print(time)
        except:
            # differences.update({ "BS Code Publish": 0 })
            pass

        try:
            time = (row["GERP Code Creation"] - row["BS Code Publish"]).total_seconds() / 3600
            differences.update({ "GERP Code Creation": "{0:.2f}".format(time) })
            gerp_times.append(time)
            print(time)

        except:
            # differences.update({ "GERP Code Creation": 0 })
            pass

        try:
            time = (row["LERP Code Creation"] - row["GERP Code Creation"]).total_seconds() / 3600
            differences.update({ "LERP Code Creation": "{0:.2f}".format(time) })
            lerp_times.append(time)
            print(time)
    
        except:
            # differences.update({ "LERP Code Creation": 0 })
            pass
        
        try:
            time = (row["VA Code Creation"] - row["BS Code Publish"]).total_seconds() / 3600
            differences.update({ "VA Code Creation": "{0:.2f}".format(time) })
            va_times.append(time)
            print(time)

        except:
            # differences.update({ "VA Code Creation": 0 })
            pass

        differences.update({ "WFID": ticket.corporate_name })

    if bscode_times == []:
        bscode_times.append(0.0)
    if gerp_times == []:
        gerp_times.append(0.0)
    if lerp_times == []:
        lerp_times.append(0.0)
    if va_times == []:
        va_times.append(0.0)
        
    data.update({ "BS Code Average": "{0:.2f}".format(mean(bscode_times)) })
    data.update({ "GERP Code Average": "{0:.2f}".format(mean(gerp_times)) })
    data.update({ "LERP Code Average": "{0:.2f}".format(mean(lerp_times)) })
    data.update({ "VA Code Average": "{0:.2f}".format(mean(va_times)) })
        
    # thing = {"data": data}
    # print(thing)
    # print(bscode_times)
    # print(data)
    return JsonResponse(data, safe=False)

def __get_sla(request):
    workflow_id = request.GET.get('wfid')
    # workflow_type = "Onboarding"
    sla = SLA()
    slas = SLA.objects.filter(wfid=workflow_id)
    print(len(slas))
    data = []
    for sla in slas:
        data.append({
            "task": sla.task,
            "fire_time": str(sla.fire_time),
            "completion_time": str(sla.completion_time),
            "status": sla.status
        })
    thing = data
    # print(thing)
    return JsonResponse(thing, safe=False)

def __get_all_sla(request):
    workflow_type = "Onboarding"
    sla = SLA()
    slas = SLA.objects.filter(workflow_type="Onboarding")
    data = []
    for sla in slas:
        data.append({
            "WFID": sla.wfid,
            "Task": sla.task,
            "Fire Time": str(sla.fire_time),
            "Completion Time": str(sla.completion_time),
            "Expected": sla.expected_difference,
            "Actual": str(sla.actual_difference),
            "Status": sla.status,
            "User": sla.user_identifier
        })
    thing = {"data": data}
    # print(thing)
    return JsonResponse(thing, safe=False)


def __get_onboarding_sla(request):
    data = []
    tickets = Ticket.objects.filter(WFType="Onboarding")
    for ticket in tickets:
        workflow_id = ticket.WFID
        row = {}

        row.update({ "WFID": ticket.WFID })
        row.update({ "BS Code": ticket.bs_code })
        row.update({ "Company": ticket.corporate_name })
        row.update({ "KAM": ticket.kam_owner })
        row.update({ "Sub Segment": Onboarding.objects.get(corporate_name=ticket.corporate_name).subsegment })

        slas = SLA.objects.filter(wfid=workflow_id)

        for sla in slas:
            if sla.task == "Onboarding Request":
                row.update({ "Onboarding Request": sla.fire_time.strftime("%d-%b-%Y (%H:%M:%S)") })
            if sla.task == "BS Code Publish":
                row.update({ "BS Code Publish": sla.fire_time.strftime("%d-%b-%Y (%H:%M:%S)") })
            if sla.task == "GERP Code Creation":
                row.update({ "GERP Code Creation": sla.fire_time.strftime("%d-%b-%Y (%H:%M:%S)") })
            if sla.task == "LERP Code Creation":
                row.update({ "LERP Code Creation": sla.fire_time.strftime("%d-%b-%Y (%H:%M:%S)") })
            if sla.task == "VA Code Creation":
                row.update({ "VA Code Creation": sla.fire_time.strftime("%d-%b-%Y (%H:%M:%S)") })
        
        stages = [
            "Onboarding Request",
            "BS Code Publish",
            "GERP Code Creation",
            "LERP Code Creation",
            "VA Code Creation",
        ]

        for stage in stages:
            if stage not in row:
                row.update({ stage: 0 })
        
        if ticket.global_status == "Completed":
            row.update({ "Status": "Completed"})
            row.update({ "Completion Time": "{0:.2f}".format((ticket.last_update_datetime - ticket.first_issued_datetime).total_seconds() / (3600 * 24)) + " days" })
        else:
            row.update({ "Status": "Pending"})
            row.update({ "Completion Time": "N/A" })

        data.append(row)
        
    thing = {"data": data}
    # print(thing)
    return JsonResponse(thing, safe=False)

def __get_pending_tickets_by_days(request):
    data = []
    tickets = Ticket.objects.filter(WFType="Onboarding")
    for ticket in tickets:
        if ticket.global_status == "Pending":
            difference = ticket.last_update_datetime - ticket.first_issued_datetime
            difference_in_days = difference.total_seconds() / (3600 * 24)
            data.append(difference_in_days)

    return JsonResponse(data, safe=False)

def __gerp_sla_days(request):
    data = []
    slas = SLA.objects.filter(workflow_type="Onboarding", task="GERP Code Creation")
    for sla in slas:
        print(sla.wfid)
        ticket = Ticket.objects.get(WFID=sla.wfid, WFType="Onboarding")
        difference = sla.fire_time - ticket.first_issued_datetime
        difference_in_days = difference.total_seconds() / (3600 * 24)
        data.append(difference_in_days)

    return JsonResponse(data, safe=False)

def __lerp_sla_days(request):
    data = []
    slas = SLA.objects.filter(workflow_type="Onboarding", task="LERP Code Creation")
    for sla in slas:
        print(sla.wfid)
        ticket = Ticket.objects.get(WFID=sla.wfid, WFType="Onboarding")
        difference = sla.fire_time - ticket.first_issued_datetime
        difference_in_days = difference.total_seconds() / (3600 * 24)
        data.append(difference_in_days)

    return JsonResponse(data, safe=False)

def __va_sla_days(request):
    data = []
    slas = SLA.objects.filter(workflow_type="Onboarding", task="VA Code Creation")
    for sla in slas:
        print(sla.wfid)
        ticket = Ticket.objects.get(WFID=sla.wfid, WFType="Onboarding")
        difference = sla.fire_time - ticket.first_issued_datetime
        difference_in_days = difference.total_seconds() / (3600 * 24)
        data.append(difference_in_days)

    return JsonResponse(data, safe=False)

def __bscode_sla_days(request):
    data = []
    slas = SLA.objects.filter(workflow_type="Onboarding", task="BS Code Publish")
    for sla in slas:
        print(sla.wfid)
        ticket = Ticket.objects.get(WFID=sla.wfid, WFType="Onboarding")
        difference = sla.fire_time - ticket.first_issued_datetime
        difference_in_days = difference.total_seconds() / (3600 * 24)
        data.append(difference_in_days)

    return JsonResponse(data, safe=False)

def __get_sla_by_stage_by(request):
    data = []
    tickets = Ticket.objects.filter(WFType="Onboarding")
    for ticket in tickets:
        if ticket.global_status == "Pending":
            difference = ticket.last_update_datetime - ticket.first_issued_datetime
            difference_in_days = difference.total_seconds() / (3600 * 24)
            data.append(difference_in_days)

    return JsonResponse(data, safe=False)

def __get_onboarding_sla_diff(request):
    data = []

    tickets = Ticket.objects.filter(WFType="Onboarding")


    for ticket in tickets:
        print(ticket.global_status)
        workflow_id = ticket.WFID
        row = {}

        row.update({ "WFID": ticket.WFID })
        row.update({ "BS Code": ticket.bs_code })
        row.update({ "Company": ticket.corporate_name })
        row.update({ "KAM": ticket.kam_owner })
        row.update({ "Sub Segment": Onboarding.objects.get(corporate_name=ticket.corporate_name).subsegment })
        slas = SLA.objects.filter(wfid=workflow_id)
        for sla in slas:
            if sla.task == "Onboarding Request":
                row.update({ "Onboarding Request": sla.fire_time })
            if sla.task == "BS Code Publish":
                row.update({ "BS Code Publish": sla.fire_time })
            if sla.task == "GERP Code Creation":
                row.update({ "GERP Code Creation": sla.fire_time })
            if sla.task == "LERP Code Creation":
                row.update({ "LERP Code Creation": sla.fire_time })
            if sla.task == "VA Code Creation":
                row.update({ "VA Code Creation": sla.fire_time })
            
        stages = [
            "Onboarding Request",
            "BS Code Publish",
            "GERP Code Creation",
            "LERP Code Creation",
            "VA Code Creation",
        ]

        for stage in stages:
            if stage not in row:
                row.update({ stage: 0 })

        differences = {}
        try:
            differences.update({ "BS Code Publish": "{0:.2f}".format((row["Onboarding Request"] - row["BS Code Publish"]).total_seconds()) })
        except:
            differences.update({ "BS Code Publish": 0 })
            pass

        try:
            differences.update({ "GERP Code Creation": "{0:.2f}".format((row["GERP Code Creation"] - row["BS Code Publish"]).total_seconds()) })
        except:
            differences.update({ "GERP Code Creation": 0 })
            pass

        try:
            differences.update({ "LERP Code Creation": "{0:.2f}".format((row["LERP Code Creation"] - row["GERP Code Creation"]).total_seconds()) })
        except:
            differences.update({ "LERP Code Creation": 0 })
            pass
        
        try:
            differences.update({ "VA Code Creation": "{0:.2f}".format((row["VA Code Creation"] - row["BS Code Publish"]).total_seconds()) })
        except:
            differences.update({ "VA Code Creation": 0 })
            pass
        differences.update({ "WFID": ticket.corporate_name })
        data.append(differences)   
            
        
    thing = {"data": data}
    # print(thing)
    return JsonResponse(thing, safe=False)




def __get_all_items(request):
    items = Item.objects.all()
    data = []
    for item in items:
        data.append({
            "code": item.item_code,
            "description": item.description,
            "type": item.item_type,

        })
    # print(data)
    return JsonResponse(data, safe=False)



def onboarding_cu(request):

    '''
        Creates or updates an onboarding model based on the corporate name.
        Must come from the onboarding form as the request is sent.
    '''
    corp = request.POST.get('corporate_name')
    corporate_name = request.POST.get('corporate_name')

    onboarding = Onboarding()
    if (Onboarding.objects.filter(corporate_name=corp).exists()):
        onboarding = Onboarding.objects.get(corporate_name=corp)
    else:
        onboarding.corporate_name = request.POST.get('corporate_name')

    onboarding.corporate_short_name = request.POST.get('corporate_short_name')
    onboarding.bscode = request.POST.get('bs_code')
    onboarding.subsegment = request.POST.get('sub_segment')
    onboarding.zone = request.POST.get('zone')
    onboarding.parent_bscode = request.POST.get('parent_bs_code')
    onboarding.corporate_type = request.POST.get('corporate_type')
    onboarding.kam_name = request.POST.get('kam_name')
    onboarding.bs_customer_region = request.POST.get('bs_customer_region')
    onboarding.address1 = request.POST.get('address_1')
    onboarding.address2 = request.POST.get('address_2')
    onboarding.district = request.POST.get('district')
    onboarding.thana = request.POST.get('thana')
    onboarding.city = request.POST.get('city')
    onboarding.zip_code = request.POST.get('zip_code')
    onboarding.gerp_address = request.POST.get('gerp_address')
    onboarding.rate = request.POST.get('rate_plan')
    onboarding.cug_id = request.POST.get('cug_id')
    onboarding.pulse = request.POST.get('pulse')
    onboarding.cug_pulse = request.POST.get('cug_pulse')
    onboarding.vat_waiver_flag = request.POST.get('vat_waiver_flag')
    onboarding.bill_cycle = request.POST.get('bill_cycle')
    onboarding.erp_company_code = request.POST.get('erp_company_code')


    onboarding.kcp_first_name = request.POST.get('bio_kcp_first_name')
    onboarding.kcp_last_name = request.POST.get('bio_kcp_last_name')
    onboarding.kcp_contact_number = request.POST.get('bio_kcp_contact_number')
    onboarding.kcp_email_1 = request.POST.get('kcp_email_1')
    onboarding.kcp_email_2 = request.POST.get('kcp_email_2')
    onboarding.kcp_email_3 = request.POST.get('kcp_email_3')
    onboarding.kcp_nid = request.POST.get('bio_kcp_nid')
    onboarding.kcp_nid = request.POST.get('bio_kcp_nid')

    if request.POST.get('bio_kcp_dob') is not "":
        onboarding.kcp_dob = request.POST.get('bio_kcp_dob')

    if request.method == 'POST' and 'work_order_application' in request.FILES:
        wo_file = request.FILES['work_order_application']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/wo/' + corporate_name + '_' + wo_file.name, wo_file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        onboarding.wo_ca_attach = uploaded_file_url

    if request.method == 'POST' and 'btrc_form_20191000' in request.FILES:
        btrc_20191000 = request.FILES['btrc_form_20191000']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/btrc_form_20191000/' + corporate_name + '_' + btrc_20191000.name, btrc_20191000)
        uploaded_file_url = fs.url(filename)
        onboarding.btrc_form_1000 = uploaded_file_url
    
    if request.method == 'POST' and 'btrc_form_20191001' in request.FILES:
        btrc_20191001 = request.FILES['btrc_form_20191001']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/btrc_form_20191001/' + corporate_name + '_' + btrc_20191001.name, btrc_20191001)
        uploaded_file_url = fs.url(filename)
        onboarding.btrc_form = uploaded_file_url

    if request.method == 'POST' and 'btrc_form_20191002' in request.FILES:
        btrc_20191002 = request.FILES['btrc_form_20191002']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/btrc_form_20191002/' + corporate_name + '_' + btrc_20191002.name, btrc_20191002)
        uploaded_file_url = fs.url(filename)
        onboarding.btrc_form_2 = uploaded_file_url

    if request.method == 'POST' and 'poc_id' in request.FILES:
        poc_identity = request.FILES['poc_id']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/poc_identity/' + corporate_name + '_' + poc_identity.name, poc_identity)
        uploaded_file_url = fs.url(filename)
        onboarding.proof_of_company_id = uploaded_file_url

    if request.method == 'POST' and 'nid_kcp' in request.FILES:
        nid_kcp = request.FILES['nid_kcp']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/nid_kcp/' + corporate_name + '_' + nid_kcp.name, nid_kcp)
        uploaded_file_url = fs.url(filename)
        onboarding.nid_authorized = uploaded_file_url

    if request.method == 'POST' and 'poc_billing_address' in request.FILES:
        poc_billing = request.FILES['poc_billing_address']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/poc_billing_address/' + corporate_name + '_' + poc_billing.name, poc_billing)
        uploaded_file_url = fs.url(filename)
        onboarding.proof_of_company_billing_address = uploaded_file_url

    if request.method == 'POST' and 'agreement_copy' in request.FILES:
        agreement_copy = request.FILES['agreement_copy']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/agreement_copy/' + corporate_name + '_' + agreement_copy.name, agreement_copy)
        uploaded_file_url = fs.url(filename)
        onboarding.agreement_copy = uploaded_file_url
    
    if request.method == 'POST' and 'approved_ams' in request.FILES:
        approved_ams = request.FILES['approved_ams']
        fs = FileSystemStorage()
        filename = fs.save(corporate_name + '/approved_ams/' + corporate_name + '_' + approved_ams.name, approved_ams)
        uploaded_file_url = fs.url(filename)
        onboarding.approved_ams = uploaded_file_url

    onboarding.save()

    return


def get_mail_text(role, wftype, requested_wfid, kam_owner, old_stage, bscode, company):
    text = ""
    if role == "KAM":
        text = '''
        Your request for customer onboarding (system integration) has been submitted successfully.
        Company Name: %s
        KAM Owner: %s
        ''' % (company, kam_owner)
    elif role == "COPC":
        text = '''
        BS Code has been created successfully for the below request:
        Company Name: %s
        BS Code: %s
        KAM Owner: %s
        ''' % (company, bscode, kam_owner)
    elif role == "VA":
        text = '''
        VA Code has been created successfully for the below request:
        Company Name: %s
        BS Code: %s
        KAM Owner: %s
        ''' % (company, bscode, kam_owner)
    elif role == "LERP":
        text = '''
        ERP Code has been created successfully for the below request:
        Company Name: %s
        BS Code: %s
        ERP Code: BD%s
        KAM Owner: %s
        ''' % (company, bscode, Onboarding.objects.get(corporate_name=company).erp_code, kam_owner)
    return text