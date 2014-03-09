from django.shortcuts import render_to_response
from views.authenticate import hasAccess
from django.http.response import HttpResponseRedirect
from E_LEARN.settings import URL_PREFIX
from App.models import tbl_subject, tbl_course
from django.template.context import RequestContext
from views.tool import i_invalidFieldException, i_validateField


def v_list_subject(req):
    if hasAccess(req):
        messages=[]
        courses=tbl_course.objects.filter(isActive=True)
#         if not courses:
#             messages.append("subjects haven't been defined yet, to create click on create subject button.")
        return render_to_response("subject/list_subject.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access

 
def v_add_subject(req):
    if hasAccess(req):
        errors=[]
        messages=[]
        courses=tbl_course.objects.filter(isActive=True)
        
        if not courses:
            messages.append("courses either in-active or haven't been defined yet .")
        if req.method=='POST':
            belong_to_course=int(req.POST.get('belong_to_course','-1'))
            subject_code=req.POST.get('subject_code').strip()
            subject_name=req.POST.get('subject_name').strip()
            subject_desc=req.POST.get('subject_desc').strip()
            subject_status=int(req.POST.get('subject_status',''))
             
            if belong_to_course<1:
                errors.append('please select atleast one course .')
            elif tbl_subject.objects.filter(code=subject_code):
                errors.append('subject with this code is already exist .')
            elif tbl_course.objects.get(id=belong_to_course).subjects.filter(name=subject_name):
                errors.append('subject with this name is already exist .')
            else:
                try:
                    s=tbl_subject(
                               code=i_validateField(subject_code,'s',"subject code"),
                               name=i_validateField(subject_name,'s',"subject name"),
                               detail=i_validateField(subject_desc,'s',"subject description",required=False),
                               isActive=i_validateField(subject_status,'b',"subject status")
                               )
                    s.save()
                    tbl_course.objects.get(id=belong_to_course).subjects.add(s)
                    req.session['success_messages']=['subject successfully created !']
                    return HttpResponseRedirect(URL_PREFIX+"/subject/")
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
        return render_to_response("subject/add_subject.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
 
 
def v_edit_subject(req,subject_id):
    if hasAccess(req):
        errors=[]
        courses=tbl_course.objects.filter(isActive=True)
        subject=tbl_subject.objects.get(id=subject_id)
         
        subject_code=subject.code
        subject_name=subject.name
        subject_desc=subject.detail
        subject_status=int(subject.isActive)
        belong_to_course=subject.tbl_course_set.get().id
         
        if req.method=='POST':
            subject_code=req.POST.get('subject_code').strip()
            subject_name=req.POST.get('subject_name').strip()
            subject_desc=req.POST.get('subject_desc').strip()
            subject_status=int(req.POST.get('subject_status',''))
            belong_to_course=int(req.POST.get('belong_to_course',''))
            
            if belong_to_course<1:
                errors.append('please select atleast one course .')
                
            try:
                if tbl_subject.objects.get(code=subject_code).code!=subject.code:
                    errors.append('subject with this code is already exist .')
            except:
                pass
            try:
                if subject.tbl_course_set.get().subjects.get(name=subject_name).name!=subject.name:
                    errors.append('subject with this name is already exist .')
            except:
                pass
             
            if not errors:
                try:
                    subject.code=i_validateField(subject_code,'s',"subject code")
                    subject.name=i_validateField(subject_name,'s',"subject name")
                    subject.detail=i_validateField(subject_desc,'s',"subject description",required=False)
                    subject.isActive=i_validateField(subject_status,'b',"subject status")
                    
                    subject.tbl_course_set.get().subjects.remove(subject)
                    
                    subject.save()
                    
                    tbl_course.objects.get(id=belong_to_course).subjects.add(subject)
                    
                    req.session['success_messages']=['subject successfully updated !']
                    return HttpResponseRedirect(URL_PREFIX+"/subject/")
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
        return render_to_response("subject/edit_subject.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
 
 


