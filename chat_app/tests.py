from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url
from django.db.models import QuerySet
from django import forms
from .models import Conversation, Message, MessageThought
from .forms import ConversationForm, MessageForm, MessageThoughtForm
from datetime import date


#Test Views
class HomeViewTest(TestCase):
    def setUp(self):
        self.url = reverse('home')
        self.conversation_form_data = {'conversation_form_submit': '', 'title': 'Test Conversation'}

    def test_home_view_returns_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_uses_correct_form(self):
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['conversation_form'], ConversationForm)

    def test_home_view_creates_conversation_on_post(self):
        response = self.client.post(self.url, data=self.conversation_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Conversation.objects.count(), 1)
        conversation = Conversation.objects.first()
        self.assertEqual(conversation.title, 'Test Conversation')

    def test_home_view_get(self):
        # Test GET request to home view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIsInstance(response.context['conversation_form'], ConversationForm)
        self.assertContains(response, 'placeholder="New conversation"')
        self.assertIsInstance(response.context['conversations'], QuerySet)

    def test_home_view_post_valid_form(self):
        # Test POST request to home view with a valid form
        response = self.client.post(self.url, data=self.conversation_form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = resolve_url('conversation_detail', pk=Conversation.objects.latest('pk').pk)
        self.assertRedirects(response, expected_url)

    def test_home_view_post_invalid_form(self):
        # Test POST request to home view with an invalid form
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIsInstance(response.context['conversation_form'], ConversationForm)
        self.assertEqual(Conversation.objects.count(), 0)


class ConversationDetailTest(TestCase):
    def setUp(self):
        self.conversation = Conversation.objects.create()
        self.message = Message.objects.create(conversation=self.conversation)
        self.conversation_form_data = {'conversation_form_submit': '', 'title': 'Test Conversation'}
        self.message_form_data = {
            'message_form_submit': '',
            'text': 'Test message content',
            'conversation': self.conversation.pk,
        }
        self.thought_form_data = {
            'thought_form_submit': '',
            'text': 'Test thought content',
            'message': self.message.pk,
        }

        self.url = reverse('conversation_detail', args=[self.conversation.pk])
        print(f"URL = {self.url}, pk = {self.conversation.pk}")

    def test_conversation_detail_view_get(self):
        # Test GET request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the expected data
        self.assertEqual(response.context['conversation'], self.conversation)
        self.assertEqual(response.context['messages'].count(), 1)
        self.assertIsInstance(response.context['message_form'], MessageForm)
        self.assertIsInstance(response.context['thought_form'], MessageThoughtForm)
        self.assertIsInstance(response.context['conversation_form'], ConversationForm)
        self.assertEqual(response.context['conversations'].count(), 1)

    def test_conversation_detail_view_post_message_form(self):
        # Send a POST request to the conversation_detail view with the MessageForm data
        response = self.client.post(self.url, data=self.message_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 2)  # Including the initial test message

    def test_conversation_detail_view_post_thought_form(self):
        # Send a POST request to the conversation_detail view with the MessageThoughtForm data
        response = self.client.post(self.url, data=self.thought_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MessageThought.objects.count(), 1)

    def test_conversation_detail_view_post_conversation_form(self):
        response = self.client.post(self.url, data=self.conversation_form_data)
        print(f"URL: {self.url}")
        print(response)
        self.assertEqual(response.status_code, 302)
        expected_url = resolve_url('conversation_detail', pk=Conversation.objects.latest('pk').pk)
        self.assertRedirects(response, expected_url)
        self.assertEqual(Conversation.objects.count(), 2)  # Including the initial test conversation


#Test Models
class ConversationModelTests(TestCase):
    def test_conversation_creation(self):
        # Create a Conversation object
        conversation = Conversation.objects.create(
            title="Test Conversation",
            start_date=date.today()
        )

        # Assert that the Conversation object was created successfully
        self.assertIsInstance(conversation, Conversation)
        self.assertEqual(conversation.title, "Test Conversation")
        self.assertEqual(conversation.start_date, date.today())

    def test_conversation_title_max_length(self):
        # Create a Conversation object with a title longer than 255 characters
        conversation = Conversation(
            title="A" * 256,
            start_date=date.today()
        )

        # Assert that trying to save the Conversation object raises a ValidationError
        with self.assertRaises(Exception):
            conversation.save()

    def test_conversation_start_date_default_value(self):
        # Create a Conversation object without providing a start_date
        conversation = Conversation.objects.create(
            title="Test Conversation",
        )

        # Assert that the start_date is set to today's date by default
        self.assertEqual(conversation.start_date, date.today())


class MessageModelTest(TestCase):
    def setUp(self):
        self.conversation = Conversation.objects.create(title='Test Conversation')
        self.message = Message.objects.create(conversation=self.conversation, text='Test Message')

    def test_message_model_fields(self):
        message = Message.objects.get(id=self.message.id)
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.text, 'Test Message')
        self.assertIsNotNone(message.date_sent)

    def test_message_model_str_representation(self):
        message = Message.objects.get(id=self.message.id)
        expected_str = f'Message: {message.text}'
        self.assertEqual(str(message), expected_str)


class MessageThoughtModelTest(TestCase):
    def setUp(self):
        self.conversation = Conversation.objects.create(title='Test Conversation')
        self.message = Message.objects.create(conversation=self.conversation, text='Test Message')
        self.thought = MessageThought.objects.create(message=self.message, text='Test Thought')

    def test_message_thought_model_fields(self):
        thought = MessageThought.objects.get(id=self.thought.id)
        self.assertEqual(thought.message, self.message)
        self.assertEqual(thought.text, 'Test Thought')
        self.assertIsNotNone(thought.date_sent)

    def test_message_thought_model_str_representation(self):
        thought = MessageThought.objects.get(id=self.thought.id)
        expected_str = f'Thought: {thought.text}'
        self.assertEqual(str(thought), expected_str)


#Test Forms
class ConversationFormTest(TestCase):
    def test_conversation_form_max_length(self):
        # Create a form instance with a long title that exceeds the max_length
        long_title = 'a' * (Conversation._meta.get_field('title').max_length + 1)
        form_data = {'title': long_title}
        form = ConversationForm(data=form_data)

        # Ensure the form is not valid
        self.assertFalse(form.is_valid())

    def test_conversation_form_widget_attributes(self):
        # Create a form instance
        form = ConversationForm()

        # Convert max_length to a string for comparison
        max_length_str = str(Conversation._meta.get_field('title').max_length)

        # Ensure the 'title' field has the correct widget attributes
        title_widget = form.fields['title'].widget
        self.assertEqual(title_widget.attrs.get('placeholder'), 'New conversation')
        self.assertEqual(title_widget.attrs.get('maxlength'), max_length_str)


class MessageFormTest(TestCase):
    def test_message_form_widget_attributes(self):
        # Create a form instance
        form = MessageForm()

        # Ensure the 'text' field has the correct widget attributes
        text_widget = form.fields['text'].widget
        self.assertEqual(text_widget.attrs.get('placeholder'), 'Send a new message')
        self.assertIsInstance(text_widget, forms.Textarea)


class MessageThoughtFormTest(TestCase):
    def test_message_thought_form_widget_attributes(self):
        # Create a form instance
        form = MessageThoughtForm()

        # Ensure the 'text' field has the correct widget attributes
        text_widget = form.fields['text'].widget
        self.assertEqual(text_widget.attrs.get('placeholder'), 'Add your thoughts')
        self.assertIsInstance(text_widget, forms.TextInput)

        # Ensure the 'message_id' field has the correct widget attributes
        message_widget = form.fields['message'].widget
        self.assertIsNone(message_widget.attrs.get('type'))
        self.assertIsInstance(message_widget, forms.HiddenInput)
