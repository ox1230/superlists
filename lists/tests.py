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

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/only_list/')   #/를 붙이자 !! ㅜㅜ

        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text = 'item1')
        Item.objects.create(text = 'item2')
        
        response = self.client.get('/lists/only_list/')

        self.assertContains(response,'item1')
        self.assertContains(response, 'item2')
    
    def test_saving_a_POST_request(self):
        
        self.client.post(
            '/lists/new',   #뒤에 꼬리슬래시를 사용하지 않는 것은 데이터베이스에 변경을 가하는 "액션" URL
            data = {'item_text': '신규 작업 아이템'}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')
    
    def test__redirects_after_POST(self):        
      
        response = self.client.post(
            '/lists/new',
            data = {'item_text': '신규 작업 아이템'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/only_list/')
    