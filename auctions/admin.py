from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(listing)
admin.site.register(comments)
admin.site.register(bids)
admin.site.register(watch_list)
