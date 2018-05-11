from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest

from unittest import skip
import time
import sys


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_addd_empty_list_items(self):
        #에디스는 메인페이지에 접속해 빈아이템을 실수로 등록하려 한다

        # 입력상자가 비어있는 상태에서 엔터키를 누른다

        # 페이지가 새로고침되고, 빈아이템을 등록할 수 없다는 에러메세지가 표시된다

        # 다른아이템을 입력하고 정상처리

        # 다시 빈아이템 입력

        # 에러메세지 표시



        self.fail('write me!')



