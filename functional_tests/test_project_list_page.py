from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

options = Options()
options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'


class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.close()

    def test_no_projects_alert(self):
        self.browser.get(self.live_server_url)
        # time.sleep(20)

        # User requests the page for the first time
        alert = self.browser.find_element_by_class_name('noproject-wrapper')

        self.assertEquals(
            alert.find_element_by_tag_name(
                'h3').text, 'Sorry, you don\'t have any projects, yet.'
        )

    def test_no_projects_alert_button_redirect(self):
        self.browser.get(self.live_server_url)

        # User requests the page for the first time
        # time.sleep(20)
        add_url = self.live_server_url + reverse('add')
        self.browser.find_element_by_tag_name('a').click()

        self.assertEquals(
            self.browser.current_url,
            add_url
        )

    def test_projects_list(self):
        project1 = Project.objects.create(
            name='project1',
            budget=10000
        )
        self.browser.get(self.live_server_url)

        # User sees the project on the screen
        # time.sleep(20)

        self.assertEquals(
            self.browser.find_element_by_tag_name('h5').text,
            'project1'
        )

    def test_projects_detail(self):
        project1 = Project.objects.create(
            name='project1',
            budget=10000
        )
        self.browser.get(self.live_server_url)

        # User sees the project on the screen and visits detail page
        # time.sleep(20)
        detail_url = self.live_server_url + \
            reverse('detail', args=[project1.slug])

        self.assertEquals(
            self.browser.find_element_by_link_text('VISIT').click(),
            self.assertEquals(
                self.browser.current_url,
                detail_url
            )
        )
