from django.db import models
from user.models import User
from will.models import Will
from task.models import Task

# Create your models here.
class Deal(models.Model):
    build_time = models.DateTimeField()
    status = models.IntegerField(default=0) # 1 => completed
    helper = models.ForeignKey(User, related_name = 'helporder')
    needer = models.ForeignKey(User, related_name = 'needorder')
    task = models.ForeignKey(Task, related_name = 'order', null = True)

    def to_dict(self):
        return dict(id=self.id, status=self.status, build_time=self.build_time,helper=self.helper, needer=self.needer,task=self.task)