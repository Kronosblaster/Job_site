from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# ------------------------------------------------------------------------------------------------------------------------
#                             Admin User Creation Form
# ------------------------------------------------------------------------------------------------------------------------
class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'username')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['pw'])
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['f_name']
        user.last_name = self.cleaned_data['l_name']
        user.is_staff = True


        print
        "form valid, saving to db"

        if commit:
            user.save()

        return user
