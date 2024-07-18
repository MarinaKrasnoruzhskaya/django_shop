from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, Contact


class ProductListView(ListView):
    model = Product


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


class ProductDetailView(DetailView):
    model = Product
