from django.shortcuts import render_to_response
from views.authenticate import hasAccess
from django.http.response import HttpResponseRedirect
from E_LEARN.settings import URL_PREFIX
from App.models import tbl_course
from django.template.context import RequestContext
from views.tool import i_invalidFieldException, i_validateField


def v_list_course(req):
    if hasAccess(req):
        messages=[]
        courses=tbl_course.objects.all()
        if not courses:
            messages.append("courses haven't been defined yet, to create click on create course button.")
        return render_to_response("course/list_course.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access


def v_add_course(req):
    if hasAccess(req):
        errors=[]
        if req.method=='POST':
            course_code=req.POST.get('course_code').strip()
            course_name=req.POST.get('course_name').strip()
            course_desc=req.POST.get('course_desc').strip()
            course_status=int(req.POST.get('course_status',''))
            
            
            if tbl_course.objects.filter(code=course_code):
                errors.append('course with this code is already exist .')
            elif tbl_course.objects.filter(name=course_name):
                errors.append('course with this name is already exist .')
            else:
                try:
                    c=tbl_course(
                               code=i_validateField(course_code,'s',"course code"),
                               name=i_validateField(course_name,'s',"course name"),
                               detail=i_validateField(course_desc,'s',"course description",required=False),
                               isActive=i_validateField(course_status,'b',"course status")
                               )
                    c.save()
                    req.session['success_messages']=['course successfully created !']
                    return HttpResponseRedirect(URL_PREFIX+"/course/")
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
        return render_to_response("course/add_course.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access


def v_edit_course(req,course_id):
    if hasAccess(req):
        errors=[]
        course=tbl_course.objects.get(id=course_id)
        
        course_code=course.code
        course_name=course.name
        course_desc=course.detail
        course_status=int(course.isActive)
        
        if req.method=='POST':
            course_code=req.POST.get('course_code').strip()
            course_name=req.POST.get('course_name').strip()
            course_desc=req.POST.get('course_desc').strip()
            course_status=int(req.POST.get('course_status',''))
            
            try:
                if tbl_course.objects.get(code=course_code).code!=course.code:
                    errors.append('course with this code is already exist .')
            except:
                pass
            try:
                if tbl_course.objects.get(name=course_name).name!=course.name:
                    errors.append('course with this name is already exist .')
            except:
                pass
            
            if not errors:
                try:
                    course.code=i_validateField(course_code,'s',"course code")
                    course.name=i_validateField(course_name,'s',"course name")
                    course.detail=i_validateField(course_desc,'s',"course description",required=False)
                    course.isActive=i_validateField(course_status,'b',"course status")
                    course.save()
                    req.session['success_messages']=['course successfully updated !']
                    return HttpResponseRedirect(URL_PREFIX+"/course/")
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
        return render_to_response("course/edit_course.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access




