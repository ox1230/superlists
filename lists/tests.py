from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# resolve: url을 해석해 일치하는 뷰 함수를 찾는다.   여기서는 /가 호출될때 resolve를 실행해서 home_page함수를 호출한다.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()      # 사용자가 보낸 요청 확인
        response = home_page(request)   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))