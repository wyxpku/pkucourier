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
            pto = self.pto, code = self.code, fetch_btime = str(self.fetch_btime), fetch_etime = str(self.fetch_etime),
            build_time = str(self.build_time), give_time = str(self.give_time), info = self.info, owner = self.owner,
            status = self.status
        )
    # only return approximate information
    def ap_to_dict(self):
        return dict(
            id = self.id, approximate_fplace = self.approximate_fplace, pto = self.pto, fetch_btime = str(self.fetch_btime),
            fetch_etime = str(self.fetch_etime), build_time = str(self.build_time),
            give_time = str(self.give_time), info = self.info, owner = self.owner, status = self.status
        )
