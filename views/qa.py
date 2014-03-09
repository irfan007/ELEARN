from App.models import tbl_chapter, tbl_topic
from django.shortcuts import render_to_response
from django.template.context import RequestContext



def v_list_qa(req):
#     m1='''
#     Questions belong to topic of a chapter ,
#     to view or modify question go to that topic. 
#     '''
    messages=[]
    chapters=tbl_chapter.objects.all()
    return render_to_response("qa/list_qa.html",locals(),context_instance=RequestContext(req))

def v_add_qa(req):
    
    return render_to_response("qa/add_qa.html",locals(),context_instance=RequestContext(req))

def v_edit_qa(req,topic_id):
    topic=tbl_topic.objects.get(id=topic_id)
    return render_to_response("qa/edit_qa.html",locals(),context_instance=RequestContext(req))
    #return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
    

def v_upload_qa(req):
    
    return render_to_response("qa/upload_qa.html",locals(),context_instance=RequestContext(req))

