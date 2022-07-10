from django.http.request import HttpRequest
from django.utils import html
from .models import Profile
from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from sendEmail.mailer import send_mail
from django.contrib.auth import authenticate, login as lg
from django.contrib.auth.decorators import login_required
import requests
from urllib.parse import quote
from django.contrib.auth import logout as logt

# Create your views here.

defaultSettings = dict({
    'selectionStyle': 'line',
    'highlightActiveLine': True,
    'highlightSelectedWord': True,
    'readOnly': False,
    'copyWithEmptySelection': False,
    'cursorStyle': 'ace',
    'mergeUndoDeltas': True,
    'behavioursEnabled': True,
    'wrapBehavioursEnabled': True,
    'enableAutoIndent': True,
    'showLineNumbers': True,
    'hScrollBarAlwaysVisible': False,
    'vScrollBarAlwaysVisible': False,
    'highlightGutterLine': True,
    'animatedScroll': False,
    'showInvisibles': False,
    'showPrintMargin': True,
    'printMarginColumn': 80,
    'printMargin': 80, 'fadeFoldWidgets': False,
    'showFoldWidgets': True,
    'displayIndentGuides': True,
    'showGutter': True,
    'fontSize': 24,
    'scrollPastEnd': 0,
    'theme': 'ace/theme/cobalt',
    'maxPixelHeight': 0,
    'useTextareaForIME': True,
    'scrollSpeed': 2,
    'dragDelay': 0,
    'dragEnabled': True,
    'focusTimeout': 0,
    'tooltipFollowsMouse': True,
    'firstLineNumber': 1,
    'overwrite': False,
    'newLineMode': 'auto',
    'useWorker': True,
    'useSoftTabs': True,
    'navigateWithinSoftTabs': False,
    'tabSize': 4,
    'wrap': 'off',
    'indentedSoftWrap': True,
    'foldStyle': 'markbegin',
    'mode': 'ace/mode/html',
    'enableMultiselect': True,
    'enableBlockSelect': True,
    'enableBasicAutocompletion': False,
    'enableLiveAutocompletion': False,
    'enableSnippets': False
})


def formatDate(date):
    return "{} {}, {}".format(str(date.day), str(date.strftime('%B')[:3]), str(date.year)[2:])


def home(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {
        "title": "ClassJoiner"
    }
    return render(request, 'accounts/register.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            if User.objects.filter(username=username).first():
                return HttpResponse(json.dumps({"error": "Username is already taken"}))

            response = requests.get(
                "https://isitarealemail.com/api/email/validate",
                params={'email': email})
            status = response.json()['status']

            if status == "invalid":
                return HttpResponse(json.dumps({"error": "Email is Invalid"}))
            elif status != "valid":
                return HttpResponse(json.dumps({"error": "Email is unknown"}))

            if User.objects.filter(email=email).first():
                return HttpResponse(json.dumps({"error": "Email is already taken"}))

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = uuid.uuid4().hex

            profile_obj = Profile.objects.create(
                user=user_obj, auth_token=auth_token)
            profile_obj.save()

            subject = "Account Verification"
            body = "OTP - {}\nHiii...\nClassJoiner is here".format(auth_token)
            send_mail(subject=subject, body=body, emailList=[email, ])
            return HttpResponse(json.dumps({"status": "success"}))
        except Exception as e:
            return HttpResponse(json.dumps({"error": e}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj:
            return HttpResponse(json.dumps({"error": "No such accont exists"}))

        if not profile_obj.is_verified:
            return HttpResponse(json.dumps({"error": "Profile is not verified check your mail"}))

        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponse(json.dumps({"error": "Wrong password."}))

        lg(request, user)
        return HttpResponse(json.dumps({"status": "success"}))
    else:
        context = {
            "title": "ClassJoiner"
        }
        return render(request, 'accounts/login.html', context)


def verifyToken(request, username):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        user = Profile.objects.filter(user=user_obj).first()

        if not user:
            return HttpResponse(json.dumps({"error": "User not found"}))

        if user.is_verified:
            return HttpResponse(json.dumps({"error": "User Already Verified"}))
        else:
            auth_token = request.POST.get("auth_token")
            stored_token = user.auth_token

            if(stored_token == auth_token):
                user.is_verified = True
                user.save()
                return HttpResponse(json.dumps({"status": "success"}))
            else:
                return HttpResponse(json.dumps({"error": "otp mismatched"}))

    else:
        context = {
            "title": "ML-TOOLBOX"
        }
        return render(request, "accounts/verifyToken.html", context)


def success(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'accounts/success.html', context)


def forgetPassword(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        user = Profile.objects.filter(user=user_obj).first()

        if user is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        auth_token = uuid.uuid4().hex
        email = user.user.email
        user.auth_token = auth_token
        user.save()

        subject = "Reset Password"
        link = "Link - {}/accounts/VerifyForgetToken/{}/{}".format(
            request.META['HTTP_HOST'], quote(username), auth_token)
        send_mail(subject=subject, body=link, emailList=[email], html=False)
        return HttpResponse(json.dumps({"email": email}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def VerifyForgetToken(request, username, auth_token):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        newPassword = request.POST.get("password")
        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        user = Profile.objects.filter(user=user_obj).first()

        if not user:
            return HttpResponse(json.dumps({"error": "User not found"}))

        context = {
            "title": "ML-TOOLBOX"
        }

        if user.auth_token == auth_token:
            user_obj.set_password(newPassword)
            user_obj.save()
            return HttpResponse(json.dumps({"status": "success"}))
        else:
            return HttpResponse(json.dumps({"error": "Authentication Token Expired"}))
    else:
        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        user = Profile.objects.filter(user=user_obj).first()

        if not user:
            return HttpResponse(json.dumps({"error": "User not found"}))

        context = {
            "title": "ML-TOOLBOX"
        }

        if user.auth_token == auth_token:
            return render(request, "accounts/verifyForgetToken.html", context)
        else:
            return HttpResponse(json.dumps({"error": "Authentication Token Expired"}))


def logout(request):
    if not request.user.is_authenticated:
        return redirect("home")
    logt(request)
    return redirect("home")


def fetchUserLastCode(request):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({"status": "failed"}))
    if request.method == "POST":
        username = request.POST.get("user")
        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        user = Profile.objects.filter(user=user_obj).first()

        if user is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        context = {}

        context["lastSettings"] = json.loads(json.dumps(user.lastSettings))
        context["lastMode"] = user.lastMode  # dark or light

        try:
            context["lastCode"] = user.codes.last().codeId
        except:
            context["lastCode"] = "noCode"

        return HttpResponse(json.dumps(context))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getLastSettings(request):
    if request.user.is_authenticated == False:
        return HttpResponse(json.dumps(defaultSettings))
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        
        if profile is None:
            return HttpResponse(json.dumps({"error": "User not found"}))
        
        return HttpResponse(json.dumps(profile.lastSettings))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def myCodes(request):
    if request.user.is_authenticated == False:
        return HttpResponse(json.dumps({"status": "success"}))
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.filter(user=user).first()

        if profile is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        codes = profile.codes.all().order_by('-dateOfCreation')
        codeDetails = {}

        for index, code in enumerate(codes):
            codeDetails[index] = {
                "codeId": code.codeId,
                "codeName": code.codeName,
            }

        return HttpResponse(json.dumps(codeDetails))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


# if __name__ == "__main__":
