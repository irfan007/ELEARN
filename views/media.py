
from wsgiref.util import FileWrapper
from views.tool import i_decrypt
from django.http.response import HttpResponse
from App.models import tbl_media

def v_serve(req,media_id):
    #return HttpResponse(req.GET.get('media_id'))
    #if req.method=="POST":
        try:
            _file = FileWrapper(tbl_media.objects.get(id=media_id).file)
            response = HttpResponse(_file, content_type='video/webm')
            #response['Content-Disposition'] = ' filename=test.mp4'
            return response
        except Exception,e:
            return HttpResponse(str(e))
    #return HttpResponse('denied')
    
def v_decrypt(req):
    #return HttpResponse(req.GET.get('this',''))
    try:
        return HttpResponse(i_decrypt(req.GET.get('this','')))
    except:
        return HttpResponse('access denied !')


#  
# x=i_encrypt('http://localhost:8000/media/1235/63546.webm')
# print x
# print i_decrypt(x)

