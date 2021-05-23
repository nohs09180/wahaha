from django.contrib import admin
from .models import Video, SmileData, SmileRate, SmileDosData, SmileDos

admin.site.register(Video)
admin.site.register(SmileData)
admin.site.register(SmileRate)
admin.site.register(SmileDosData)
admin.site.register(SmileDos)
