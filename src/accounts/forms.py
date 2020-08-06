from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

from.models import EmailActivation, GuestEmail

class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('register')
            msg = """This email does not exist.Would you like to <a href="{link}">Register</a>?""".format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Userfields = ('full name', 'email')


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords failed to match')

        return password2

class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label = 'Name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    class Meta:
        model = User
        fields = ['Full-name']

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('Full_name', 'email', 'password', 'is_active', 'admin')

        def clean_password(self):
            return self.initial['password']


class GuestForm(forms.ModelForm):

    class Meta:
        model = GuestEmail
        fieds = [
            'email'
        ]

    def __init__(self,request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).save(commit=True)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    passowrd = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm,self).__init__(*args, **kwargs)


    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        qs = User.objects.filter(email=email)
        if qs.exists():

            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse("account: resend activation")
                reconfirm_msg = """ Go to <a href='{resend_link}'>""".format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()

                if is_confirmable:
                    msg1 = 'Please check you account to confirm or ' + reconfirm_msg.lower()

                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed." + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and email_confirm_exists:
                    raise forms.ValidationError('This useris inactive')

        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError('Invalid Credentials were provided')
        login(request, user)
        self.user = user
        return data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm passowrd', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email')

        def clean_password2(self):
            password1 = self.cleaned_data.get('password')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")

            return password2

        def save(self, commit=True):
            user = super(RegisterForm, slef).save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.is_active = False

            if commit:
                user.save()
            return user




