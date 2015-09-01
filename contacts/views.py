
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.db.models import Q
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ContactForm, ContactAddressFormSet


class ContactOwnerMixin(object):

    def get_object(self, queryset=None):
        """Returns the object the view is displaying."""

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(pk=pk, owner=self.request.user)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise PermissionDenied
        return obj


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class ReturnToMain(object):
    def get_success_url(self):
        return reverse('contacts-list')


class ListContactView(LoggedInMixin, ListView):
    model = Contact
    template_name = "contact_list.html"

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


class ListContactByNameView(LoggedInMixin, ListView):
    template_name = "contacts_by_name_list.html"

    def get_queryset(self):
        name = self.kwargs['name']
        return Contact.objects.filter(Q(first_name__icontains=name) |
                                      Q(last_name__icontains=name) &
                                      Q(owner=self.request.user))

    def get_context_data(self, **kwargs):
        context = super(ListContactByNameView, self).get_context_data(**kwargs)
        context['name'] = self.kwargs['name']
        return context


class CreateContactView(LoggedInMixin, ContactOwnerMixin, ReturnToMain, CreateView):
    model = Contact
    template_name = "edit_contact.html"
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')
        return context


class UpdateContactView(LoggedInMixin, ContactOwnerMixin, ReturnToMain, UpdateView):
    model = Contact
    template_name = "edit_contact.html"
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',
                                    kwargs={'pk': self.get_object().id})
        return context


class DeleteContactView(LoggedInMixin, ContactOwnerMixin, ReturnToMain, DeleteView):
    model = Contact
    template_name = "delete_contact.html"


class DetailContactView(LoggedInMixin, ContactOwnerMixin, DetailView):
    model = Contact
    template_name = 'contact.html'


class EditContactAddressView(LoggedInMixin, ContactOwnerMixin, UpdateView):
    model = Contact
    template_name = 'edit_addresses.html'
    form_class = ContactAddressFormSet

    def get_success_url(self):
        return self.get_object().get_absolute_url()

