from django import forms


# Formats ModelForms with BootStrap
class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Iterates through all fields in the ModelForm
        for name, field in self.fields.items():

            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label

            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }
