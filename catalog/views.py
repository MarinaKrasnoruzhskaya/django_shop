from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Product, Contact


class ProductListView(ListView):
    """Контроллер для списка продуктов"""
    model = Product


class ProductDetailView(DetailView):
    """Контроллер для просмотра конкретного продукта"""
    model = Product


class ProductCreateView(CreateView):
    """Контроллер для добавления нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    """Контроллер для редактирования продукта"""
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_contacts"] = Contact.objects.all()[:5]
        return context

    def post(self, request, **kwargs):
        if request.method == 'POST':
            contact = Contact()
            contact.name = request.POST.get('name')
            contact.phone = request.POST.get('phone')
            contact.message = request.POST.get('message')
            contact.save()

        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)
