from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item,List
from lists.forms import ItemForm
import re

class HomePageTest(TestCase):
  
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    @staticmethod
    def remove_csrf_tag(text):
        """Remove csrf tag from TEXT"""
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class NewListTest(TestCase):
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data = {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = "빈 아이템을 등록할 수 없습니다"
        self.assertContains(response , expected_error)


    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new',data = {'text':''})
        
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))   #/를 붙이자 !! ㅜㅜ
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = 'item1', list = correct_list)
        Item.objects.create(text = 'item2', list = correct_list)

        other_list = List.objects.create()
        Item.objects.create(text = 'other item1', list = other_list)
        Item.objects.create(text = 'other item2', list = other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response,'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other item1')
        self.assertNotContains(response, 'other item2')
    
    def test_saving_a_POST_request(self):
        
        self.client.post(
            '/lists/new',   #뒤에 꼬리슬래시를 사용하지 않는 것은 데이터베이스에 변경을 가하는 "액션" URL
            data = {'text': '신규 작업 아이템'}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')
    
    def test_redirects_after_POST(self):        
      
        response = self.client.post(
            '/lists/new',
            data = {'text': '신규 작업 아이템'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data = {'text': '기존 목록에 신규 아이템'}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "기존 목록에 신규 아이템")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data = {'text': '기존 목록에 신규 아이템'}
        )

        self.assertRedirects(response , '/lists/{}/'.format(correct_list.id))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/{}/'.format(list_.id),
            data = {'text':''}
        )

        self. assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = "빈 아이템을 등록할 수 없습니다"
        self.assertContains(response, expected_error)