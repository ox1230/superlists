from django import forms
from lists.models import Item,List

EMPTY_LIST_ERROR = "빈 아이템을 등록할 수 없습니다"

class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
               'required': False,
                'placeholder':'작업아이템 입력',
                'id' : 'id_text',
                'class' : "form-control input-lg",
                })
        }

        error_messages = {
            'text' : {'required':EMPTY_LIST_ERROR}
        }
   
    def save(self, for_list:List):
        self.instance.list = for_list
        return super().save()