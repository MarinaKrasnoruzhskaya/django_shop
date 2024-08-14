from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, VersionFormset, ProductModeratorForm
from catalog.models import Product, Contact, Version


class ProductListView(ListView):
    """Контроллер для списка продуктов"""
    model = Product

    def get_context_data(self, *args, **kwargs):
        """Метод для получения списка продуктов активной версии с последующей выборкой
        либо всех продуктов (для модератора),
        либо опубликованные продукты других пользователей и все свои продукты (для владельца продуктов),
        либо только опубликованные продукты (для всех остальных)"""
        context_data = super().get_context_data(*args, **kwargs)
        active_product_list = []
        for product in context_data['product_list']:
            product.current_version = Version.objects.filter(product=product, is_current_version=True).first()
            if product.current_version:
                product.active_version = product.current_version
            else:
                product.active_version = None
            active_product_list.append(product)

        user = self.request.user
        user_products = user.product_set.all() if user.id else []
        if user.has_perm("catalog.can_cancel_publication"):
            context_data['object_list'] = active_product_list
            return context_data
        elif not user_products:
            published_product_list = []
            for product in active_product_list:
                if product.is_published:
                    published_product_list.append(product)
            context_data['object_list'] = published_product_list
            return context_data
        else:
            product_list = []
            for product in active_product_list:
                if product.is_published or product in user_products:
                    product_list.append(product)
            context_data['object_list'] = product_list
            return context_data


class ProductDetailView(DetailView):
    """Контроллер для просмотра конкретного продукта и его версий"""
    model = Product

    def get_context_data(self, **kwargs):
        """Метод для получения данных о продукте и его версиях"""
        context_data = super().get_context_data(**kwargs)
        context_data['versions'] = Version.objects.filter(product=self.object)
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для добавления нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        """Метод для получения контекста страницы редактирования"""
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormset, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form, **kwargs):
        """Метод для автоматической привязки владельца продукта - пользователя"""
        product = form.save()
        product.user = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования продукта"""
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        """Метод для получения контекста страницы редактирования"""
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormset, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form, **kwargs):
        """Метод для проверки валидации формы"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Метод для отображения страницы редактирования с ошибками валидации"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        """Метод для перехода на страницу продукта после его изменения"""
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """Метод для получения класса формы продукта в зависимости от прав доступа авторизованного пользователя"""
        user = self.request.user
        if user == self.object.user:
            return ProductForm
        if user.has_perm("catalog.can_cancel_publication") and user.has_perm(
                "catalog.can_change_description") and user.has_perm("catalog.can_change_category"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер для удаления продукта"""
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        """Метод для проверки прав доступа на удаление продукта"""
        product = Product.objects.get(pk=self.kwargs['pk'])
        return self.request.user.is_superuser or self.request.user.pk == product.user.pk


class ContactsView(TemplateView):
    """Контроллер для страницы контактов"""
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
