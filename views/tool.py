from E_LEARN.settings import AES_KEY, MEDIA_ROOT


def i_encrypt(msg):
    '''
    encrypted message contain text has non readable ch
    
    aracter set which not all platform support  
    '''
    from Crypto.Cipher import AES
    obj = AES.new(AES_KEY,AES.MODE_CBC, 'This is an IV456')
    return ''.join(map(lambda x:hex(ord(x)),obj.encrypt(i_fillBy_16(msg))))


def i_decrypt(cipher):
    
    from Crypto.Cipher import AES
    obj = AES.new(AES_KEY, AES.MODE_CBC, 'This is an IV456')
    cipher=''.join(map(lambda x:chr(x),i_hex2Decimal(cipher)))
    return obj.decrypt(cipher).strip()


def i_fillBy_16(msg):
    '''
    make an string multiple of length 16 ,by multiplying it with space ' ' 
    '''
    msg=msg.strip()
    l=len(msg)
    if (l%16):
        if l<16:
            msg=msg+' '*(16-l)
            return msg
        else:
            msg=msg+(16-(l%16))*' '
            return msg
    else:
        return msg

def i_hex2Decimal(hex_msg):
    ls=hex_msg.split('0x')[1:]
    return map(lambda h:int('0x'+h,16),ls)







class i_invalidFieldException(Exception):
    def __init__(self,value,msg,override):
        self.value=value
        self.msg=msg
        self.overirde=override
    def error_msg(self):
        if self.overirde and self.msg:
            return self.msg
        else:
            return "Invalid value found '"+str(self.value)+"' for '"+self.msg+"' !"
            
            
def i_validateField(value,mark,msg,override=False,required=True,options={}):
    
    '''
    NOTE : calling this method must be safe by catching i_invalidFieldException
    
    override used to customize default error message bydefault is normal 
    override =false means normal
    override =true means override whole message
    
    mark has values for different data type
    string          's'
    integer/number  'n'
    boolean         'b'
    date            'd'
    excel date      'xld' (excel store date as float type,so 'value' must be float) NOTE:workbook mode assumed as 0

    '''
    if mark=='s':
        if required and not value:
            raise i_invalidFieldException('',msg+" can not be empty !",True)
        else:
            return str(value)
        
    elif mark=='n':
        if required and not value:
            raise i_invalidFieldException('',msg+" can not be empty !",True)
        elif not required and not value:
            return None
        else:
            try:
                return int(value)
            except ValueError:
                raise i_invalidFieldException(value,msg,override)
    elif mark=='b':
        if required and value=='':
            raise i_invalidFieldException('',msg+" can not be empty !",True)
        elif not required and not value:
            return None
        else:
            try:
                return bool(value)
            except ValueError:
                raise i_invalidFieldException(value,msg,override)
#     elif mark=='xld':
#         if required and not value:
#             raise i_invalidFieldException('',msg+" can not be empty !",True)
#         elif not required and not value:
#             return None
#         else:
#             try:
#                 import datetime
#                 tpl=xlrd.xldate_as_tuple(value,0)
#                 return datetime.datetime(tpl[0],tpl[1],tpl[2])
#                 #return tpl
#             except ValueError:
#                 raise i_invalidFieldException(value,msg,override)
#     
    elif mark=='opt':
        if required and not value:
            raise i_invalidFieldException('',msg+" can not be empty !",True)
        elif not required and not value:
            return value
        else:
            try:
                return options[value]
            except KeyError:
                raise i_invalidFieldException(value,msg,override)
    elif mark=='e':
        if required and not value:
            raise i_invalidFieldException('',msg+" can not be empty !",True)
        elif not required and not value:
            return value
        else:
            if '@' not in value:
                raise i_invalidFieldException(value,msg,override)
            else:
                return value
#     elif mark=='city':
#         try:
#             return tbl_location.objects.filter(name__icontains=str(value))[0]
#         except tbl_location.DoesNotExist:
#             raise i_invalidFieldException(value,msg,override)
    
    else:
        raise i_invalidFieldException('',"Undefined 'Mark' argument '"+mark+"' in validation for value '"+str(value)+"'",True)
  




def upload(file_,subDirectory,name):
    import os
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+str(name), 'w') as destination:
            for chunk in file_.chunks():
                destination.write(chunk)
        return MEDIA_ROOT+subDirectory+'/'+name
    except IOError:
        if not os.path.exists(MEDIA_ROOT+subDirectory):
            os.makedirs(MEDIA_ROOT+subDirectory)
        with open(MEDIA_ROOT+subDirectory+'/'+str(name), 'w') as destination:
            for chunk in file_.chunks():
                destination.write(chunk)
        return MEDIA_ROOT+subDirectory+'/'+name

 
