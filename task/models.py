from django.db import models
from user.models import User

# Create your models here.
class Task(models.Model):
    approximate_fplace = models.CharField(max_length = 50)
    detailed_fplace = models.CharField(max_length = 50)
    pto = models.CharField(max_length = 50)
    code = models.CharField(max_length = 50)
    fetch_btime = models.DateTimeField()
    fetch_etime = models.DateTimeField()
    build_time = models.DateTimeField()
    give_time = models.DateTimeField()
    info = models.CharField(max_length = 200)
    owner = models.ForeignKey(User, related_name = 'task')
    status = models.IntegerField(default = 0) # 0:未接, 1:已解

    def to_dict(self):
        return dict(
            id = self.id, approximate_fplace = self.approximate_fplace, detailed_fplace = self.detailed_fplace,
            pto = self.pto, code = self.code, info = self.info, owner = self.owner,status = self.status,
            fetch_btime = self.fetch_btime.strftime('%Y-%m-%d %H:%M:%S'),
            fetch_etime = self.fetch_etime.strftime('%Y-%m-%d %H:%M:%S'),
            build_time = self.build_time.strftime('%Y-%m-%d %H:%M:%S'),
            give_time = self.give_time.strftime('%Y-%m-%d %H:%M:%S')
        )

    # only return approximate information
    def ap_to_dict(self):
        return dict(
            id = self.id, approximate_fplace = self.approximate_fplace, pto = self.pto,
            info = self.info, owner = self.owner, status = self.status,
            fetch_btime = self.fetch_btime.strftime('%Y-%m-%d %H:%M:%S'),
            fetch_etime = self.fetch_etime.strftime('%Y-%m-%d %H:%M:%S'),
            build_time = self.build_time.strftime('%Y-%m-%d %H:%M:%S'),
            give_time = self.give_time.strftime('%Y-%m-%d %H:%M:%S')
        )
