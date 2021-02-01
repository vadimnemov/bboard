from django import forms
from .models import AdvUser, SuperRubric, SubRubric
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import user_registrated

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль ещё раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        """
        if password1:
            password_validation.validate_password(password1)
        return password1
        """
        try:
            password_validation.validate_password(password1)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean(self):
            super().clean()
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 and password2 and password1 != password2:
                errors = {'password2': ValidationError(
                        'Введенные пароли не совпадают', code='password_mismatch')}
                raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, isinstance=user)
        return user

    class Meta:
        model = AdvUser
        fields =  ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages')

class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
                   queryset=SuperRubric.objects.all(), empty_label=None,
                   label='Надрубрика', required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'

class SearchForm(forms.Form):
    reyword = forms.CharField(required=False, max_length=20, label='')