import smtplib

from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.

#ADMIN
from myapp.models import *


def login_get(request):
    return render(request, "login.html")


def forgot_password_get(request):
    return render(request, "forgot.html")

def forgot_password_post(request):
    email=request.POST['email']
    if User.objects.filter(username=email):
        import random
        temp=random.randint(0000,9999)
        user=User.objects.get(username=email)
        user.set_password(str(temp))
        user.save()

        subject='Course Companion – Password Recovery'
        messages=f"We received a request to reset the password for your Course Companion account.Password:{str(temp)}"
        from_email='coursecompanion05@gmail.com'
        recipient_list=[email]
        send_mail(subject,messages,from_email,recipient_list)
    return redirect('/myapp/login/')



def login_out(request):
    logout(request)
    return render(request, "login.html")


def check(request):

    print(request.user)

    try:
        id=int(request.user.id)

        print("yes")
        return JsonResponse(
            {
                'status':'ok'
            }
        )
    except Exception as a:

        print("no")
        return JsonResponse(
            {
                'status':'no'
            }
        )

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    log= authenticate(request, username=username, password=password)
    if log is not None:
        login(request, log)
        if log.groups.filter(name='admin'):
            return redirect('/myapp/admin_home/')
        elif log.groups.filter(name='course_provider'):
            if Cp.objects.filter(USER_id=request.user.id,status='approved').exists():
                print("lllllllllllllllllll")
                print(request.user.id)
                return redirect('/myapp/cp_home/')
            else:
                messages.warning(request, 'invalid user')
                return redirect('/myapp/login/')
        else:
            messages.warning(request, 'invalid user')
            return redirect('/myapp/login/')
    else:
         messages.warning(request, 'user not found')
         return redirect('/myapp/login/')

@login_required(login_url='/myapp/login/')
def admin_home(request):
    return render(request, "admin/admin_home.html")

def cp_signup(request):
    return render(request, "cp/signup.html")

def cp_signup_post(request):
    fullname= request.POST['fullname']
    email= request.POST['email']
    phoneno= request.POST['phoneno']
    place = request.POST['place']
    post = request.POST['post']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    description = request.POST['description']

    if User.objects.filter(username=email).exists():
        messages.warning(request,"Email is already exist!")
        return redirect('/myapp/cp_signup/')

    proof = request.FILES['proof']

    fs= FileSystemStorage()
    from datetime import datetime
    date = datetime.now().strftime("%y%M%d-%H%M%S")+"1.jpg"
    fs.save(date,proof)
    path= fs.url(date)


    photo = request.FILES['photo']

    fs1 = FileSystemStorage()
    from datetime import datetime
    date1 = datetime.now().strftime("%y%M%d-%H%M%S") + "-1.jpg"
    fs1.save(date1,photo)
    path1 = fs1.url(date1)



    password = request.POST['password']
    confirmpassword = request.POST['confirmpassword']



    if password == confirmpassword:
        cp=User.objects.create_user(username=email, password=password)
        cp.groups.add(Group.objects.get(name="course_provider"))
        cp.save()
        data=Cp()
        data.name=fullname
        data.phone = phoneno
        data.email=email
        data.place=place
        data.post=post
        data.pin=pincode
        data.district=district
        data.state = state
        data.description = description
        data.proof=path
        data.photo= path1
        data.status='pending'
        data.USER=cp
        data.save  ()
        messages.warning(request, 'Sign up succefull')
        return redirect('/myapp/login/')
    else:
        messages.warning(request, 'Password does not match')
        return redirect('/myapp/cp_signup/')



@login_required(login_url='/myapp/login/')
def admin_view_cp(request):
    data=Cp.objects.filter(status='pending')
    return render(request, "admin/view_cp.html",{'data':data})

@login_required(login_url='/myapp/login/')
def admin_view_all_cp(request):
    data=Cp.objects.all()
    return render(request, "admin/view_al_cp.html",{'data':data})


@login_required(login_url='/myapp/login/')
def approve_cp(request,id):
    email=Cp.objects.get(id=id).email
    name=Cp.objects.get(id=id).name
    Cp.objects.filter(id = id).update(status='approved')

    subject = 'Your Request Has Been Considered'
    messages = f"Hello,We are pleased to inform you that your{name}request has been successfully approved by the administrator. You can now log in and start uploading course materials to the Course Companion platform."
    from_email = 'coursecompanion05@gmail.com'
    recipient_list = [email]
    send_mail(subject, messages, from_email, recipient_list)

    return redirect('/myapp/admin_view_cp/')

@login_required(login_url='/myapp/login/')
def reject_cp(request,id):
    email = Cp.objects.get(id=id).email
    name = Cp.objects.get(id=id).name
    Cp.objects.filter(id=id).update(status='rejected')

    subject = 'Your Request Has Been Considered'
    messages = f"Hello,We are pleased to inform you that your{name}request has been successfully Rejected by the administrator.we regret to inform you that your registration could not be approved at this time."
    from_email = 'coursecompanion05@gmail.com'
    recipient_list = [email]
    send_mail(subject, messages, from_email, recipient_list)
    return redirect('/myapp/admin_view_cp/')

@login_required(login_url='/myapp/login/')
def view_cp_approve(request):
    data=Cp.objects.filter(status='approved')
    return render(request, "admin/view_cp_approve.html",{'data':data})

@login_required(login_url='/myapp/login/')
def view_cp_reject(request):
    data=Cp.objects.filter(status='rejected')
    return render(request, "admin/view_cp_reject.html",{'data':data})

@login_required(login_url='/myapp/login/')
def view_ccp(request):
    data=Course.objects.all()
    return render(request, "admin/view_ccp.html",{'data':data})

@login_required(login_url='/myapp/login/')
def view_user(request):
    data=Registration.objects.all()
    return render(request, "admin/view_user.html",{'data':data})

@login_required(login_url='/myapp/login/')
def view_cuser(request):
    data=Cp.objects.all()
    return render(request, "admin/view_cuser.html",{'data':data})


@login_required(login_url='/myapp/login/')
def view_review(request):
    data=Review.objects.all()
    return render(request, "admin/view_review.html",{'data':data})

@login_required(login_url='/myapp/login/')
def admin_view_cp_review(request):
    data=Creview.objects.all()
    return render(request, "admin/view_cp_review.html",{'data':data})

#COURSE PROVIDER
@login_required(login_url='/myapp/login/')
def cp_home(request):
    return render(request,"cp/index.html")

@login_required(login_url='/myapp/login/')
def view_cprofile(request):
    user= request.user
    data=Cp.objects.get(USER= user)
    return render(request, "cp/view_cprofile.html",{'data': data})

@login_required(login_url='/myapp/login/')
def edit_cprofile(request):
    user= request.user
    data=Cp.objects.get(USER= user)
    return render(request, "cp/edit_cprofile.html", {'data': data})

@login_required(login_url='/myapp/login/')
def edit_cprofile_post(request):
    fullname = request.POST['fullname']
    email = request.POST['email']
    phoneno = request.POST['phoneno']
    place = request.POST['place']
    post = request.POST['post']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    description = request.POST['description']

    user= request.user
    data = Cp.objects.get(USER_id = user.id)
    u=User.objects.get(id=user.id)
    u.username=email
    u.save()


    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        if photo!="":
            fs = FileSystemStorage()
            from datetime import datetime
            date = datetime.now().strftime("%y%M%d-%H%M%S") + "1.jpg"
            fs.save(date, photo)
            path = fs.url(date)
            data.photo = path

    if 'proof' in request.FILES:
        proof = request.FILES['proof']
        if proof!="":
            fs = FileSystemStorage()
            from datetime import datetime
            date = datetime.now().strftime("%y%M%d-%H%M%S") + "1.jpg"
            fs.save(date, proof)
            path = fs.url(date)
            data.proof = path

    data.name = fullname
    data.phone = phoneno
    data.email = email
    data.place = place
    data.post = post
    data.pin = pincode
    data.district = district
    data.state = state
    data.description = description
    data.save()
    messages.success(request,'Updated Succesfully!')
    return redirect('/myapp/view_cprofile/')

@login_required(login_url='/myapp/login/')
def addc_cp(request):
    return render(request, "cp/addc_cp.html")
#
# @login_required(login_url='/myapp/login/')
# def addc_cp_post(request):
#     coursename= request.POST['coursename']
#     coursecode= request.POST['coursecode']
#     duration=request.POST['duration']
#     description=request.POST['description']
#     user = request.user.id
#     print(user,"uuuuuuuuuuuuuuuuu")
#
#
#
#
#
#     cobj=Course()
#     cobj.coursename=coursename
#     cobj.coursecode=coursecode
#     cobj.duration=duration
#     cobj.description=description
#     cobj.CP=Cp.objects.get(USER_id=request.user.id)
#     cobj.save()
#     messages.success(request,'Course Added Succesfully')
#     return redirect('/myapp/addc_cp/')




@login_required(login_url='/myapp/login/')
def addc_cp_post(request):
    coursename = request.POST['coursename']
    coursecode = request.POST['coursecode']
    duration = request.POST['duration']
    description = request.POST['description']

    cp = Cp.objects.get(USER=request.user)

    if Course.objects.filter(coursecode=coursecode, CP=cp).exists():
        messages.warning(
            request,
            "You already added a course with this course code."
        )
        return redirect('/myapp/addc_cp/')

    cobj = Course()
    cobj.coursename = coursename
    cobj.coursecode = coursecode
    cobj.duration = duration
    cobj.description = description
    cobj.CP = cp
    cobj.save()

    messages.success(request, 'Course Added Successfully')
    return redirect('/myapp/addc_cp/')


@login_required(login_url='/myapp/login/')
def viewc_cp(request):
    user = request.user
    cp=Cp.objects.get(USER=user)
    data=Course.objects.filter(CP=cp)
    return render(request, "cp/viewc_cp.html",{'data':data})

@login_required(login_url='/myapp/login/')
def removecourse(request,cid):
    Course.objects.filter(id=cid).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('/myapp/viewc_cp/#abc')


@login_required(login_url='/myapp/login/')
def editc_cp(request,cid):
    cobj=Course.objects.get(id=cid)
    return render(request, "cp/editc_cp.html",{'data': cobj})

@login_required(login_url='/myapp/login/')
def editc_cp_post(request):
    coursecode = request.POST['coursecode']
    coursename = request.POST['coursename']
    duration = request.POST['duration']
    description = request.POST['description']
    cid= request.POST['cid']
    user = request.user

    cobj = Course.objects.get(id=cid)
    cobj.coursecode = coursecode
    cobj.coursename = coursename
    cobj.duration = duration
    cobj.description = description
    cobj.CP = Cp.objects.get(USER=user)
    cobj.save()
    messages.success(request,'Edited Successfully')
    return redirect('/myapp/viewc_cp/#abc')

@login_required(login_url='/myapp/login/')
def viewcp_review(request):
    data=Creview.objects.all()
    return render(request, "cp/viewcp_review.html",{'data':data})




@login_required(login_url='/myapp/login/')
def cp_change_password_get(request):

    return render(request, 'cp/change_password.html')

@login_required(login_url='/myapp/login/')
def cp_change_password_post(request):
    lid = request.user.id
    current_password = request.POST["current_password"]
    new_password = request.POST["new_password"]
    confirm_password = request.POST["confirm_password"]
    u = User.objects.get(id=lid)
    if u.check_password(current_password):
        if new_password==confirm_password:
            u.set_password(confirm_password)
            u.save()
            return redirect('/myapp/login/')
        else:
            return redirect('/myapp/cp_change_password_get/')
    else:
        return redirect('/myapp/cp_change_password_get/')

@login_required(login_url='/myapp/login/')
def viewcp_req(request):
    data=Join.objects.filter(course__CP__USER=request.user).order_by('-id')
    return render(request, "cp/viewcp_req.html",{'data':data})

@login_required(login_url='/myapp/login/')
def approve_creq(request,id):
    Join.objects.filter(id = id).update(status='approved')


    server = smtplib.SMTP('smtp.gmail.com', 587)

    cc=Cp.objects.get(USER_id=request.user.id)


    server.starttls()
    server.login("coursecompanion05@gmail.com", "qrry eafb typk khjw")  # App Password
    to = Join.objects.get(id=id).REGISTRATION.email
    subject = "Request Approved"
    body=('''Congratulations!!!,\n\n"
        "Your request has been approved. Welcome! If you need further help, reply to this email.\n\n"
        "Regards,\n"
        "Course Companion Team"'''
    )
    # body = "Your new password is " + str(new_pass)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)
    # Disconnect from the server
    server.quit()

    # recipient = join.REGISTRATION.email  # keep your existing relation
    # subject = "Request Approved"
    # message = (
    #     "Assalamu alaikum,\n\n"
    #     "Your request has been approved. Welcome! If you need further help, reply to this email.\n\n"
    #     "Regards,\n"
    #     "Course Companion Team"
    # )
    # from_email = getattr(settings, "EMAIL_HOST_USER", None)
    #
    # try:
    #     # send mail (will raise if config wrong and fail_silently=False)
    #     send_mail(subject, message, from_email, [recipient], fail_silently=False)
    #     messages.success(request, "Request approved and email sent to the user.")
    # except Exception as e:
    #     # still approved, but email failed — log or message the admin
    #     messages.warning(request, f"Request approved but email sending failed: {e}")

    return redirect('/myapp/viewcp_req/')

@login_required(login_url='/myapp/login/')
def reject_creq(request,id):
    Join.objects.filter(id = id).update(status='rejected')
    return redirect('/myapp/viewcp_req/')

@login_required(login_url='/myapp/login/')
def video_cp(request):
    c = Course.objects.filter(CP__USER_id=request.user.id)
    return render(request,"cp/video_cp.html",{'data':c})

@login_required(login_url='/myapp/login/')
def video_cp_post(request):
    video=request.FILES['videoFile']
    course= request.POST['courseName']
    title=request.POST['videoTitle']
    fs = FileSystemStorage()
    from datetime import datetime
    date = datetime.now().strftime("%y%M%d-%H%M%S") + ".mp4"
    fs.save(date, video)
    path = fs.url(date)

    # # video_path = r"C:\Users\ridar\Downloads\COA module 1.mp4"
    #
    # from moviepy.editor import VideoFileClip
    #
    # # Path to your video file
    # video_path = r"C:\Users\ridar\Downloads\COA module 1.mp4"
    # audio_path = r"C:\Users\ridar\Downloads\COA_module1_audio.wav"
    #
    # # Load video
    # video = VideoFileClip(video_path)
    #
    # # Extract audio and save as WAV (or MP3 if you prefer)
    # video.audio.write_audiofile(audio_path)
    #
    # print(f"Audio successfully saved to: {audio_path}")

    # save_audio_from_video.py
    import subprocess
    import shutil
    from pathlib import Path
    import speech_recognition as sr
    import timeit


    def audio_to_text(audio_path):
        import speech_recognition as sr
        # Initialize the recognizer
        recognizer = sr.Recognizer()
        # Load the WAV file
        # wav_file = "C:\\Users\\ridar\\PycharmProjects\\coursecompanion\\media\\audio\\COA module 1.wav"  # Replace with your WAV file path
        # Process the audio file
        text=""
        wav_file = audio_path
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)  # Read the audio file
        # Convert speech to text
        try:
            text = recognizer.recognize_google(audio_data)  # Using Google Web Speech API
            print("Transcribed Text: ", text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        return text



    # ====== EDIT THESE ======
    video_path = "C:\\Users\\ridar\\PycharmProjects\\coursecompanion\\media\\"+date  # <--- change to your uploaded video path if different
    output_dir = Path(r"C:\Users\ridar\PycharmProjects\coursecompanion\media\audio")
    output_format = "wav"  # "wav" or "mp3" etc.
    sample_rate = "16000"  # optional, set to None to keep original
    channels = 1  # 1 = mono, 2 = stereo
    # ========================

    # ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # build output file name from video file name
    video_path_obj = Path(video_path)
    if not video_path_obj.exists():
        print("Error: video file not found:", video_path)

    output_fname = video_path_obj.stem + "." + output_format
    output_path = output_dir / output_fname

    # locate ffmpeg
    ffmpeg_cmd = shutil.which(
        "ffmpeg") or r"C:\Users\ridar\Downloads\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"  # if you installed ffmpeg to C:\ffmpeg\bin, keep this fallback
    # ffmpeg_cmd = shutil.which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"  # if you installed ffmpeg to C:\ffmpeg\bin, keep this fallback
    if not Path(ffmpeg_cmd).exists():
        print("ffmpeg not found. Please install FFmpeg and add it to PATH, or update ffmpeg_cmd variable.")
        print("Download: https://ffmpeg.org/download.html")

    # build ffmpeg command
    cmd = [
        ffmpeg_cmd, "-y",  # overwrite if exists
        "-i", str(video_path_obj),
        "-vn"  # drop video stream
    ]

    # optional: set sample rate / channels
    if sample_rate:
        cmd += ["-ar", str(sample_rate)]
    if channels in (1, 2):
        cmd += ["-ac", str(channels)]

    # choose codec depending on format
    if output_format.lower() == "wav":
        cmd += ["-acodec", "pcm_s16le"]
    elif output_format.lower() == "mp3":
        cmd += ["-acodec", "libmp3lame"]
    # add output path last
    cmd.append(str(output_path))

    # run ffmpeg
    try:
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=False)
        print("✅ Audio extracted to:", output_path)

        print(type(output_path))

        k=audio_to_text(str(output_path))

        v = Video()
        v.videoFile = path
        v.COURSE = Course.objects.get(id=course)
        v.title = title
        v.date = datetime.now().today()
        v.transcribedtext=k
        v.save()


    except subprocess.CalledProcessError as e:
        print("ffmpeg failed with:", e)


    return redirect('/myapp/video_cp/')
@login_required(login_url='/myapp/login/')
def cpview_video(request):
    data=Video.objects.filter(COURSE__CP__USER_id=request.user.id)
    return render(request, "cp/cpview_video.html",{'data':data})

@login_required(login_url='/myapp/login/')
def edit_video(request, vid):
    cobj = Video.objects.get(id=vid)
    c = Course.objects.filter(CP__USER_id=request.user.id)
    return render(request,'cp/edit_video.html',{'data':cobj,'data1':c})

@login_required(login_url='/myapp/login/')
def edit_video_post(request):
    id=request.POST['id']
    course = request.POST['courseName']
    title = request.POST['videoTitle']

    v = Video.objects.get(id=id)
    if 'videoFile' in request.FILES:
        video = request.FILES['videoFile']
        fs = FileSystemStorage()
        date = datetime.now().strftime("%y%M%d-%H%M%S") + ".mp4"
        fs.save(date, video)
        path = fs.url(date)
        v.videoFile = path

    v.COURSE = Course.objects.get(id=course)
    v.title = title
    v.date = datetime.now().today()
    v.save()
    return redirect('/myapp/cpview_video/#abc')

@login_required(login_url='/myapp/login/')
def delete_video(request, vid):
    cobj = Video.objects.get(id=vid).delete()
    return redirect('/myapp/cpview_video/')


@login_required(login_url='/myapp/login/')
def material_cp(request):
    c = Course.objects.filter(CP__USER_id=request.user.id)
    return render(request,"cp/material_cp.html",{'data':c})

@login_required(login_url='/myapp/login/')
def material_cp_post(request):
    materialf=request.FILES['MaterialFile']
    course= request.POST['courseName']
    material=request.POST['MaterialTitle']
    fs = FileSystemStorage()
    from datetime import datetime
    date = datetime.now().strftime("%y%M%d-%H%M%S") + ".pdf"
    fs.save(date, materialf)
    path = fs.url(date)
    v = Material()

    v.COURSE = Course.objects.get(id=course)
    v.materialename = material
    v.File=path
    v.date = datetime.now().today()
    v.save()

    return redirect('/myapp/material_cp/')
@login_required(login_url='/myapp/login/')
def cpview_material(request):
    data=Material.objects.filter(COURSE__CP__USER_id=request.user.id)
    return render(request, "cp/cpview_material.html",{'data':data})

@login_required(login_url='/myapp/login/')
def edit_material(request, vid):
    cobj = Material.objects.get(id=vid)
    c = Course.objects.filter(CP__USER_id=request.user.id)
    return render(request,'cp/edit_material.html',{'data':cobj,'data1':c})

@login_required(login_url='/myapp/login/')
def edit_material_post(request):
    id=request.POST['id']
    course = request.POST['courseName']
    title = request.POST['MaterialTitle']

    v = Material.objects.get(id=id)
    if 'MaterialFile' in request.FILES:
        material = request.FILES['MaterialFile']
        fs = FileSystemStorage()
        date = datetime.now().strftime("%y%M%d-%H%M%S") + ".pdf"
        fs.save(date, material)
        path = fs.url(date)
        v.File = path

    v.COURSE = Course.objects.get(id=course)
    v.materialename = title
    v.date = datetime.now().today()
    v.save()
    return redirect('/myapp/cpview_material/#abc')

@login_required(login_url='/myapp/login/')
def delete_material(request, vid):
    cobj = Material.objects.get(id=vid).delete()
    return redirect('/myapp/cpview_material/')

@login_required(login_url='/myapp/login/')
def admin_changepassword_get (request):

    return render(request,'admin/change password.html')




@login_required(login_url='/myapp/login/')
def admin_changepassword_post (request):
    lid=request.user.id
    current_password =request.POST["current_password"]
    new_password=request.POST["new_password"]
    confirm_password=request.POST["confirm_password"]

    u=User.objects.get(id=lid)

    if u.check_password(current_password):
        if new_password==confirm_password:
            u.set_password(confirm_password)
            u.save()
            return redirect('/myapp/login/')
        else:
            messages.error(request,'Passwords does not match')
            return redirect('/myapp/admin_changepassword_get/#abc')
    else:
        messages.error(request, 'Current Password Incorrect')
        return redirect('/myapp/admin_changepassword_get/#abc')


#=========== USER============


@csrf_exempt
def user_signup(request):
    name = request.POST["uname"]
    dob = request.POST["udob"]
    phone = request.POST["uphone"]
    gender = request.POST["ugender"]
    email = request.POST["uemail"]
    place = request.POST["uplace"]
    post = request.POST["upost"]
    pin = request.POST["upin"]
    district = request.POST["udistrict"]
    password = request.POST["upassword"]
    confirmpassword = request.POST["uconfirmpassword"]

    photo = request.FILES["photo"]

    fs = FileSystemStorage()
    from datetime import datetime
    date = datetime.now().strftime("%y%M%d-%H%M%S") + "1.jpg"
    fs.save(date, photo)

    path = fs.url(date)

    user = User.objects.create_user(username=email, password=password)
    user.groups.add(Group.objects.get(name="users"))
    user.save()

    r=Registration()
    r.name=name
    r.phone=phone
    r.email=email
    r.dob=dob
    r.gender=gender
    r.photo=path
    r.place=place
    r.post=post
    r.pin=pin
    r.district=district
    r.status='pending'
    r.USER=user
    r.save()
    return JsonResponse({'status':'ok'})


@csrf_exempt
def user_login(request):
    username=request.POST["Username"]
    password=request.POST["Password"]
    print(request.POST)
    log = authenticate(request, username=username, password=password)
    if log is not None:
        # print("jjjjjjjjjjjjjj")
        login(request, log)
        # user=
        d=request.user
        # print(d.id,"==============")
        if log.groups.filter(name='users'):
            # print("kkkkkkkkkkkkkkk")
            return JsonResponse({'status':'ok','lid':str(d.id)})
        else:
            return JsonResponse({'status':'no'})
    return JsonResponse({'status':'no'})

@csrf_exempt
def app_forgot_password(request):
    email=request.POST['Username']
    if User.objects.filter(username=email):
        import random
        temp=random.randint(0000,9999)
        user=User.objects.get(username=email)
        user.set_password(str(temp))
        user.save()

        subject='Course Companion – Password Recovery'
        messages=f"We received a request to reset the password for your Course Companion account.Password:{str(temp)}"
        from_email='coursecompanion05@gmail.com'
        recipient_list=[email]
        send_mail(subject,messages,from_email,recipient_list)
    return JsonResponse({'status':'ok'})




@csrf_exempt
def user_view_profile(request):
   lid=request.POST['lid']
   print(lid)
   data=Registration.objects.get(USER_id=lid)
   print(data)
   return JsonResponse({'status': 'ok','name':data.name,'phone':data.phone,'email':data.email,'dob':data.dob,'gender':data.gender,'photo':data.photo,
                        'place':data.place,'post':data.post,'pin':data.pin,'district':data.district})

@csrf_exempt
def user_edit_profile(request):
    name= request.POST["uname"]
    dob = request.POST["udob"]
    gender= request.POST["ugender"]
    phone = request.POST["uphone"]
    email = request.POST["uemail"]
    place = request.POST["uplace"]
    post = request.POST["upost"]
    pin = request.POST["upin"]
    district = request.POST["udistrict"]
    lid=request.POST["lid"]




    data = Registration.objects.get(USER=lid)
    if 'photo' in request.FILES:
        photo = request.POST["photo"]
        if photo !="":
            fs = FileSystemStorage()
            from datetime import datetime
            date = datetime.now().strftime("%y%M%d-%H%M%S") + "1.jpg"
            fs.save(date, photo)
            path = fs.url(date)
            data.photo = path

    data.name=name
    data.dob=dob
    data.gender=gender
    data.phone=phone
    data.email=email
    data.place=place
    data.post=post
    data.pin=pin
    data.district=district

    data.save()

    return JsonResponse({'status': 'ok'})

@csrf_exempt
def user_view_cp(request):
    data=Cp.objects.filter(status='approved')
    l=[]
    for i in data:
        # rr=Review.objects.filter()
        l.append({
            'id':i.id,
            'name':i.name,
            'phone':i.phone,
            'email':i.email,
            'place':i.place,
            'post':i.post,
            'pin':i.pin,
            'district':i.district,
            'state':i.state,
            # 'status':i.status,
            'proof':i.proof,
            'photo':i.photo,
            'description':i.description,

        })
    print(l)
    return JsonResponse({'status': 'ok','data':l})

@csrf_exempt
def send_course_req(request):
    lid=request.POST["lid"]
    return JsonResponse({'status ':'ok'})

@csrf_exempt
def user_review(request):
    lid=request.POST["lid"]
    print(lid)
    review=request.POST["ureview"]
    rating = request.POST["urating"]

    r=Review()
    r.review=review
    r.rating=rating
    r.date=datetime.now().today()
    r.REGISTRATION=Registration.objects.get(USER=lid)
    r.save()

    return JsonResponse({'status': 'ok'})


@csrf_exempt
def course_review(request):
    lid=request.POST["lid"]
    cid=request.POST["cid"]
    print(lid)
    review=request.POST["ureview"]
    rating = request.POST["urating"]

    r=Creview()
    r.review=review
    r.rating=rating
    r.date=datetime.now().today()
    r.COURSE=Course.objects.get(id=cid)
    r.REGISTRATION=Registration.objects.get(USER=lid)
    r.save()

    return JsonResponse({'status': 'ok'})
#
# def view_review(request):
#     return render('')


@csrf_exempt
def user_view_offcourse(request):
    lid=request.POST['lid']
    cp_id=request.POST['cp_id']
    print(cp_id,"==========")
    data=Course.objects.filter(CP=cp_id)
    l=[]
    for i in data:
        if Join.objects.filter(REGISTRATION__USER=lid,course_id=i.id).exists():

            l.append({
                'id':i.id,
                'coursename':i.coursename,
                'duration':i.duration,
                'description':i.description,
                'jstatus':"yes"
            })
        else:

            l.append({
                'id': i.id,
                'coursename': i.coursename,
                'duration': i.duration,
                'description': i.description,
                'jstatus': "no"
            })
    return JsonResponse({'status': 'ok' , 'data':l} )

@csrf_exempt
def send_req(request):
    lid=request.POST['lid']
    cid=request.POST['cid']
    jobj=Join()
    jobj.course=Course.objects.get(id=cid)
    jobj.date=datetime.now().today()
    jobj.status='pending'
    jobj.REGISTRATION=Registration.objects.get(USER=lid)
    jobj.save()

    return JsonResponse({'status': 'ok'})

@csrf_exempt
def req_status(request):
    lid=request.POST['lid']
    data=Join.objects.filter(REGISTRATION__USER=lid,status='approved')
    l = []
    for i in data:

            l.append({
                'id': i.id,
                'name': i.course.CP.name,
                'cid': i.course.id,
                'coursename': i.course.coursename,
                'date': i.date,
                'description': i.course.description,
                'status':i.status,
            })
    return JsonResponse({'status' : 'ok', 'data':l})

@csrf_exempt
def uview_video(request):
    cid=request.POST["crsid"]
    print(cid,'gchbvjbvhjvjkvjvh')

    data = Video.objects.filter(COURSE_id=cid)
    l = []
    for i in data:
        l.append({
            'id': i.id,
            'date': i.date,
            'title': i.title,
            'videoFile': i.videoFile,

        })
    print("aaaaaaaaaaaaaaaaaaaaaaaaa")
    print(l)
    return JsonResponse({'status': 'ok', 'data': l})

@csrf_exempt
def uview_material(request):
    cid=request.POST["crsid"]
    print(cid)

    data = Material.objects.filter(COURSE_id=cid)
    l = []
    for i in data:
        l.append({

            'MaterialName': i.materialename,
            'MaterialFile': i.File,

        })
    return JsonResponse({'status': 'ok', 'data': l})


# @csrf_exempt
# def view_joined_course(request):
#     lid=request.POST["lid"]
#     # cid=request.POST["crsid"]
#     # print(cid)
#
#     data = Join.objects.filter(REGISTRATION__USER_id=lid,status='approved')
#     l = []
#     for i in data:
#         cc=Video.objects.get(COURSE_id=i.course.id)
#         l.append({
#             'id': cc.id,
#             'date': cc.date,
#             'title': cc.title,
#             'videoFile': cc.videoFile,
#
#         })
#     print("aaaaaaaaaaaaaaaaaaaaaaaaa")
#     print(l)
#     return JsonResponse({'status': 'ok', 'data': l})


@csrf_exempt
# def view_joined_course(request):
#     lid = request.POST["lid"]
#
#     joins = Join.objects.filter(
#         REGISTRATION__USER_id=lid,
#         status='approved'
#     )
#
#     data = []
#
#     for j in joins:
#         videos = Video.objects.filter(COURSE=j.course)
#
#         for v in videos:
#             data.append({
#                 'id': v.id,
#                 'date': v.date,
#                 'title': v.title,
#                 'videoFile': v.videoFile,
#                 # 'course_id': j.course.id
#             })
#
#     return JsonResponse({'status': 'ok', 'data': data})


@csrf_exempt
def changepassword(request):
    lid=request.POST["lid"]
    currentpassword=request.POST["currentpassword"]
    newpassword=request.POST["newpassword"]

    u=User.objects.get(id=lid)
    u.set_password(newpassword)
    u.save()


    return  JsonResponse(
        {
            'status':'ok'
        }
    )




@csrf_exempt
def view_creview(request):
    cid=request.POST["cid"]
    l=[]
    data=Creview.objects.filter(COURSE_id=cid)
    for i in data:
        l.append({
            'id': i.id,
            'review': i.review,
            'rating': i.rating,
            'date': i.date,
            'name': i.REGISTRATION.name,

        })


    return JsonResponse({'status': 'ok','data':l})
#
# def view_review(request):
#     return render('')

@csrf_exempt
def chat_bot(request):

    message=request.POST["message"]
    # print(message)
    #
    apikey="AIzaSyDTsgAuVQEAfTjcZbUzCAyWp24R2y8USm4"
    #
    # data= Video.objects.all()
    #
    # li=[]
    #
    # for i in data:
    #
    #     li.append(
    #         i.transcribedtext
    #     )
    #
    # # pip
    # # install
    # # google - generativeai
    # # faiss - cpu
    #
    # import os
    # import google.generativeai as genai
    # import faiss
    # import numpy as np
    #
    #
    # DATA_DIR = "text_data"  # Folder containing multiple .txt files
    # API_KEY =apikey
    # MODEL_EMBED = "models/embedding-001"
    # MODEL_CHAT = "gemini-2.5-flash"
    #
    #
    # genai.configure(api_key=API_KEY)
    #
    # def chunk_text(text, chunk_size=1000, overlap=100):
    #     chunks = []
    #     for i in range(0, len(text), chunk_size - overlap):
    #         chunk = text[i:i + chunk_size]
    #         chunks.append(chunk)
    #     return chunks
    #
    # # ==== STEP 3: CREATE EMBEDDINGS ====
    # def create_embeddings(texts):
    #     print("🔹 Generating embeddings...")
    #     embeddings = []
    #     for t in texts:
    #         emb = genai.embed_content(model=MODEL_EMBED, content=t)["embedding"]
    #         embeddings.append(emb)
    #     return np.array(embeddings).astype("float32")
    #
    # # ==== STEP 4: BUILD VECTOR INDEX ====
    # def build_index(embeddings):
    #     dim = len(embeddings[0])
    #     index = faiss.IndexFlatL2(dim)
    #     index.add(embeddings)
    #     return index
    #
    # # ==== STEP 5: GEMINI CHAT ====
    # def chat_with_gemini(query, texts, index, k=3):
    #     query_emb = genai.embed_content(model=MODEL_EMBED, content=query)["embedding"]
    #     query_emb = np.array([query_emb]).astype("float32")
    #     distances, indices = index.search(query_emb, k)
    #
    #     # Collect relevant chunks
    #     context = "\n\n".join([texts[i] for i in indices[0]])
    #     prompt = f"""
    #     You are a knowledgeable assistant trained on these documents.
    #     Use the context below to answer accurately.
    #
    #     CONTEXT:
    #     {context}
    #
    #     QUESTION:
    #     {query}
    #
    #     ANSWER:
    #     """
    #
    #     model = genai.GenerativeModel(MODEL_CHAT)
    #     response = model.generate_content(prompt)
    #     return response.text
    #
    # # ==== MAIN ====
    #
    #     # Load & preprocess data
    # all_texts=li
    #
    #
    # # Optionally split into chunks
    # chunks = []
    # for txt in all_texts:
    #     chunks.extend(chunk_text(txt))
    #
    # # Create embeddings + index
    # embeddings = create_embeddings(chunks)
    # index = build_index(embeddings)
    #
    # print("✅ Chatbot is ready!")
    #
    # # Chat loop
    #
    # answer = chat_with_gemini(message, chunks, index)
    # print("\n🤖 Gemini:", answer)


    """
    sentence_transformer_embeddings.py

    Full drop-in script to replace Google Generative AI embeddings with
    SentenceTransformers locally while keeping your FAISS index + Gemini chat.

    Requirements (pip):
      pip install sentence-transformers faiss-cpu google-generativeai numpy

    Notes:
     - This script expects your transcribed texts as a Python list `all_texts`.
     - It caches embeddings to EMB_CACHE_FILE and the chunk texts to CHUNKS_CACHE_FILE.
     - It persists FAISS index to FAISS_INDEX_FILE.
     - Set GENAI_API_KEY in env if you still want to use Gemini for generation.

    Usage:
      1. Put your list of transcribed texts into `all_texts` (e.g., load from Django ORM).
      2. Run: python sentence_transformer_embeddings.py

    """

    import os

    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer
    import google.generativeai as genai

    # ---------------- CONFIG ----------------
    MODEL_NAME = os.environ.get("ST_MODEL", "sentence-transformers/all-mpnet-base-v2")
    EMB_CACHE_FILE = "embeddings.npy"
    CHUNKS_CACHE_FILE = "chunks.npy"
    FAISS_INDEX_FILE = "faiss.index"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    BATCH_SIZE = 64  # batch size for sentence-transformers encode
    K = 3

    # Optional: Genie/Gemini config for chat generation (keep if you use it)
    GENAI_API_KEY =apikey
    MODEL_CHAT = os.environ.get("GENAI_CHAT_MODEL", "gemini-2.5-flash")
    if GENAI_API_KEY:
        genai.configure(api_key=GENAI_API_KEY)

    # ---------------- HELPERS ----------------

    def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
        """Split `text` into overlapping chunks."""
        chunks = []
        if not text:
            return chunks
        step = chunk_size - overlap
        for i in range(0, len(text), step):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def batch_iterable(iterable, n):
        it = iter(iterable)
        while True:
            batch = []
            try:
                for _ in range(n):
                    batch.append(next(it))
            except StopIteration:
                if batch:
                    yield batch
                break
            yield batch

    # ---------------- EMBEDDINGS (SentenceTransformers) ----------------
    class Embedder:
        def __init__(self, model_name=MODEL_NAME):
            print(f"Loading SentenceTransformer model: {model_name} ...")
            self.model = SentenceTransformer(model_name)
            # tune parameters if you need GPU/FP16 etc

        def encode(self, texts, batch_size=BATCH_SIZE, show_progress_bar=False):
            """Encode list of texts -> numpy float32 array.
               Uses the sentence-transformers encode() method which supports batching.
            """
            if not texts:
                return np.zeros((0, self.model.get_sentence_embedding_dimension()), dtype="float32")
            embs = self.model.encode(texts, batch_size=batch_size, show_progress_bar=show_progress_bar)
            arr = np.array(embs, dtype="float32")
            return arr

    # ---------------- FAISS UTIL ----------------

    def build_faiss_index(embeddings: np.ndarray):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index

    def save_faiss(index, path=FAISS_INDEX_FILE):
        faiss.write_index(index, path)

    def load_faiss(path=FAISS_INDEX_FILE):
        return faiss.read_index(path)

    # ---------------- PIPELINE ----------------

    def prepare_index_from_texts(all_texts, embedder: Embedder):
        """
        all_texts: list[str] -- raw transcribed documents
        returns: chunks (list[str]), embeddings (np.ndarray), faiss_index
        """
        print("Preparing chunks from documents...")
        chunks = []
        seen = set()
        for txt in all_texts:
            for c in chunk_text(txt):
                # light dedupe by first 200 chars
                key = c.strip()[:200]
                if key not in seen:
                    chunks.append(c)
                    seen.add(key)

        # Save chunks for reproducibility
        np.save(CHUNKS_CACHE_FILE, np.array(chunks, dtype=object))

        # If embeddings + index cached, load them
        if os.path.exists(EMB_CACHE_FILE) and os.path.exists(FAISS_INDEX_FILE):
            print("Loading cached embeddings and FAISS index...")
            embeddings = np.load(EMB_CACHE_FILE)
            index = load_faiss(FAISS_INDEX_FILE)
            return chunks, embeddings, index

        # Otherwise compute embeddings in batches
        print(f"Encoding {len(chunks)} chunks with SentenceTransformer (batch_size={BATCH_SIZE})...")
        # You can encode all at once; SentenceTransformer handles batching internally.
        embeddings = embedder.encode(chunks, batch_size=BATCH_SIZE, show_progress_bar=True)

        # Save embeddings and build index
        np.save(EMB_CACHE_FILE, embeddings)
        index = build_faiss_index(embeddings)
        save_faiss(index, FAISS_INDEX_FILE)

        print("Saved embeddings and FAISS index.")
        return chunks, embeddings, index

    # ---------------- RETRIEVAL + CHAT ----------------

    def retrieve_top_k(query, embedder: Embedder, chunks, index, k=K):
        q_emb = embedder.encode([query])  # shape (1, dim)
        distances, indices = index.search(q_emb, k)
        idxs = [int(i) for i in indices[0] if i != -1]
        retrieved = [chunks[i] for i in idxs]
        return retrieved, distances[0]

    def chat_with_gemini(query, embedder: Embedder, chunks, index, k=K):
        """If you want to use Gemini for answer generation. Requires GENAI_API_KEY env var.
           If GENAI_API_KEY is not set, this function will instead return a combined-context answer
           as a simple concatenation (useful for testing offline).
        """
        retrieved, dists = retrieve_top_k(query, embedder, chunks, index, k=k)
        context = "\n\n".join(retrieved)

        prompt = f"""
    You are a knowledgeable assistant trained on these documents.
    Use the context below to answer accurately.

    CONTEXT:
    {context}

    QUESTION:
    {query}

    ANSWER:
    """

        if GENAI_API_KEY:
            model = genai.GenerativeModel(MODEL_CHAT)
            res = model.generate_content(prompt)
            return res.text
        else:
            # Offline fallback: return the context + a template
            return "CONTEXT:\n" + context + "\n\n----\nAnswer (offline): Use the context above to craft a response."

    # ---------------- MAIN / EXAMPLE USAGE ----------------

        # Example: integrate with Django (replace with your ORM call)
    try:
        # If running inside Django manage.py context, import your model
        from myapp.models import Video  # <- replace with real app & model
        data = Video.objects.all()
        all_texts = [v.transcribedtext for v in data]
    except Exception:
        # Fallback demo texts
        all_texts = [
            "This is an example transcript from video A. It talks about FFmpeg usage and audio conversion.",
            "Video B transcription: Resin art techniques and jewelry making workflows."
        ]

    embedder = Embedder()
    chunks, embeddings, index = prepare_index_from_texts(all_texts, embedder)
    print(f"Index ready with {len(chunks)} chunks.")

    # Example query
    q = message
    ans = chat_with_gemini(q, embedder, chunks, index, k=3)
    print("\n=== ANSWER ===\n")


    if ans ==" am sorry, but the provided context does not contain information on how to convert MP4 to WAV using ffmpeg in Python. The documents discuss Java syntax, strings, and type casting.":

        print("1")
        return  JsonResponse(
            {
                'status':'no'
            }
        )
    else:
        print("2")


        return JsonResponse({'status': 'ok', 'ans':ans})




# user=User.objects.get(username="ayishasafapk@gmail.com")
# user.set_password("123456")
# user.save()



