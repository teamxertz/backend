from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, Group
from .models import User, Patient, Doctor, Hospital, Address, PatientData
from .forms import UserAdminChangeForm, UserAdminCreationForm, PatientAdminChangeForm, PatientAdminCreationForm
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','type', 'admin')
    list_filter = ('type',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ()}),
        #('Permissions', {'fields': ('admin','type')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'type')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('type',)
        return self.readonly_fields

class AddressInline(admin.StackedInline):
    model= Address
    max_num=1
    verbose_name_plural = "Address"

class PatientInline(admin.StackedInline):
    model = PatientData
    max_num=1
    verbose_name_plural = "Patient Data"
   


class PatientAdmin(BaseUserAdmin):
    form = PatientAdminChangeForm
    add_form = PatientAdminCreationForm
    #model = Patient
    inlines = (PatientInline,AddressInline)
    list_display = ('email','type',)
    list_filter = ('type',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password','active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    
    
    

# Adding Our Models
admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor)
#admin.site.register(Address)
admin.site.register(Hospital)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)



# Customzation
admin.site.site_header = "Xertz Admin"
admin.site.site_title = "Xertz Admin Portal"
admin.site.index_title = "Welcome to Xertz Portal"