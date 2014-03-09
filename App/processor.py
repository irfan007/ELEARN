from App.models import tbl_user
from E_LEARN.settings import URL_PREFIX


def share(req):
    try:
        return {'REQ':req,'URL_PREFIX':URL_PREFIX,'CU':tbl_user.objects.get(username=req.session['username'])}
    except:
        return {}