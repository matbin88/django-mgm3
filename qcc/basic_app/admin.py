from django.contrib import admin
#from basic_app.models import UserProfileInfo,Subject,Topic,Video,Frame,Question,Option,Answer
from basic_app.models import UserProfileInfo,Subject,Topic,Video,Frame,Question,Option, Test, TestResult
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Video)
admin.site.register(Frame)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Test)
admin.site.register(TestResult)
#admin.site.register(Answer)
