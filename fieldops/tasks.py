from celery.decorators import periodic_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

from fieldops.models import Visit
from WorkflowTool.models import GPUser

@periodic_task(
    run_every=(crontab()),
    name="send_emails_to_kams",
    ignore_result=True
)
def send_emails_to_kams():
    for user in GPUser.objects.filter(role="KAM"):
    # for user in GPUser.objects.filter(phone_number="saqibur"):
        user_id = str(user.phone_number)

        html = """
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Visit-Tracker Table</title>
        <style type="text/css" media="screen">
            table{
                empty-cells:hide;
                background-color: white;
            }
        </style>
        </head>
        <html><body>
        <table border="1">
        <tr>
            <td>Ref #</td>
            <td>Company Name</td>
            <td>Visit Type</td>
            <td>Visit Date</td>
            <td>Last Updated</td>
        </tr>
        """

        visit_counter = 0
        for visit in Visit.objects.filter(kam_id=user_id, visited=False):
            visit_counter += 1
            html += """
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
            """ % (str(visit.visit_id), str(visit.company_name), str(visit.visit_type), str(visit.date_of_visit), str(visit.last_updated))
        

        html += """
        </table>
        <p>Regards,</p>
        <p>Workflow<sup class="font-weight-light">Lite</sup></p>
        </body></html>"""

        if visit_counter == 0:
            html = """
                <h3>You have no pending visits.</h3>
                <p>Regards,</p>
                <p>Workflow<sup class="font-weight-light">Lite</sup></p>
            """

        message = MIMEMultipart(
            "alternative", None, [MIMEText(html, 'html')])
        me = open('.me').readline()
        password = open('.password').readline()
        server = open('.mailserver').readline()
        message['Subject'] = "Visit-Tracker: Your Pending Visits for today"
        message['From'] = me
        message['To'] = user_id + '@grameenphone.com'
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