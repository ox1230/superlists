from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item
import re

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        # resolve: url을 해석해 일치하는 뷰 함수를 찾는다.   여기서는 /가 호출될때 resolve를 실행해서 home_page함수를 호출한다.
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()      # 사용자가 보낸 요청 확인
        response = home_page(request)   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        
        expected_html = render_to_string('home.html', request = request)
        
        self.assertEqual(self.remove_csrf_tag(response.content.decode()), self.remove_csrf_tag(expected_html))
    
    def test_home_page_can_save_a_POST_request(self):
        #POST 테스트가 너무 길어지고 있다!!
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')


        self.assertIn('신규 작업 아이템', response.content.decode())
        
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': '신규 작업 아이템'},
            request = request)

        self.assertEqual(self.remove_csrf_tag(response.content.decode()), self.remove_csrf_tag(expected_html))

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()

        home_page(request)

        self.assertEqual(Item.objects.count(),0)


    def remove_csrf_tag(self,text):
        """Remove csrf tag from TEXT"""
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')