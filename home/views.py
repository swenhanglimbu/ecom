from django.shortcuts import render,redirect
from django.views.generic import View

from .models import *
# Create your views here.
class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
    views['sale_products'] = Product.objects.filter(labels='sale', stock='In stock')


class HomeView(BaseView):
    def get(self, request):
        self.views
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['new_products'] = Product.objects.filter(labels='new', stock='In stock')
        self.views['hot_products'] = Product.objects.filter(labels='hot', stock='In stock')
        self.views['sale_products'] = Product.objects.filter(labels='sale', stock='In stock')

        return render(request, 'index.html', self.views)

class CategoryView(BaseView):
    def get(self, request, slug):
        ids = Category.objects.get(slug=slug).id
        cat_name = Category.objects.get(slug=slug).name
        self.views['cat_product'] = Product.objects.filter(category_id=ids)

        return render(request, 'category.html', self.views)

class BrandView(BaseView):
    def get(self, request, slug):
        ids = Brand.objects.get(slug=slug).id
        self.views['brand_product'] = Product.objects.filter(brand_id=ids)

        return render(request, 'brand.html', self.views)

class SearchView(BaseView):
    def get(self, request):
        query = request.GET.get('query')
        if query !='':
            self.views['search_product'] = Product.objects.filter(name__icontains=query)
        else:
            return redirect('/')

        return render(request, 'search.html', self.views)