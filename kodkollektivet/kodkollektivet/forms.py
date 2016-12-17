from django.forms import ModelForm, ValidationError, CharField, PasswordInput
from .models import Project, Contributor


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('gh_name', 'gh_id', 'gh_url', 'gh_readme')


class ContributorForm(ModelForm):
    password = CharField(widget=PasswordInput)
    password_verify = CharField(widget=PasswordInput, label='Password confirmation')
    def __init__(self, *args, **kwargs):
        super(ContributorForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['email'].required = True
        self.fields['gh_login'].required = True
        self.fields['gh_url'].required = True
        self.fields['gh_id'].required = True
        self.fields['gh_id'].required = True

    class Meta:
        model = Contributor
        # fields = ('gh_login', 'gh_url', 'gh_id')
        fields = ['first_name',
                  'last_name',
                  'email',
                  'website',
                  'linkedin',
                  'about',
                  'password',
                  'gh_login',
                  'gh_url',
                  'gh_id',
                  'gh_html']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        self.cleaned_data = super(ContributorForm, self).clean()
        if 'password' in self.cleaned_data and 'password_verify' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
                raise ValidationError("Passwords mismatch")
            return self.cleaned_data


    def save(self, commit=True):
        user = super(ContributorForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
