from django.shortcuts import render, redirect
from django.views import View
from App.models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from App.email import send_otp_email
from datetime import date
from App.form import *
import pandas as pd
from django.contrib.auth import authenticate, login , logout




class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("Admin:dashboard")
        return render(request,"login.html")

    def post(self, request):
        print(" iam working")
        user = authenticate(email=request.POST.get("email"),password=request.POST.get("password"))
        if user is not None:
            login(request,user)
            return redirect("Admin:email-management")
        else:
            return redirect("Admin:login")
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("Admin:login")


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
        
            notify_obj = NotifyModal.objects.all().order_by("-id")
            thirty_days = date.today() + timedelta(days=30)
            print(thirty_days)
            
            recent_objects = []
            older_objects = []

            for obj in notify_obj:
                if isinstance(obj.expires, str):
                    try:
                        obj.expires = datetime.strptime(obj.expires, '%Y-%m-%d').date()
                    except ValueError:
                        obj.expires = None  
                    
                if obj.expires and obj.expires <= thirty_days:
                    recent_objects.append(obj)
                else:
                    older_objects.append(obj)

            sorted_notify_obj = recent_objects + older_objects

            return render(request, "user-management.html", {"notify_obj": sorted_notify_obj, "today": thirty_days})
        return redirect("Admin:login")
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)
            
            for index, row in df.iterrows():
                NotifyModal.objects.create(
                    domain_name=row['Domain Name'],
                    server_ip=row['Server IP'],
                    associated_account=row['Associated Account'],
                    customer_id=row['Customer ID'],
                    domain_account=row['Domain - Account'],
                    ssl_status=row['SSL Status'],
                    hosted_account=row['Hosted Account'],
                    remark=row['Remark'],
                    expires=row['Expires']
                )
        return redirect("Admin:dashboard")
    

class AddInformationView(View):
    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect("Admin:dashboard")
        return render(request, "add-user.html")
    
    def post(self, request):
        data = request.POST
        print("data",data)
        notify_obj = NotifyModal.objects.create(
            domain_name=request.POST.get("domain_name"),
            server_ip=request.POST.get("server_ip"),
            associated_account=request.POST.get("associated_account"),
            customer_id=request.POST.get("customer_id"),
            domain_account=request.POST.get("domain_account"),
            ssl_status=request.POST.get("ssl_status"),
            hosted_account=request.POST.get("hosted_account"),
            remark=request.POST.get("remark"),
            expires=request.POST.get("expires"))
        return redirect("Admin:dashboard")
    

class DeleteUser(View):
    def get(self, request, id):
        obj = get_object_or_404(NotifyModal, id=id)
        obj.delete()
        return redirect("Admin:dashboard")
    

class EditNotifyView(View):
    def get(self, request,id):
        try:
            edit_obj = NotifyModal.objects.get(id=id)
            data = {
                "domain_name": edit_obj.domain_name,
                "server_ip": edit_obj.server_ip,
                "associated_account": edit_obj.associated_account,
                "customer_id": edit_obj.customer_id,
                "domain_account": edit_obj.domain_account,
                "ssl_status": edit_obj.ssl_status,
                "hosted_account": edit_obj.hosted_account,
                "remark": edit_obj.remark,
                "expires": edit_obj.expires,
            }
        except NotifyModal.DoesNotExist:
            data = None
        return render(request, "edit-notify.html",{"data":data})

    def post(self, request, id):
        try:
            edit_obj = NotifyModal.objects.get(id=id)
            edit_obj.domain_name = request.POST.get("domain_name")
            edit_obj.server_ip = request.POST.get("server_ip")
            edit_obj.associated_account = request.POST.get("associated_account")
            edit_obj.customer_id = request.POST.get("customer_id")
            edit_obj.domain_account = request.POST.get("domain_account")
            edit_obj.ssl_status = request.POST.get("ssl_status")
            edit_obj.hosted_account = request.POST.get("hosted_account")
            edit_obj.remark = request.POST.get("remark")
            
            expires_str = request.POST.get("expires")
            if expires_str:
                try:
                    edit_obj.expires = datetime.strptime(expires_str, '%Y-%m-%d').date()
                except ValueError:
                    edit_obj.expires = None  
            else:
                edit_obj.expires = None
            
            edit_obj.save()
            return redirect("Admin:dashboard")  
        except NotifyModal.DoesNotExist:
            return redirect("Admin:edit-notify")
    


class CronJobAPI(APIView):
    def get(self, request):
        alert_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        print(alert_date)
        alert_hit = NotifyModal.objects.filter(expires=alert_date)
        if alert_hit:
            for alert in alert_hit:
                send_otp_email(
                    email="harish@tranktechies.com",
                    domain_name=alert.domain_name,
                    server_ip=alert.server_ip,
                    associated_account=alert.associated_account,
                    customer_id=alert.customer_id,
                    domain_account=alert.domain_account,
                    ssl_status=alert.ssl_status,
                    hosted_account=alert.hosted_account,
                    remark=alert.remark,
                    expires=alert.expires
                )
            return Response({"status": status.HTTP_200_OK, "message": "CronJob created successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": "data not found."}, status=status.HTTP_200_OK)



class EmailView(View):
    def get(self, request):
        return render(request, "email-management.html",{"email_data":EmployeeModal.objects.all()})
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)
            
            for index, row in df.iterrows():
                EmployeeModal.objects.create(
                    emp_name=row['Employee Name'],
                    email_address=row['Email Address'],
                    expires=row["expires"],
                    password=row['Password'])
        return redirect("Admin:email-management")
    

class AddEmailView(View):
    def get(self, request):
        return render(request, "add-email.html")
    
    def post(self, request):
        emp_obj = EmployeeModal.objects.create(
            emp_name=request.POST.get("emp_name"),
            email_address=request.POST.get("email_address"),
            expires=request.POST.get("expires"),
            password=request.POST.get("password")
            )
        return redirect("Admin:email-management")
    


class EditEmailView(View):
    def get(self, request, id):
        edit_obj = EmployeeModal.objects.get(id=id) 
        return render(request, "edit-email.html",{"edit_obj": edit_obj})
    
    def post(self, request,id):
        print(request.POST.get("status") == "True")
        data = request.POST
        data = EmployeeModal.objects.get(id=id)
        data.emp_name=request.POST.get("emp_name")
        data.email_address=request.POST.get("email_address")
        data.expires=request.POST.get("expires")
        data.password=request.POST.get("password")
        data.save()
        return redirect("Admin:email-management")
        

class DeleteEmailView(View):
    def get(self, request, id):
        obj = get_object_or_404(EmployeeModal, id=id)
        obj.delete()
        return redirect("Admin:email-management") 
    

