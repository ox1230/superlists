from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "빈 아이템을 등록할 수 없습니다"

class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder':'작업아이템 입력',
                'class' : 'form-control input-lg',
                'id' : 'id_text',
            })
        }
        error_messages = {
            'text' : {'required':EMPTY_LIST_ERROR}
        }
