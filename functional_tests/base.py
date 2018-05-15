from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from unittest import skip
import time
import sys

class FunctionalTest(StaticLiveServerTestCase):
    
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
            super().setUpClass()
            cls.server_url = cls.live_server_url
    
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        """테스트 시작 전에 수행"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)   # 암묵적 대기 -- 3초

    def tearDown(self):
        """테스트 후에 시행-- 테스트에 에러가 발생해도 실행된다"""
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        time.sleep(1)        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')