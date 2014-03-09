from django.contrib import admin
from App.models import tbl_registration, tbl_course, tbl_subject, tbl_topic,\
    tbl_student, tbl_chapter, tbl_exam, tbl_media, tbl_option, tbl_question,\
    tbl_result, tbl_user, tbl_device



admin.site.register(tbl_registration)
admin.site.register(tbl_student)
admin.site.register(tbl_course)
admin.site.register(tbl_subject)
admin.site.register(tbl_topic)
admin.site.register(tbl_chapter)
admin.site.register(tbl_exam)
admin.site.register(tbl_media)
admin.site.register(tbl_option)
admin.site.register(tbl_question)
admin.site.register(tbl_result)
admin.site.register(tbl_user)
admin.site.register(tbl_device)
                    
