from django.shortcuts import render_to_response
from views.authenticate import hasAccess
from django.http.response import HttpResponseRedirect, HttpResponse
from E_LEARN.settings import URL_PREFIX
from App.models import tbl_chapter, tbl_subject
from django.template.context import RequestContext
from views.tool import i_invalidFieldException, i_validateField


def v_list_chapter(req):
    if hasAccess(req):
        messages=[]
        subjects=tbl_subject.objects.filter(isActive=True)
        #s=tbl_subject.objects.all()
#         if not subjects:
#             messages.append("subjects haven't been defined yet, to create click on create subject button.")
        return render_to_response("chapter/list_chapter.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access

  
def v_add_chapter(req):
    if hasAccess(req):
        errors=[]
        messages=[]
        
        subjects=tbl_subject.objects.filter(isActive=True)
        if not subjects:
            messages.append("subjects either in-active or haven't been defined yet .")
        if req.method=='POST':
            #return HttpResponse(req.POST.get('belong_to_subject','-1'))
            belong_to_subject=int(req.POST.get('belong_to_subject','-1'))
            chapter_name=req.POST.get('chapter_name').strip()
            chapter_desc=req.POST.get('chapter_desc').strip()
            
            if belong_to_subject<1:
                errors.append('please select atleast one subject .')
            elif tbl_subject.objects.get(id=belong_to_subject).chapters.filter(name=chapter_name):
                errors.append('chapter with this title is already exist .')
            else:
                try:
                    c=tbl_chapter(
                               precedence=(tbl_chapter.objects.count()+1),
                               name=i_validateField(chapter_name,'s',"chapter title"),
                               detail=i_validateField(chapter_desc,'s',"chapter description",required=False),
                               )
                    c.save()
                    tbl_subject.objects.get(id=belong_to_subject).chapters.add(c)
                    req.session['success_messages']=['chapter successfully created !']
                    return HttpResponseRedirect(URL_PREFIX+"/chapter/")
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
        return render_to_response("chapter/add_chapter.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
  
  
def v_edit_chapter(req,chapter_id):
    if hasAccess(req):
        errors=[]
        subjects=tbl_subject.objects.filter(isActive=True)
        chapter=tbl_chapter.objects.get(id=chapter_id)
                     
        belong_to_subject=chapter.tbl_subject_set.get().id
        chapter_name=chapter.name
        chapter_desc=chapter.detail
            
        if req.method=='POST':
            belong_to_subject=int(req.POST.get('belong_to_subject','-1'))
            chapter_name=req.POST.get('chapter_name').strip()
            chapter_desc=req.POST.get('chapter_desc').strip()
                
            if belong_to_subject<1:
                errors.append('please select atleast one subject .')
            else:
                try:
                    if tbl_subject.objects.get(id=chapter.tbl_subject_set.get().id).chapters.get(name=chapter_name).name!=chapter.name:
                        errors.append('chapter with this name is already exist .')
                except:
                    pass
                
            
            if not errors:
                try:
                    chapter.name=i_validateField(chapter_name,'s',"chapter name")
                    chapter.detail=i_validateField(chapter_desc,'s',"chapter description",required=False)
                    
                    tbl_subject.objects.get(id=chapter.tbl_subject_set.get().id).chapters.remove(chapter)
                    
                    chapter.save()
                    
                    tbl_subject.objects.get(id=belong_to_subject).chapters.add(chapter)
                    
                    req.session['success_messages']=['subject successfully updated !']
                    return HttpResponseRedirect(URL_PREFIX+"/chapter/")
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
        return render_to_response("chapter/edit_chapter.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
   
   

# chapter=tbl_chapter.objects.get(id=2)
# print chapter.tbl_subject_set.get().id
