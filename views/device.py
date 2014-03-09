from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_device, tbl_student
from django.http.response import HttpResponseRedirect
from E_LEARN.settings import URL_PREFIX
from views.authenticate import hasAccess
from views.tool import i_validateField, i_invalidFieldException


#print tbl_student.tbl_device_set
    

def v_list_device(req):
    if hasAccess(req):
        messages=[]
        devices=tbl_device.objects.all()
        return render_to_response("device/list_device.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
    
def v_add_device(req):
    if hasAccess(req):
        device_id=tbl_device.objects.last().id+1
        if req.method=="POST":
            errors=[]
            
            signature=req.POST.get('signature','').strip()
            assigned_to=req.POST.get('assigned_to','').strip()
            status=int(req.POST.get('status','0'))
            
            try:
                signature=i_validateField(signature,'s',msg="signature")
                assigned_to=i_validateField(assigned_to,'n',msg="assigned to")
            except i_invalidFieldException,e:
                errors.append(e.error_msg)
            
            if not errors:
                try:
                    if not tbl_student.objects.filter(id=assigned_to):
                        errors.append("Invalid assigned to id .")
                    if tbl_device.objects.filter(assigned_to=assigned_to):
                        errors.append("device has already been assigned to student.")
                        
                except tbl_student.DoesNotExist:
                    pass
            
            if not errors:
                tbl_device.objects.create(
                                          assigned_to=tbl_student.objects.get(id=assigned_to),
                                          signature=signature,
                                          isActive=status
                                          )
                
                req.session['success_messages']=['successfully created .']
                return HttpResponseRedirect(URL_PREFIX+"/device/")
            
        return render_to_response("device/add_device.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
    
def v_edit_device(req,device_id):
    if hasAccess(req):
        editing_device=tbl_device.objects.get(id=device_id)
        
        signature=editing_device.signature
        assigned_to=editing_device.assigned_to.id
        status=int(editing_device.isActive)
        
        if req.method=="POST":
            errors=[]
            
            signature=req.POST.get('signature','').strip()
            assigned_to=req.POST.get('assigned_to','').strip()
            status=int(req.POST.get('status','0'))
            
            try:
                signature=i_validateField(signature,'s',msg="signature")
                assigned_to=i_validateField(assigned_to,'n',msg="assigned to")
            except i_invalidFieldException,e:
                errors.append(e.error_msg)
            
            if not errors:
                try:
                    if not tbl_student.objects.filter(id=assigned_to):
                        errors.append("Invalid assigned to id .")
                    if tbl_device.objects.filter(assigned_to=assigned_to)[0].id!=editing_device.id:
                        errors.append("device has already been assigned to student.")
                        
                except :
                    pass
            
            if not errors:
                editing_device.signature=signature
                editing_device.assigned_to=tbl_student.objects.get(id=assigned_to)
                editing_device.isActive=status
                editing_device.save()
                
                req.session['success_messages']=['successfully updated .']
                return HttpResponseRedirect(URL_PREFIX+"/device/")
            
        return render_to_response("device/edit_device.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
    

def v_upload_device(req):
    return render_to_response("device/upload_device.html",locals(),context_instance=RequestContext(req))