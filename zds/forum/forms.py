# coding: utf-8

import re

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Hidden
from crispy_forms.bootstrap import StrictButton
from zds.forum.models import Forum, Topic, sub_tag, Tag
from zds.utils.forms import CommonLayoutEditor
from django.utils.translation import ugettext_lazy as _


class TopicForm(forms.Form):
    title = forms.CharField(
        label=_('Titre'),
        max_length=Topic._meta.get_field('title').max_length,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'[Tag 1][Tag 2] Titre de mon sujet'),
                'required': 'required',
            }
        )
    )

    subtitle = forms.CharField(
        label=_('Sous-titre'),
        max_length=Topic._meta.get_field('subtitle').max_length,
        required=False,
    )

    text = forms.CharField(
        label='Texte',
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Votre message au format Markdown.'),
                'required': 'required',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title', autocomplete='off'),
            HTML('<div id="results" ><table id="tb-results" class="topics-entries"></table></div>'),
            Field('subtitle', autocomplete='off'),
            CommonLayoutEditor(),
        )

    def clean(self):
        cleaned_data = super(TopicForm, self).clean()

        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if title is not None:
            if title.strip() == '':
                self._errors['title'] = self.error_class(
                    [_(u'Le champ titre ne peut être vide')])
                if 'title' in cleaned_data:
                    del cleaned_data['title']
            elif re.sub(ur"(?P<start>)(\[.*?\])(?P<end>)", sub_tag, title) \
                    .strip() == '':
                self._errors['title'] = self.error_class(
                    [_(u'Le titre ne peux pas contenir uniquement des tags')])
            else:
                tags = re.findall(ur"((.*?)\[(.*?)\](.*?))", title)
                for tag in tags:
                    if tag[2].strip() == "":
                        if 'title' in cleaned_data:
                            self._errors['title'] = self.error_class(
                                [_(u'Un tag ne peut être vide')])

                    elif len(tag[2]) > Tag._meta.get_field('title').max_length:
                        if 'title' in cleaned_data:
                            self._errors['title'] = self.error_class(
                                [_(u'Un tag doit faire moins de {0} caractères').
                                    format(Tag._meta.get_field('title').max_length)])
        if text is not None and text.strip() == '':
            self._errors['text'] = self.error_class(
                [_(u'Le champ text ne peut être vide')])
            if 'text' in cleaned_data:
                del cleaned_data['text']

        if text is not None and len(text) > settings.ZDS_APP['forum']['max_post_length']:
            self._errors['text'] = self.error_class(
                [_(u'Ce message est trop long, il ne doit pas dépasser {0} '
                   u'caractères').format(settings.ZDS_APP['forum']['max_post_length'])])

        return cleaned_data


class PostForm(forms.Form):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Votre message au format Markdown.'),
                'required': 'required',
            }
        )
    )

    def __init__(self, topic, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            CommonLayoutEditor(),
            Hidden('last_post', '{{ last_post_pk }}'),
        )
        if topic.antispam(user):
            if 'text' not in self.initial:
                self.helper['text'].wrap(
                    Field,
                    placeholder=_(u'Vous venez de poster. Merci de patienter '
                                  u'au moins 15 minutes entre deux messages consécutifs '
                                  u'afin de limiter le flood.'),
                    disabled=True)
        elif topic.is_locked:
            if 'text' not in self.initial:
                self.helper['text'].wrap(
                    Field,
                    placeholder=_(u'Ce topic est verrouillé.'),
                    disabled=True
                )

    def clean(self):
        cleaned_data = super(PostForm, self).clean()

        text = cleaned_data.get('text')

        if text is None or text.strip() == '':
            self._errors['text'] = self.error_class(
                [_(u'Vous devez écrire une réponse !')])

        elif len(text) > settings.ZDS_APP['forum']['max_post_length']:
            self._errors['text'] = self.error_class(
                [_(u'Ce message est trop long, il ne doit pas dépasser {0} '
                   u'caractères').format(settings.ZDS_APP['forum']['max_post_length'])])

        return cleaned_data


class MoveTopicForm(forms.Form):

    forum = forms.ModelChoiceField(
        label=_("Forum"),
        queryset=Forum.objects.all(),
        required=True,
    )

    def __init__(self, topic, *args, **kwargs):
        super(MoveTopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(
            'zds.forum.views.move_topic') + '?sujet=' + str(topic.pk)
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('forum'),
            StrictButton(_('Valider'), type='submit'),
        )
