from django.shortcuts import render_to_response
from django.template.context import RequestContext
from App.models import tbl_chapter, tbl_topic, tbl_media
from views.authenticate import hasAccess
from django.http.response import HttpResponseRedirect, HttpResponse
from E_LEARN.settings import URL_PREFIX
from views.tool import i_invalidFieldException, i_validateField, upload

def v_list_chapter_and_topics(req):
    if hasAccess(req):
        messages=[]
        chapters=tbl_chapter.objects.all()
        return render_to_response("chapter_and_topics/list_chapter_and_topics.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access 

def v_add_chapter_and_topics(req):
    
    if hasAccess(req):
        errors=[]
        messages=[]
        messages.append('NOTE : topic rows without topic no. will be ignored.')
        chapter_precedence=tbl_chapter.objects.count()+1
        topics=[[x,x,'',None]  for x in range(1,11)]
        
        if req.method=='POST':
            messages=[]
            #return HttpResponse(req.POST.get('last_topic','sasd'))
            try:
                try:
                    chapter_precedence=req.POST.get('chapter_precedence').strip()
                    chapter_name=req.POST.get('chapter_name').strip()
                    #chapter_logo=req.FILES.get('chapter_logo',None)
                    
                    chapter_precedence=i_validateField(chapter_precedence,'n',"chapter no")
                    chapter_name=i_validateField(chapter_name,'s',"chapter name")
                    
                    
                    if tbl_chapter.objects.filter(name=chapter_name):
                        errors.append('chapter name already used .')
                
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
                    topics=[[x,x,'',None]  for x in range(1,int(req.POST.get('last_topic'))+1)]    
                
                topics=[]
                for x in range(1,int(req.POST.get('last_topic'))+1):
                    try:
                        temp=[]
                        temp.append(x)
                        if req.POST.get('topic_'+str(x)+'_no',''):
                            temp.append(i_validateField(req.POST.get('topic_'+str(x)+'_no',''),'n',"topic no for row "+str(x)))
                            temp.append(i_validateField(req.POST.get('topic_'+str(x)+'_name',''),'s',"topic name for row "+str(x)))
                            if not 'topic_'+str(x)+'_file' in req.FILES:errors.append('please choose a file for row no. '+str(x)+' .')
                        else:
                            temp.append('')
                            temp.append('')
                        topics.append(temp)
                    except i_invalidFieldException,e:
                        topics.append(temp)
                        errors.append(e.error_msg)
                
                if 'chapter_logo' not in req.FILES:
                    errors.append('please choose a logo for chapter .')
                 
                if not errors:
                    c=tbl_chapter.objects.create(
                                               precedence=chapter_precedence,
                                               name=chapter_name,
                                               logo=upload(req.FILES['chapter_logo'],'logos',chapter_name+'_logo.jpg')
                                               )
                    
                    for id,no,name in topics:
                        if no!='' and name!='':
                            t=tbl_topic.objects.create(
                                                       precedence=no,
                                                       name=name
                                                       )
                            tbl_media.objects.create(
                                                     title=chapter_name+"_"+name,
                                                     belongsTo=t,
                                                     file=upload(req.FILES['topic_'+str(id)+'_file'],'videos',chapter_name+"_"+name)
                                                     )
                            c.topics.add(t)
                            
                            
                    
                    req.session['success_messages']=['successfully created .']
                    return HttpResponseRedirect(URL_PREFIX+"/chapter_and_topics/")        
                        
                        
               
            except i_invalidFieldException,e:
                errors.append(e.error_msg)
                topics=[[x,x,'',None]  for x in range(1,int(req.POST.get('last_topic'))+1)]
        
        return render_to_response("chapter_and_topics/add_chapter_and_topics.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access





def v_edit_chapter_and_topics(req,chapter_id):
    if hasAccess(req):
        messages=['''NOTE : leave topic no. blank to ignore (or) delete that topic row .''']
        chapter=tbl_chapter.objects.get(id=chapter_id)
        chapter_name=chapter.name
        chapter_precedence=chapter.precedence
        '''format [index,id,no,name,consider this row]'''
        topics=[[i+1,t.id,t.precedence,t.name,True] for i,t in enumerate(chapter.topics.all())]
        #topics.append([chapter.topics.count()+1,chapter.topics.count()+1,chapter.topics.count()+1,'',False])#default row on page
        
        if req.method=="POST":
            errors=[]
            messages=[]
            try:
                chapter_precedence=req.POST.get('chapter_precedence').strip()
                chapter_name=req.POST.get('chapter_name').strip()
                #chapter_logo=req.FILES.get('chapter_logo',None)
                
                chapter_precedence=i_validateField(chapter_precedence,'n',"chapter no")
                chapter_name=i_validateField(chapter_name,'s',"chapter name")
                try:
                    if tbl_chapter.objects.get(name=chapter_name).name!=chapter.name:
                        errors.append('chapter with this name is already exist.')
                except:
                    pass
            except i_invalidFieldException,e:
                errors.append(e.error_msg)
            
            '''hold on [index,id,no,name,consider this row]'''
            topics=[[index,req.POST.get('topic_'+str(index)+'_id','-1'),req.POST.get('topic_'+str(index)+'_no','').strip(),req.POST.get('topic_'+str(index)+'_name','').strip(),True] for index in range(1,int(req.POST.get('last_topic'))+1)]
            '''end'''
            
            '''validate and clean'''
            for i,t in enumerate(topics):
                try:
                    #index (no changed required)
                    topics[i][1]=int(t[1])
                    if t[2]:
                        topics[i][2]=i_validateField(t[2],'n',"topic no for row "+str(i+1),required=False)
                        topics[i][3]=i_validateField(t[3],'s',"topic name for row "+str(i+1))
                        if t[1]==-1:
                            if 'topic_'+str(i+1)+'_file' not in req.FILES:
                                errors.append('please choose a file for row '+str(i+1)+' .')
                    else:
                        #mark a row is no longer needed/and should be deleted
                        topics[i][3]=''
                        topics[i][4]=False
                        
                except i_invalidFieldException,e:
                    errors.append(e.error_msg)
            '''end'''
                    
            if not errors:
                #return HttpResponse(repr(topics))
            
                chapter.name=chapter_name
                chapter.precedence=chapter_precedence
                if 'chapter_logo' in req.FILES:
                    chapter.logo=upload(req.FILES['chapter_logo'],'logos',chapter_name+'_logo.jpg')
                chapter.topics=[]
                chapter.save()
                
                for index,tid,no,name,consider in topics:
                    if consider and tid>0:#old topic modified
                        catched_topic=tbl_topic.objects.get(id=tid)
                        catched_topic.precedence=no
                        catched_topic.name=name
                        if 'topic_'+str(index)+'_file' in req.FILES:
                            tbl_media.objects.get(belongsTo=catched_topic).file=upload(req.FILES['topic_'+str(index)+'_file'],'videos',chapter_name+"_"+name)
                        catched_topic.save()
                        chapter.topics.add(catched_topic)
                    if consider and tid==-1:#new topic added
                        new_topic=tbl_topic.objects.create(
                                                   precedence=no,
                                                   name=name
                                                   )
                        tbl_media.objects.create(
                                                 title=chapter_name+"_"+name,
                                                 belongsTo=new_topic,
                                                 file=upload(req.FILES['topic_'+str(index)+'_file'],'videos',chapter_name+"_"+name)
                                                 )
                        chapter.topics.add(new_topic)
                    if not consider and tid>0:#old topic deleted
                        tbl_topic.objects.get(id=tid).delete()
                chapter.save()
                req.session['success_messages']=['successfully updated .']
                return HttpResponseRedirect(URL_PREFIX+"/chapter_and_topics/")    
                
                
                    
        return render_to_response("chapter_and_topics/edit_chapter_and_topics.html",locals(),context_instance=RequestContext(req))
    return HttpResponseRedirect(URL_PREFIX+"/")#unauthorized access
    











 #             elif tbl_chapter.objects.get(id=belong_to_subject).chapters.filter(name=chapter_name):
    #                 errors.append('chapter with this title is already exist .')
    #             else:
    #                 try:
    #                     c=tbl_chapter(
    #                                precedence=(tbl_chapter.objects.count()+1),
    #                                name=i_validateField(chapter_name,'s',"chapter title"),
    #                                detail=i_validateField(chapter_desc,'s',"chapter description",required=False),
    #                                )
    #                     c.save()
    #                     tbl_subject.objects.get(id=belong_to_subject).chapters.add(c)
    #                     req.session['success_messages']=['chapter successfully created !']
    #                     return HttpResponseRedirect(URL_PREFIX+"/chapter/")
    #                 except i_invalidFieldException,e:
    #                     errors.append(e.error_msg)

