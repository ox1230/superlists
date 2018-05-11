from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest
from unittest import skip
import time
import sys


class LayoutAndStylingTest(FunctionalTest):
    
    def test_layout_and_styling(self):
        
        #에디스는 메인페이지를 방문한다
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)   #윈도우 사이즈는 중간

        #입력상자가 가운데에 위치한 것을 본다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )

        #새로운 리스트를 시작하고 입력상자가 가운데 배치된것을 확인
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )
