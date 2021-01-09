from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="Search")


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="Content", widget=forms.Textarea)
