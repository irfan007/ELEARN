from App.models import tbl_student, tbl_registration
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from views.authenticate import hasAccess
from django.http.response import HttpResponseRedirect
from E_LEARN.settings import URL_PREFIX
from views.tool import i_invalidFieldException, i_validateField

def v_list_student(req):
    if hasAccess(req):
        messages=[]
        students=tbl_student.objects.all()
        return render_to_response("student/list_student.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access


def v_add_student(req):
    if hasAccess(req):
        errors=[]
        messages=[]
        if req.method=="POST":
            student_username=req.POST.get('student_username','').strip()
            student_password=req.POST.get('student_password','').strip()
            student_fname=req.POST.get('student_fname','').strip()
            student_lname=req.POST.get('student_lname','').strip()
            student_contact=req.POST.get('student_contact','').strip()
            student_email=req.POST.get('student_email','').strip()
            student_status=int(req.POST.get('student_status','1'))
            
            try:
                student_username=i_validateField(student_username,'s',msg="username")
                student_password=i_validateField(student_password,'s',msg="password")
                student_fname=i_validateField(student_fname,'s',msg="first name")
                student_lname=i_validateField(student_lname,'s',msg="lirst name")
                student_contact=i_validateField(student_contact,'n',msg="contact")
                student_email=i_validateField(student_email,'e',msg="email")
            except i_invalidFieldException,e:
                errors.append(e.error_msg)
            
            if not errors:
                if tbl_registration.objects.filter(username=student_username):
                    errors.append('username already exist .')
                    
            if not errors:
                r=tbl_registration.objects.create(
                                               username=student_username,
                                               password=student_password,
                                               fName=student_fname,
                                               lName=student_lname,
                                               contact=student_contact,
                                               email=student_email
                                               )
                    
                tbl_student.objects.create(
                                           registration=r,
                                           isActive=student_status
                                           )
                    
                req.session['success_messages']=['successfully created .']
                return HttpResponseRedirect(URL_PREFIX+"/student/")
        return render_to_response("student/add_student.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
    
    
def v_edit_student(req,student_id):
    if hasAccess(req):
        errors=[]
        messages=[]
        student=tbl_student.objects.get(id=student_id)
        
        student_username=student.registration.username
        student_password=student.registration.password
        student_fname=student.registration.fName
        student_lname=student.registration.lName
        student_contact=student.registration.contact
        student_email=student.registration.email
        student_status=int(student.isActive)
        
        if req.method=="POST":
            student_username=req.POST.get('student_username','').strip()
            student_password=req.POST.get('student_password','').strip()
            student_fname=req.POST.get('student_fname','').strip()
            student_lname=req.POST.get('student_lname','').strip()
            student_contact=req.POST.get('student_contact','').strip()
            student_email=req.POST.get('student_email','').strip()
            student_status=int(req.POST.get('student_status','1'))
            
            try:
                student_username=i_validateField(student_username,'s',msg="username")
                student_password=i_validateField(student_password,'s',msg="password")
                student_fname=i_validateField(student_fname,'s',msg="first name")
                student_lname=i_validateField(student_lname,'s',msg="lirst name")
                student_contact=i_validateField(student_contact,'n',msg="contact")
                student_email=i_validateField(student_email,'e',msg="email")
            except i_invalidFieldException,e:
                errors.append(e.error_msg)
            
            if not errors:
                try:
                    if tbl_registration.objects.get(username=student_username).username!=student.registration.username:
                        errors.append('username already exist .')
                except tbl_registration.DoesNotExist:
                    pass
            
            if not errors:
                student.registration.username=student_username
                student.registration.password=student_password
                student.registration.fName=student_fname
                student.registration.lName=student_lname
                student.registration.contact=student_contact
                student.registration.email=student_email
                student.isActive=int(student_status)
                req.session['success_messages']=['successfully updated .']
                
                student.registration.save()
                student.save()
                return HttpResponseRedirect(URL_PREFIX+"/student/")
            
    return render_to_response("student/edit_student.html",locals(),context_instance=RequestContext(req))
    