from django.db import models
from user.models import User

# Create your models here.
class Will(models.Model):
    pfrom = models.CharField(max_length = 50)
    pto = models.CharField(max_length = 50)
    info = models.CharField(max_length = 50)
    build_time = models.DateTimeField()
    owner = models.ForeignKey(User, related_name = 'will')
    status = models.IntegerField(default=0) # 0->Opened, 1->Closed
    def to_dict(self):
        return dict(
            id = self.id, pfrom = self.pfrom, pto = self.pto, info = self.info,
            build_time = self.build_time.strftime('%Y-%m-%d %H:%M:%S'), owner = self.owner
        )

