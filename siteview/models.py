from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class SlideShow(models.Model):
    title = models.CharField(_('title'),max_length=128)
    subtitle = models.CharField(_('subtitle'),max_length=256)
    image = models.ImageField(_('Background'),upload_to='SlideShow/Category/image')
    action_text = models.CharField(_('action text'),max_length=128,default='shop now')
    action_url  = models.URLField(_('action url'),default='http://127.0.0.1:8000')



    def __str__(self):
        return self.title
