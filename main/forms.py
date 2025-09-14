from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjUserCreationForm
from django.core import validators as dj_validators

from main import models


class OnboardForm(forms.ModelForm):
    sunflower = forms.BooleanField(required=False)

    class Meta:
        model = models.Onboard
        fields = ["problems", "quality", "seo"]


class UserCreationForm(DjUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["email"]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, list | tuple):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadTextFilesForm(forms.Form):
    file = MultipleFileField()


class UploadImagesForm(forms.Form):
    file = MultipleFileField(
        validators=[
            dj_validators.FileExtensionValidator(
                ["jpeg", "jpg", "png", "svg", "gif", "webp", "tiff", "tif", "bmp", "txt", "md", "rtf", "pdf", "epub", "doc", "docx", "odt", "ppt", "pptx", "odp", "xls", "xlsx", "ods", "csv", "tsv", "ics", "vcf", "log", "json", "xml", "yml", "yaml", "ini", "toml", "cfg", "conf", "mdown", "markdown"]
            )
        ],
    )


class StripeForm(forms.Form):
    card_token = forms.CharField(max_length=100, widget=forms.HiddenInput())


class ResetAPIKeyForm(forms.Form):
    """Reset user's api_key field."""


class APIPost(forms.Form):
    """Form for Post resource when accessed from the API."""

    title = forms.CharField(max_length=300, required=False)
    slug = forms.SlugField(max_length=300, required=False)
    body = forms.CharField(widget=forms.Textarea, required=False)
    published_at = forms.DateField(required=False)
