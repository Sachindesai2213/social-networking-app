from django.db import models
from users.models import User, BaseModel


# Create your models here.
class FriendRequest(BaseModel):
    to_user = models.ForeignKey(User, models.CASCADE,
                                related_name='friendrequests')
    from_user = models.ForeignKey(User, models.CASCADE,
                                  related_name='%(class)s_from_user')
    status = models.CharField(max_length=1, null=True)


class Friend(BaseModel):
    user = models.ForeignKey(User, models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, models.CASCADE,
                               related_name='%(class)s_friend')
