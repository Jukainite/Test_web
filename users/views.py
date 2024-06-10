from django.shortcuts import render, redirect
from user_management import settings 
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm,QRForm
from functions.so import* 
from functions.QR import* 
from functions.sinh_trac_hoc import*
from functions.nhan_tuong_hoc import*
from functions.supa_data import* 
from functions.tinh_tien import* 
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
import os
from supabase import create_client, Client
import base64
import face_recognition
from io import BytesIO
import json
from users.forms import FingerImageForm,FaceImageForm,UpgradeForm
from users.models import qr_image
# from .models import UploadImage  
url="https://zilpepysnqvfkpylfumn.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppbHBlcHlzbnF2ZmtweWxmdW1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwNjA2NzAsImV4cCI6MjAzMjYzNjY3MH0.yhOVyH2Ulk2Uhnulyu8FxkKS5zYfqgy1W_vRIGkQ300"
supabase = create_client(url, key)



def home(request):
    if request.user.is_authenticated:
        name = request.user.username
        # data=get_data(name)
        rows = supabase.table("feature").select("*").eq( "username",name).execute()

        for row in rows.data:
            data = {
                    'thansohoc': row['thansohoc'],
                    'sinhtrachoc': row['sinhtrachoc'],
                    'nhantuonghoc': row['nhantuonghoc'],
            }
        return render(request, 'users/home.html',data)
    else:
        return render(request, 'users/home.html')
def numerology_result(request):
    return render(request, 'users/numerology_result.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # Chuyển hướng tới trang chủ nếu người dùng đã đăng nhập
        if request.user.is_authenticated:
            return redirect(to='/')

        # Nếu không, xử lý dispatch như bình thường
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

class GuestLoginView(View):
    def get(self, request, *args, **kwargs):
        guest_user = authenticate(username='Guest', password='Wieh6IekJXrQCZGETD2Y4087pqYis1ysYRZ1I6Kn8vv0OV00r6')  # Thay thế mật khẩu bằng mật khẩu thực tế
        if guest_user is not None:
            login(request, guest_user)
            return redirect('users-home')  # Chuyển hướng tới trang chủ hoặc bất kỳ đâu
        else:
            messages.error(request, 'Unable to login as guest')
            return redirect('login')
def read_file_content(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()       


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

def calculate_numerology(request):
        name = request.user.username
        # data=get_data(name)
        rows = supabase.table("feature").select("*").eq( "username",name).execute()

        # Assert we pulled real data.
        assert len(rows.data) > 0
        for row in rows.data:
            data = {
                    'Thần số học': row['thansohoc'],
                    'Sinh trắc học': row['sinhtrachoc'],
                    'Nhân tướng học': row['nhantuonghoc'],
            }
        ngay = request.GET.get('ngay')
        thang = request.GET.get('thang')
        nam = request.GET.get('nam')
        ten = request.GET.get('ten')

        
            
        # Thực hiện tính toán các số thần số học ở đây
        # so_chu_dao_result = so_chu_dao(f"{ngay}/{thang}/{nam}")
        # so_linh_hon_result = so_linh_hon(ten)
        # so_su_menh_result = so_su_menh(ten)

        if not ngay or not thang or not nam or not ten:
            return render(request, 'numerology_form.html', {'error': 'Vui lòng nhập đầy đủ thông tin'})
        
        sochudao = {
            "filename": None,
            'result':None,
            "content": None
        }

        sosumenh = {
            "filename": None,
            'result':None,
            "content": None
        }

        solinhhon = {
            "filename": None,
            'result':None,
            "content": None
        }

        def format_date(day, month, year):
            formatted_day = str(day).zfill(2)
            formatted_month = str(month).zfill(2)
            formatted_year = str(year)
            return f"{formatted_day}/{formatted_month}/{formatted_year}"
        
        sochudao['result'] = so_chu_dao(format_date(ngay, thang, nam))
        solinhhon['result'] = so_linh_hon(ten)
        sosumenh['result'] = so_su_menh(ten)

        status = None
        if data['Thần số học'] > 0: 
            status="Vip"
            sochudao['filename']= f"data/thansohoc_vip/sochudao/{sochudao['result']}.txt"
            solinhhon['filename']= f"data/thansohoc_vip/solinhhon/{solinhhon['result']}.txt"
            sosumenh['filename']= f"data/thansohoc_vip/sosumenh/{sosumenh['result']}.txt"
            # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
            new_vip_count = data['Thần số học'] - 1
            supabase.table("feature").update({"thansohoc": new_vip_count}).eq("username", name).execute()
    
        else:
            status='Non-Vip'
            sochudao['filename']= f"data/thansohoc_nor/sochudao/{sochudao['result']}.txt"
            solinhhon['filename']= f"data/thansohoc_nor/solinhhon/{solinhhon['result']}.txt"
            sosumenh['filename']= f"data/thansohoc_nor/sosumenh/{sosumenh['result']}.txt"

        sochudao["content"] = read_file_content(sochudao["filename"]).replace('\n', '<br>') 
        solinhhon["content"] = read_file_content(solinhhon["filename"]).replace('\n', '<br>') 
        sosumenh["content"] = read_file_content(sosumenh["filename"]).replace('\n', '<br>')     


        context = {
            'so_chu_dao_result': sochudao['result'],
            'so_linh_hon_result':solinhhon['result'],
            'so_su_menh_result': sosumenh['result'],
            'so_chu_dao_cotent':sochudao["content"] ,
            'so_linh_hon_content':solinhhon["content"],
            'so_su_menh_cotent': sosumenh["content"],
            'status':status,
        }
        
        return render(request, 'users/numerology_result.html', context)

def sinhtrachoc_result(request):
    pass


def thansohoc(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    context = {
        'username':name,
        'data': data['Thần số học'],
        
    }
    return render(request, 'users/thansohoc.html',context)     

def sinhtrachoc(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    sinhtrachoc = {
            "filename": None,
            'result':None,
            "content": None
        }
    # return render(request, 'users/sinhtrachoc.html',context)
    def delete_files_in_folder(folder_path):
        # num_files = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
        num_files = len(files)
        if num_files > 100:
            files_to_delete = files[:50]  # Chọn 50 tệp đầu tiên để xóa
            for filename in files_to_delete:
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            counter = num_files
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                new_filename = f'DSPfinger{counter}{os.path.splitext(filename)[1]}'  # Giữ nguyên phần mở rộng của tệp
                new_file_path = os.path.join(folder_path, new_filename)
                try:
                    os.rename(file_path, new_file_path)
                    counter += 1
                except Exception as e:
                    print(f'Failed to rename {file_path} to {new_file_path}. Reason: {e}')
    if request.method == 'POST':  
        form = FingerImageForm(request.POST, request.FILES)  
        if form.is_valid(): 
            upload_folder = os.path.join(settings.MEDIA_ROOT, 'finger_images')  # Thay 'path_to_upload_folder' bằng đường dẫn thực tế
            delete_files_in_folder(upload_folder)
            form.save()  

            # Getting the current instance object to display in the template  
            img_object = form.instance  

            image_path = img_object.image.path
            img= Image.open(image_path)
            sinhtrachoc['result'] = predict_label(img)

            status = None
            if data['Sinh trắc học'] > 0: 
                status="Vip"
                sinhtrachoc['filename']= f"data/sinhtrachoc_vip/{sinhtrachoc['result']}.txt"
                # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
                sinhtrachoc["content"] = read_file_content(sinhtrachoc["filename"]).replace('\n', '<br>') 
                new_vip_count = data['Sinh trắc học'] - 1
                supabase.table("feature").update({"sinhtrachoc": new_vip_count}).eq("username", name).execute()
        
            else:
                status='Non-Vip'
                sinhtrachoc['filename']= f"data/sinhtrachoc_nor/{sinhtrachoc['result']}.txt"
                sinhtrachoc["content"] = read_file_content(sinhtrachoc["filename"]).replace('\n', '<br>') 


            context = {
                'form': form,
                'img_obj': img_object,
                'biometric_info': sinhtrachoc['result'],
                'status':status,
                'result':sinhtrachoc['result'],
                'content':sinhtrachoc['content'],
                
            }
            return render(request, 'users/sinhtrachoc_result.html', context)  
    else:  
        form = FingerImageForm()  
    context = {
        'username':name,
        'data': data['Sinh trắc học'],
        'form': form
    }
    return render(request, 'users/sinhtrachoc.html', context)  
           
def nhantuonghoc_image(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    nhantuonghoc = {
            "filename": None,
            'result':None,
            "content": None
        }
   
    def delete_files_in_folder(folder_path):
        # num_files = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
        num_files = len(files)
        if num_files > 100:
            files_to_delete = files[:50]  # Chọn 50 tệp đầu tiên để xóa
            for filename in files_to_delete:
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            counter = num_files
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                new_filename = f'DSPface{counter}{os.path.splitext(filename)[1]}'  # Giữ nguyên phần mở rộng của tệp
                new_file_path = os.path.join(folder_path, new_filename)
                try:
                    os.rename(file_path, new_file_path)
                    counter += 1
                except Exception as e:
                    print(f'Failed to rename {file_path} to {new_file_path}. Reason: {e}')
    if request.method == 'POST':  
        form = FaceImageForm(request.POST, request.FILES)  
        if form.is_valid(): 
            upload_folder = os.path.join(settings.MEDIA_ROOT, 'face_images')  # Thay 'path_to_upload_folder' bằng đường dẫn thực tế
            try:
                delete_files_in_folder(upload_folder)
            except: pass
            form.save()  

            # Getting the current instance object to display in the template  
            img_object = form.instance  

            image_path = img_object.image.path
            img= Image.open(image_path)
            # nhantuonghoc['result'] = predict_from_image(img)
            image_np = np.array(img)
            face_locations = face_recognition.face_locations(image_np)
            if face_locations:
                top, right, bottom, left = face_locations[0]
                face_image_np = image_np[top:bottom, left:right]
                nhantuonghoc['result'] = predict_from_face_image(face_image_np)
                status = None
                if data['Nhân tướng học'] > 0: 
                    status="Vip"
                    nhantuonghoc['filename']= f"data/nhantuonghoc_vip/{nhantuonghoc['result']}.txt"
                    # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
                   
                    nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
                    
                    new_vip_count = data['Nhân tướng học'] - 1
                    supabase.table("feature").update({"nhantuonghoc": new_vip_count}).eq("username", name).execute()
            
                else:
                    status='Non-Vip'
                    nhantuonghoc['filename']= f"data/nhantuonghoc_nor/{nhantuonghoc['result']}.txt"
                    
                    nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
            else:
                nhantuonghoc["content"]='Không phát hiện thấy khuôn mặt nào trong ảnh. Đảm bảo khuôn mặt của bạn được nhìn thấy trong ảnh! Nếu có thể, mời bạn thử lại với ảnh khác'
                return render(request, 'users/nhantuonghoc_result.html', context) 

            context = {
                'form': form,
                'img_obj': img_object,
                'biometric_info': nhantuonghoc['result'],
                'status':status,
                'result':nhantuonghoc['result'],
                'content':nhantuonghoc['content'],
                
            }
            return render(request, 'users/nhantuonghoc_result.html', context)  
            # nhantuonghoc_result(request,context)
    else:  
        form = FingerImageForm()  
    context = {
        'username':name,
        'data': data['Nhân tướng học'],
        'form': form
    }
    return render(request, 'users/nhantuonghoc_image.html',context) 
face_content={}
status_face=False
def nhantuonghoc_video(request):
    name = request.user.username
        # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    nhantuonghoc = {
            "filename": None,
            'result':None,
            "content": None
        }
    if request.method == 'POST':
        
        # face_content={}
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        # Decode base64 string to bytes
        decoded_data = base64.b64decode(str_img)

        # Create PIL image from bytes
        pil_image = Image.open(BytesIO(decoded_data))
        image_np = np.array(pil_image)
        face_locations = face_recognition.face_locations(image_np)
        if face_locations:
            top, right, bottom, left = face_locations[0]
            face_image_np = image_np[top:bottom, left:right]
            nhantuonghoc['result'] = predict_from_face_image(face_image_np)
            status = None
            if data['Nhân tướng học'] > 0: 
                status="Vip"
                nhantuonghoc['filename']= f"data/nhantuonghoc_vip/{nhantuonghoc['result']}.txt"
                # Trừ đi 1 lượt VIP và cập nhật cơ sở dữ liệu
                
                nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
                
                new_vip_count = data['Nhân tướng học'] - 1
                supabase.table("feature").update({"nhantuonghoc": new_vip_count}).eq("username", name).execute()
        
            else:
                status='Non-Vip'
                nhantuonghoc['filename']= f"data/nhantuonghoc_nor/{nhantuonghoc['result']}.txt"
                
                nhantuonghoc["content"] = read_file_content(nhantuonghoc["filename"]).replace('\n', '<br>') 
                

            content = {

                'biometric_info': nhantuonghoc['result'],
                'status':status,
                'result':nhantuonghoc['result'],
                'content':nhantuonghoc['content'],
                
            }
            request.session['content'] = content
            return JsonResponse({'success': True, 'redirect_url': reverse('videoresult')})
       
        
       
    else:

        return render(request, 'users/nhantuonghoc_video.html')
 
def intro_video(request):
    name = request.user.username
    # data=get_data(name)
    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    content={
        "username": name,
        "data": data['Nhân tướng học']
    }
    return render(request, 'users/intro_video.html',content)     


def change_QR(qr):
    buffer_png = BytesIO()
    qr.save(buffer_png, kind='PNG')
    return base64.b64encode(buffer_png.getvalue()).decode('utf-8')

def nhantuonghoc_result(request):
    pass

def predict_shape(request):
    pass

def video_result(request):
    global face_content
    content = request.session.get('content')
    print(content)
    return render(request, 'users/video_result.html', content)

def hoadon(request):
    return render(request, 'users/hoadon.html')

def nangcap(request):
    form = UpgradeForm(request.POST)
    
    context ={
        'error' :''
    } 
    context['form']= form 
    if request.GET: 
        temp = {}
        temp['Thần số học']= request.GET['thansohoc'] 
        temp['Nhân tướng học']= request.GET['nhantuonghoc'] 
        temp['Sinh trắc học']= request.GET['sinhtrachoc'] 
        
        if (temp['Thần số học']== '0') and (temp['Sinh trắc học']== '0') and (temp['Nhân tướng học']== '0'):
            context['error']= 'Không thể tiến hành thanh toán khi cả ba lựa chọn đều là 0. Vui lòng chọn lại!'
         
            return render(request,'users/nangcap.html',context)
        def change_QR(qr):
            buffer_png = BytesIO()
            qr.save(buffer_png, kind='PNG')
            return base64.b64encode(buffer_png.getvalue()).decode('utf-8')
        thansohoc = int(temp['Thần số học'])
        nhantuonghoc = int(temp['Nhân tướng học']) 
        sinhtrachoc = int(temp['Sinh trắc học'])
        tong_tien= tinh_tien(thansohoc,nhantuonghoc,sinhtrachoc)
        username = request.user.username

        # Lấy bill_id cuối cùng và tăng lên 1
        response = supabase.table('bills').select('bill_id').order('bill_id', desc=True).limit(1).execute()
        if response.data:
            last_bill_id = response.data[0]['bill_id']
            last_number = int(last_bill_id[3:])
            new_number = last_number + 1
            new_bill_id = f'DSP{new_number:010d}'
        else:
            new_bill_id = 'DSP0000000001'
        
        qr= QR(new_bill_id,tong_tien )
        # temp_path=os.path.join(settings.MEDIA_ROOT, f'QR_images/{new_bill_id}.png')
        
        
        # image_path = img_object.image.path
        new_bill = {
            'bill_id': new_bill_id,
            'username': username,
            'thansohoc': thansohoc,
            'nhantuonghoc': nhantuonghoc,
            'sinhtrachoc': sinhtrachoc,
            'total':tong_tien,
            'approved': False,
            
        }
        supabase.table('bills').insert(new_bill).execute()
        new_bill = {
            'bill_id': new_bill_id,
            'username': username,
            'thansohoc': thansohoc,
            'nhantuonghoc': nhantuonghoc,
            'sinhtrachoc': sinhtrachoc,
            'total':tong_tien,
            'approved': False,
            'img_str': change_QR(qr),
        }
        # new_bill['img_str']= change_QR(qr),
       

        return render(request,'users/thanhtoanhoadon.html',new_bill)
    return render(request, 'users/nangcap.html',context)

def thanhtoanhoadon(request,new_bill):
    return render(request,'users/thanhtoanhoadon.html',new_bill)

def lichsumua(request):
    username = request.user.username
    response = supabase.table('bills').select('*').eq('username', username).execute()
    bills = response.data
    
    return render(request,'users/lichsumua.html', {'bills': bills})

def hoadon(request, bill_id):
    username = request.user.username
    response = supabase.table('bills').select('*').eq('bill_id', bill_id).eq('username', username).execute()
    bills = response.data
    bill=bills[0]
    print(bill)
    qr= QR(bill_id, bill['total'] )
    new_bill = {
            'bill_id': bill_id,
            'username': username,
            'thansohoc': bill['thansohoc'],
            'nhantuonghoc': bill['nhantuonghoc'],
            'sinhtrachoc': bill['sinhtrachoc'],
            'total':bill['total'],
            'approved': bill['approved'],
            'img_str': change_QR(qr),
        }
    # if not bills:
    #     return redirect('bill_list')
    
    return render(request,'users/hoadon.html',new_bill)

def approvehoadon(request):
    # Lấy tất cả các hoá đơn từ Supabase
    response = supabase.table('bills').select('*').execute()
    bills = response.data
    
    if request.method == 'POST':
        # Xử lý duyệt hoá đơn
        approved_bills = request.POST.getlist('approve')
        for bill_id in approved_bills:
            supabase.table('bills').update({'approved': True}).eq('bill_id', bill_id).execute()
            return redirect('approvehoadon')
    return render(request,'users/approvehoadon.html', {'bills': bills})