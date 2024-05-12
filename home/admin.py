from django.contrib import admin

# Register your models here.
from .models import Aadhaar

admin.site.register(Aadhaar)

from .models import Aadhaar_detail

admin.site.register(Aadhaar_detail)