from django import forms
from .models import Conversation, Message, MessageThought


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={
            'placeholder': 'New conversation',
            'maxlength': Conversation._meta.get_field('title').max_length})
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'placeholder': 'Send a new message'})}


class MessageThoughtForm(forms.ModelForm):
    class Meta:
        model = MessageThought
        fields = ['text', 'message']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Add your thoughts'}),
            'message': forms.HiddenInput(attrs={'type': 'hidden'})
            }


class ConversationSearchForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={
            'placeholder': 'Search for conversation by title',
            'maxlength': Conversation._meta.get_field('title').max_length})
        }


class MessageSearchForm(forms.ModelForm):
    # max length matches the max length of the title
    class Meta:
        model = Message
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'placeholder': 'Search for message by content'})}