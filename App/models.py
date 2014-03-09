from django.db import models
from datetime import datetime
from E_LEARN.settings import MEDIA_ROOT, URL_PREFIX
from views.tool import i_encrypt


class tbl_option(models.Model):
    title=models.CharField(null=True,max_length=100)
    
    
class tbl_question(models.Model):
    title=models.TextField(null=True)
    options=models.ManyToManyField(tbl_option,null=True,blank=True)
    answer=models.ForeignKey(tbl_option,null=True,blank=True,related_name='answer_field')


class tbl_topic(models.Model):
    '''
    defaults
    precedence=self.id (store manually)
    '''
       
    precedence=models.IntegerField(default=0)
    name=models.CharField(null=True,max_length=100)
    detail=models.TextField(null=True)
    
    questions=models.ManyToManyField(tbl_question,null=True,blank=True)
#     def save(self, *args, **kwargs):
#         super(tbl_section, self).save(*args, **kwargs)
#         self.precedence=self.id
    
    def hasFile(self):
        try:
            if tbl_media.objects.get(belongsTo=self.id):
                return True
        except tbl_media.DoesNotExist:
            return False
    
    def __unicode__(self):
        return '%s'%(self.id)        
            
    
class tbl_chapter(models.Model):
    '''
    defaults
    precedence=self.id (store manually)
    1) A student can appear multiple time for same exam for a chapter(if not qualified in first attempt) 
    '''
    precedence=models.IntegerField(default=0)
    name=models.CharField(null=True,max_length=100)
    detail=models.TextField(null=True)
    logo=models.FileField(upload_to=MEDIA_ROOT,null=True)
    
    topics=models.ManyToManyField(tbl_topic,null=True,blank=True)
    
    def __unicode__(self):
        return '%s'%(self.name)
    
    def logoName(self):
        import os
        return os.path.basename(self.logo.name)
#     def save(self, *args, **kwargs):
#         super(tbl_chapter, self).save(*args, **kwargs)
#         self.precedence=self.id


class tbl_subject(models.Model):
    code=models.CharField(null=True,max_length=100)
    name=models.CharField(null=True,max_length=100)
    detail=models.TextField(null=True)
    isActive=models.BooleanField(default=True)
    
    chapters=models.ManyToManyField(tbl_chapter,null=True,blank=True)
    
    def __unicode__(self):
        return '%s,%s'%(self.code,self.name)
    
     
class tbl_course(models.Model):
    code=models.CharField(null=True,max_length=100)
    name=models.CharField(null=True,max_length=100)
    detail=models.TextField(null=True)
    isActive=models.BooleanField(default=True)
    
    subjects=models.ManyToManyField(tbl_subject,null=True,blank=True)
    
    def __unicode__(self):
        return '%s,%s'%(self.code,self.name)
            


class tbl_media(models.Model):
    '''
    * each media belongs to a unique topic of a chapter
      belongsTo=tbl_topic (exam belongs to which topic)
    
    '''
    title=models.TextField(null=True)
    belongsTo=models.ForeignKey(tbl_topic,null=True,blank=True)
    file=models.FileField(upload_to=MEDIA_ROOT,null=True)
    
    def cipher_url(self):
        '''
        
        '''
        return i_encrypt(URL_PREFIX+'/media/'+str(self.id)+"/")
    

#________local to each student________________________________________________________________________________________________________

    
    


class tbl_registration(models.Model):
    username=models.CharField(null=True,max_length=50)
    password=models.CharField(null=True,max_length=50)
    
    fName=models.CharField(null=True,max_length=50)
    lName=models.CharField(null=True,max_length=50)
    contact=models.CharField(null=True,max_length=20)
    email=models.CharField(null=True,max_length=100)



class tbl_result(models.Model):
    '''
    defaults
    status=False(fail)
    marks=0
    '''
    status=models.BooleanField(default=False)
    marks=models.IntegerField(default=0)
    
    
class tbl_exam(models.Model):
    '''
    defaults
    total_questions=0
    correct_answers=0
    unanswered=0
    
    * one exam has only one result
    * each exam belongs to a unique topic
      
      belongsTo=tbl_topic
    '''
    belongsTo=models.ForeignKey(tbl_topic,null=True,blank=True)
    date=models.DateField(default=datetime.today())
    result=models.ForeignKey(tbl_result,null=True,blank=True)
    total_questions=models.IntegerField(default=0)
    correct_answers=models.IntegerField(default=0)
    unanswered=models.IntegerField(default=0)
    

class tbl_student(models.Model):
    '''
    default
    isActive=True
    1) A student can appear multiple time for same exam for a chapter(if not qualified in first attempt) 
    '''
    registration=models.ForeignKey(tbl_registration,null=True,blank=True)
    exams=models.ManyToManyField(tbl_exam,null=True,blank=True)    #1
    isActive=models.BooleanField(default=True)
    
    def progress(self):
        return " - - - - "
    
    
class tbl_device(models.Model):
    assigned_to=models.ForeignKey(tbl_student,null=True,blank=True)
    signature=models.TextField(null=True)
    isActive=models.BooleanField(default=False)
    
    def __unicode__(self):
        return "ID:%s ASSIGNED_TO_ID:%s"%(self.id,self.assigned_to.id)
#_________system user(administrator)_________________________________________________________________________________________________


class tbl_user(models.Model):
    class Meta:
        verbose_name="SYSTEM USER"
        verbose_name_plural="SYSTEM USER"
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    email=models.CharField(max_length=150)
    #role=models.ForeignKey(tbl_role,null=True,blank=True)
    #designation=models.CharField(max_length=100,null=True,blank=True)
    #department=models.ForeignKey(tbl_department,null=True,blank=True)
    #image=models.ImageField(upload_to=djangoUpload,null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    #isAdmin=models.BooleanField(default=False)
    isSuper=models.BooleanField(default=False)#super user is admin who's right can not be removed (only single super user exist for whole system),isSuper will hide admin from userlist and edit  
    createdOn=models.DateField(default=datetime.today())
    def __unicode__(self):
        return "ADMIN ID:%s"%(self.id)
#     def getImageURL(self):
#         if self.image:
#             return uploadFolder+self.image.url

