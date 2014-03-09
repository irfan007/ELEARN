from django.shortcuts import render_to_response
from App.models import tbl_media, tbl_chapter



    

def v_test(req):
    medias=tbl_media.objects.all()
    return render_to_response('page.html',locals())

# for t in tbl_chapter.objects.get(id=1).topics.all():
#     print t.id


