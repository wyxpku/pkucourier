from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    status = models.IntegerField(default = 0) # authened or not, default 0, authened 1
    signup_time = models.DateTimeField()
    avatar = models.IntegerField()
    bonus = models.IntegerField(default = 10)
    hx_username = models.CharField(max_length = 50, null = True)
    hx_password = models.CharField(max_length = 50, null = True)

    def to_dict(self):
        return dict(
            uid = self.id, name = self.name, email = self.email, status = self.status, avatar = self.avatar,
            signup_time = self.signup_time.strftime('%Y-%m-%d %H:%M:%S'),
            bonus = self.bonus, hx_username = self.hx_username, hx_password = self.hx_password
        )
