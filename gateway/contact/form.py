from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(max_length=100, label='Your email')
    msg_body = forms.CharField(max_length=500, widget=forms.Textarea)

    name.widget.attrs.update({
        'class':'form-control',
        'placeholder': 'Your name',
    })
    email.widget.attrs.update({
        'class':'form-control',
        'placeholder': 'Your email',
    })
    msg_body.widget.attrs.update({
        'class':'form-control',
        'placeholder':'Please enter your message here...',
        'rows': 5,
    })

    pass


