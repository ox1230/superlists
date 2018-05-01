from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        """테스트 시작 전에 수행"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)   # 암묵적 대기 -- 5초
    
    def tearDown(self):
        """테스트 후에 시행-- 테스트에 에러가 발생해도 실행된다"""
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        """  """
        #해당 웹사이트 방문
        self.browser.get('http://localhost:8000')

        # 타이틀과 헤더가 'To-Do'를 표시
        self.assertIn('To-Do' ,self.browser.title)  # 다양한 assert


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
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn( '1: 공작깃털 사기',[row.text for row in rows])
        

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
        inputBox = self.browser.find_element_by_id('id_new_item')
        
        # 다시 '공작 깃털을 이용해 그물 만들기"라고 입력
        inputBox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputBox.send_keys(Keys.ENTER)

        # 페이지 갱신, 두개의 아이템이 목록에 표시
        time.sleep(2)        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn( '1: 공작깃털 사기',[row.text for row in rows])
        self.assertIn( '2: 공작깃털을 이용해서 그물 만들기',[row.text for row in rows])
        
        self.fail('Finish the test!')  # 강제적 테스트 실패 발생
        #사이트가 입력한 목록을 저장하고 있는가? -- 특정 URL로 접속하면 작업목록이 그대로 있다.

if __name__ == '__main__':
    unittest.main(warnings= 'ignore')