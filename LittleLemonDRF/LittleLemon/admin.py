from django.contrib import admin
from . import models
# admin
# admin@littlelemon.co
# lemonade123@


# manager
# username johndoe
# doer135!

# user
# jotarokujo
# jotaroPassword

# valkyrja
# valk123456789


# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.MenuItem)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
