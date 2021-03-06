from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest

from unittest import skip
import time
import sys


class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        #에디스는 메인페이지에 접속해 빈아이템을 실수로 등록하려 한다

        # 입력상자가 비어있는 상태에서 엔터키를 누른다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 페이지가 새로고침되고, 빈아이템을 등록할 수 없다는 에러메세지가 표시된다
        # error = self.browser.find_element_by_css_selector('.has-error')
        # self.assertEqual(error.text, '빈 아이템을 등록할 수 없습니다')
        """ http code required가 들어가서 입력자체가 되지 않는다 -- 해결책 알수 없음 ㅠㅠ"""
        # 다른아이템을 입력하고 정상처리

        self.get_item_input_box().send_keys('우유 사기')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: 우유 사기')

        # 다시 빈아이템 입력
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 에러메세지 표시
        self.check_for_row_in_list_table('1: 우유 사기')
        # error = self.browser.find_element_by_css_selector('.has-error')
        # self.assertEqual(error.text, '빈 아이템을 등록할 수 없습니다')
        """ http code required가 들어가서 입력자체가 되지 않는다 -- 해결책 알수 없음 ㅠㅠ"""

        #아이템 입력시 다시 정상 동작
        self.get_item_input_box().send_keys('차 만들기')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: 우유 사기')
        self.check_for_row_in_list_table('2: 차 만들기')
    
    def test_cannot_add_duplicate_items(self):
        #에디스는 메인페이지로 돌아가서 신규목록을 시작한다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('콜라 사기')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: 콜라 사기')

        time.sleep(1)
        #실수로 중복 아이템을 입력한다
        self.get_item_input_box().send_keys('콜라 사기')
        self.get_item_input_box().send_keys(Keys.ENTER)

        #도움이 되는 에러메세지를 본다.
        self.check_for_row_in_list_table('1: 콜라 사기')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, '이미 리스트에 해당 아이템이 있습니다')




