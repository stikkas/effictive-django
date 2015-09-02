
# encoding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test.client import Client, RequestFactory
from rebar.testing import flatten_to_dict
from contacts.models import Contact
from contacts.views import ListContactView
from contacts import forms


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ContactTests(TestCase):
    def test_str(self):
        contact = Contact(first_name='John', last_name='Smith')
        self.assertEquals(str(contact), 'Smith John')


class ContactListViewTest(TestCase):
    url = reverse('contacts-list')

    def test_contacts_in_the_context(self):
        client = Client()
        response = client.get(self.url)
        self.assertEquals(list(response.context['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')

        response = client.get(self.url)
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):
        factory = RequestFactory()
        request = factory.get(self.url)

        response = ListContactView.as_view()(request)
        self.assertEquals(list(response.context_data['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')

        response = ListContactView.as_view()(request)
        self.assertEquals(response.context_data['object_list'].count(), 1)


class ContactListIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.list_url = reverse('contacts-list')
        cls.edit_url = reverse('contacts-new')
        cls.selenium = WebDriver()
        super(ContactListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactListIntegrationTests, cls).tearDownClass()

    def test_contact_listed(self):
        Contact.objects.create(first_name="foo", last_name="bar")
        self.selenium.get('%s%s' % (self.live_server_url, self.list_url))
        self.assertEqual(self.selenium.find_elements_by_css_selector(
            '.contact > a:first-child')[0].text, 'bar foo')

    def add_contact_linked(self):
        self.selenium.get('%s%s' % (self.live_server_url, self.list_url))
        self.assertTrue(self.selenium.find_element_by_link_text(u'Добавить контакт'))

    def test_add_contact(self):
        self.selenium.get('%s%s' % (self.live_server_url, self.list_url))
        self.selenium.find_element_by_link_text(u'Добавить контакт').click()
        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@contact.tu')
        self.selenium.find_element_by_id('id_confirm_email').send_keys('test@contact.tu')
        self.selenium.find_element_by_id('save_contact').click()
        self.assertEqual(self.selenium.find_elements_by_css_selector(
            '.contact > a:first-child')[-1].text, 'contact test')


class EditContactFormTests(TestCase):
    def test_mismatch_email_is_invalid(self):
        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@bar.ru'
        form_data['confirm_email'] = 'bar@foo.ru'

        bound_form = forms.ContactForm(data=form_data)
        self.assertFalse(bound_form.is_valid())

    def test_same_email_is_valid(self):
        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@bar.ru'
        form_data['confirm_email'] = 'foo@bar.ru'

        bound_form = forms.ContactForm(data=form_data)
        self.assertTrue(bound_form.is_valid())

