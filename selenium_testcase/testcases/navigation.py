# -*- coding: utf-8 -*-

from __future__ import absolute_import

from urlparse import urljoin

from django.urls import reverse
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from .utils import wait_for


class NavigationTestMixin:

    def get_page(self, url):
        """ Navigate to the given url.  """
        return self.browser.get(urljoin(self.live_server_url, url))

    def get_page_by_name(self, viewname, *args, **kwargs):
        """ Navigate to the named url using django.urls.reverse(). """
        return self.browser.get(
            urljoin(self.live_server_url,
                    reverse(viewname, *args, **kwargs)))

    dropdown_search_list = (
        (By.ID, '{}',),
        (By.NAME, '{}',),
    )

    @wait_for
    def get_dropdown(self, field, *kwargs):
        """ Find a dropdown menu on the current page. """
        return self.find_element(
            self.dropdown_search_list, field, *kwargs)

    def select_dropdown(self, field, value, *kwargs):
        """ Select a dropdown menu on the current page. """
        dropdown = self.get_dropdown(field, *kwargs)
        input = Select(dropdown)
        input.select_by_visible_text(value)

    # default search for button
    button_search_list = (
        (By.ID, '{}',),
        (By.NAME, '{}',),
        (By.XPATH, '//a[normalize-space()="{}"]',),
        (By.XPATH, '//input[@value="{}"]',),
        (By.XPATH, '//input[@type="{}"]', ),
        (By.XPATH, '//button[normalize-space()="{}"]',),
        (By.XPATH, '//button[normalize-space()[contains(.,"{}")]]',),
    )

    @wait_for
    def get_button(self, value, *args, **kwargs):
        """ Select a button or link with the given name.  """
        return self.find_element(
            self.button_search_list, value, *args, **kwargs)

    def click_button(self, value, *args, **kwargs):
        """ Select a button or link with the given name.  """
        button = self.get_button(value, *args, **kwargs)
        button.click()

    def hover_over_button(self, value, *args, **kwargs):
        """ Hover over a button or link with the given name. """
        button = self.get_button(value, *args, **kwargs)
        hover = ActionChains(self.browser).move_to_element(button)
        hover.perform()

    @wait_for
    def at_page(self, url, **kwargs):
        """ Assert current page is not at the given url. """
        self.assertEqual(
            urljoin(self.live_server_url, url), self.browser.current_url)

    @wait_for
    def not_at_page(self, url, **kwargs):
        """ Assert current page is at the given url. """
        self.assertNotEqual(
            urljoin(self.live_server_url, url), self.browser.current_url)

    @wait_for
    def url_should_contain(self, text, **kwargs):
        """ Assert if the current url DOES NOT contain the given string. """
        self.assertIn(text, self.browser.current_url)

    @wait_for
    def url_should_not_contain(self, text, **kwargs):
        """ Assert if the current url DOES contain the given string. """
        self.assertNotIn(text, self.browser.current_url)
