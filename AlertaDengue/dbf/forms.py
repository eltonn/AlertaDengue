from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dbf.models import DBF, DBFChunkedUpload
from dbf.validation import is_valid_dbf


class DBFForm(forms.Form):
    uploaded_by = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    chunked_upload_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    filename = forms.CharField(required=False, widget=forms.HiddenInput())
    export_date = forms.DateField()
    notification_year = forms.IntegerField()

    def clean(self):
        cleaned_data = super(DBFForm, self).clean()
        chunked_upload_id = cleaned_data.get('chunked_upload_id')
        user = cleaned_data.get('uploaded_by')
        # If the user tries to give the id of a chunked_upload by
        # another user, or an inexistent id, we raise a validation
        # error.
        try:
            uploaded_file = DBFChunkedUpload.objects.get(id=chunked_upload_id, user=user)
        except DBF.DoesNotExist:
            raise ValidationError("It looks like there was an error during the file upload. "
                    "Please try again.")
        # This might be a performance problem for really large DBFs
        is_valid_dbf(uploaded_file.file, cleaned_data['notification_year'])
        return cleaned_data