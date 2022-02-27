from django.contrib import admin
from .models import UserBase, Address

# Register your models here.

admin.site.register(UserBase)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "customer_id",
        "Account",
    )

    def Account(self, object):

        return UserBase.objects.get(id=object.customer_id)

    Account.short_description = "Account"
