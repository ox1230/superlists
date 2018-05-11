from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest

from unittest import skip
import time
import sys



class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        """  """
        #edith가 해당 웹사이트 방문
        self.browser.get(self.server_url)

        # 타이틀과 헤더가 'To-Do'를 표시
        self.assertIn('To-Do' ,self.browser.title) 


        #작업 추가
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputBox.get_attribute('placeHolder'), 
            '작업아이템 입력'
        )

        # '공작깃털 사기'라고 텍스트 상자에 입력
        inputBox.send_keys('공작깃털 사기')
        # 엔터키를 치면 페이지 갱신, 작업 목록에 "1: 공작깃털 사기"아이템이 추가 
        inputBox.send_keys(Keys.ENTER)
        time.sleep(2)
        edith_list_url = self.browser.current_url
    
        self.assertRegex(edith_list_url, '/lists/.+')
        #assertRegex: 지정 정규표현식과 문자열이 일치하는지 확인
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
        inputBox = self.browser.find_element_by_id('id_new_item')
        
        # 다시 '공작 깃털을 이용해 그물 만들기"라고 입력
        inputBox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputBox.send_keys(Keys.ENTER)

        # 페이지 갱신, 두개의 아이템이 목록에 표시
        self.check_for_row_in_list_table("2: 공작깃털을 이용해서 그물 만들기")
        self.check_for_row_in_list_table('1: 공작깃털 사기')
    
        #Francis가 사이트에 접속
        ## 새로운 브라우저 세션을 이용해서 Edith의 정보가 쿠키를 통해 유입되는 것을 방지한다.

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        #프란시스가 새로운 작업 아이템을 입력한다
        inputBox = self.browser.find_element_by_id('id_new_item')
        
        inputBox.send_keys('우유 사기')
        inputBox.send_keys(Keys.ENTER)

        #프란시스가 전용 URL을 취득한다
        time.sleep(2)
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #에디스가 입력한 흔적이 없다는 것을 확인한다.

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

