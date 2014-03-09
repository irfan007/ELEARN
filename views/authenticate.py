from django.shortcuts import render_to_response
from App.models import tbl_user
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect
from E_LEARN.settings import URL_PREFIX, EMAIL_HOST_USER
from django.core.mail import send_mail


def v_home(req):
    if req.session.get('username'):
        try:
            #return render_to_response("dashboard.html",context_instance=RequestContext(req))
            return HttpResponseRedirect(URL_PREFIX+'/chapter_and_topics/')#home of App
        except:
            return HttpResponseRedirect(URL_PREFIX+'/login/')#home of App
    return HttpResponseRedirect(URL_PREFIX+'/login/')#home of App

def v_login(req):
    
    if req.session.get('username'):
        try:
            return HttpResponseRedirect(URL_PREFIX+'/')#home of App
        except:
            pass    
        
    if req.POST.get('login_click'):
        errors=[]
        _user=None
        username=req.POST.get('username','').strip()
        password=req.POST.get('password','').strip()
        if len(username)==0:
            errors.append("Please enter username !")
        elif len(password)==0:
            errors.append("Please enter password !")
        try:
            _user=tbl_user.objects.get(username=username,password=password,isActive=True)
        except tbl_user.DoesNotExist:
            if not errors:
                errors.append("Invalid Username Or Password !")
        
        if not errors:
            req.session['username']=_user.username
            return HttpResponseRedirect(URL_PREFIX+'/')
        return render_to_response("login.html",locals())
    return render_to_response('login.html',locals())


def v_logout(req):
    try:
        del req.session['username']
        return HttpResponseRedirect(URL_PREFIX+'/login/')#home of App
    except:
        return HttpResponseRedirect(URL_PREFIX+'/')#home of App
    
    

def v_forgotPassword(req):
    
    if req.session.get('username'):
        try:
            return HttpResponseRedirect(URL_PREFIX+'/')#home of App
        except:
            pass    
    
    if req.method=='POST':
        errors=[]
        employee=None
        email=req.POST.get('email','').strip()
        if len(email)==0:
            errors.append("Please enter a email address !")
        elif '@' not in email:
            errors.append("Please enter a valid email address !")
        else:
            try:
                employee=tbl_user.objects.get(email=email)
            except:
                errors.append("We have no user with this email Id !")
            
        if not errors:
            msg="\nHi "+employee.username+",\n\nYour Forgotten Password is inside '()' :("+employee.password+")\n\nThanks,\nNovus Team"
            send_mail('Novus',msg,EMAIL_HOST_USER,[email])
            return render_to_response('forgotPassword.html',{'messages':['successfully done,check your mail.']})
        return render_to_response('forgotPassword.html',locals())
        
    return render_to_response('forgotPassword.html')


def hasAccess(req):
    try:
        tbl_user.objects.get(username=req.session['username'],isActive=True)
        return True
    except:
        return False
    
    