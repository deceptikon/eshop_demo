from django.contrib import admin
from . import models as m

class CartContentInline(admin.TabularInline):
    model = m.CartContent
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = (CartContentInline,)

admin.site.register(m.Product)
admin.site.register(m.Category)
admin.site.register(m.Cart, CartAdmin)
admin.site.register(m.CartContent)
admin.site.register(m.Order)

# Register your models here.
