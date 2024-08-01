from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, BaseInlineFormSet, CheckboxInput

from catalog.models import Product, Version


class StyleFormMixin:
    """Миксин для стилизации формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif not isinstance(field, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    """Форма для добавления нового продукта"""
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    def clean_name(self):
        """Метод для проверки наличия запрещенных слов в названии продукта"""
        cleaned_data = self.cleaned_data['name'].lower()
        for word in self.FORBIDDEN_WORDS:
            if word in cleaned_data:
                raise forms.ValidationError(f'Слово {word} нельзя использовать в названии продукта')

        return cleaned_data

    def clean_description(self):
        """Метод для проверки наличия запрещенных слов в описании продукта"""
        cleaned_data = self.cleaned_data['description'].lower()
        for word in self.FORBIDDEN_WORDS:
            if word in cleaned_data:
                raise forms.ValidationError(f'Слово {word} нельзя использовать в описании продукта')

        return cleaned_data


class VersionForm(StyleFormMixin, ModelForm):
    """Класс для добавления новой версии продукта"""
    class Meta:
        model = Version
        fields = '__all__'


class VersionFormset(BaseInlineFormSet):
    def clean(self):
        """Метод для проверки условия, что количество активных версий мржет быть только одна"""
        super().clean()
        count = 0
        for form in self.forms:
            if form.instance.is_current_version:
                count += 1
                if count > 1:
                    form.add_error(None, ValidationError("У продукта может быть только одна активная версия"))
                    break
