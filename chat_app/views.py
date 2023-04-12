from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from .models import Conversation, Message, MessageThought
from .forms import ConversationForm, MessageForm, MessageThoughtForm, ConversationSearchForm, MessageSearchForm


def home(request):
    if 'search_context' in request.session:
        del request.session['search_context']

    conversations = Conversation.objects.all()
    conversation_form = ConversationForm()
    conversation_search_form = ConversationSearchForm()
    message_search_form = MessageSearchForm()

    if request.method == 'POST':
        if 'conversation_form_submit' in request.POST:
            conversation_form = ConversationForm(request.POST)
            if conversation_form.is_valid():
                conversation = conversation_form.save()
                return redirect('conversation_detail', pk=conversation.pk)

    if request.method == 'GET':
        if 'conversation_search_form_submit' in request.GET:
            conversation_search_form = ConversationSearchForm(request.GET)  # Pass request.GET data to the form
            if conversation_search_form.is_valid():
                print("GET REQUEST")
                title = conversation_search_form.cleaned_data.get('title')
                filtered_conversations = conversations.filter(title__icontains=title)
                print(list(filtered_conversations))
                context = {
                    'title': title,
                    'filtered_conversations': list(filtered_conversations.values_list('pk', flat=True)),
                }
                request.session['search_context'] = context
                return redirect('conversation_search_results', title)
        if 'message_search_form_submit' in request.GET:
            message_search_form = MessageSearchForm(request.GET)  # Pass request.GET data to the form
            if message_search_form.is_valid():
                messages = Message.objects.all()
                print("GET REQUEST")
                search_text = message_search_form.cleaned_data.get('text')
                filtered_messages = messages.filter(text__icontains=search_text)
                print(list(filtered_messages))
                context = {
                    'search_text': search_text,
                    'filtered_messages': list(filtered_messages.values_list('pk', flat=True)),
                }
                request.session['search_context'] = context
                return redirect('message_search_results', search_text)


    else:
        conversation_form = ConversationForm()
        conversation_search_form = ConversationSearchForm()
        message_search_form = MessageSearchForm()

    context = {
        'conversations': conversations,
        'conversation_form': conversation_form,
        'conversation_search_form': conversation_search_form,
        'message_search_form': message_search_form,
    }
    return render(request, 'home.html', context)

def conversation_detail(request, pk):
    if 'search_context' in request.session:
        del request.session['search_context']

    conversation = get_object_or_404(Conversation, pk=pk)
    messages = conversation.message_set.all()
    message_form = MessageForm()
    thought_form = MessageThoughtForm()
    conversation_form = ConversationForm()

    if request.method == 'POST':
        if 'message_form_submit' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.conversation = conversation
                message.save()
                return redirect('conversation_detail', pk=conversation.pk)
        if 'thought_form_submit' in request.POST:
            thought_form = MessageThoughtForm(request.POST)
            if thought_form.is_valid():
                message_id = request.POST['message']
                message = Message.objects.get(id=message_id)
                thought = thought_form.save(commit=False)
                thought.message = message
                thought.save()
                return redirect('conversation_detail', pk=message.conversation.pk)
        if 'conversation_form_submit' in request.POST:
            new_conversation_form = ConversationForm(request.POST)
            if new_conversation_form.is_valid():
                conversation = new_conversation_form.save()
                return redirect('conversation_detail', pk=conversation.pk)
    else:
        message_form = MessageForm()
        thought_form = MessageThoughtForm()
        conversation_form = ConversationForm()

    conversations = Conversation.objects.all()

    context = {
        'conversation': conversation,
        'messages': messages,
        'message_form': message_form,
        'thought_form': thought_form,
        'conversation_form': conversation_form,
        'conversations': conversations,
    }

    return render(request, 'chat_app/conversation_detail.html', context)


def conversation_search_results(request, title):
    conversations = Conversation.objects.all()

    #context contains search title and a list of conversation pks
    context = request.session['search_context']
    print(f"context: {context}")
    conversation_ids = context['filtered_conversations']
    filtered_conversations = Conversation.objects.filter(id__in=conversation_ids)
    context['filtered_conversations'] = filtered_conversations
    context['conversations'] = conversations

    return render(request, 'chat_app/conversation_search_results.html', context)

def message_search_results(request, search_text):
    conversations = Conversation.objects.all()

    #context contains search text and a list of message pks
    context = request.session['search_context']
    print(f"context: {context}")
    message_ids = context['filtered_messages']
    filtered_messages = Message.objects.filter(id__in=message_ids)
    context['filtered_messages'] = filtered_messages
    context['conversations'] = conversations

    return render(request, 'chat_app/message_search_results.html', context)