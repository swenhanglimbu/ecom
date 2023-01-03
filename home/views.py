from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
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

class ProductDetailView(BaseView):
    def get(self,request,slug):
        self.views['product_detail'] = Product.objects.filter(slug = slug)
        subcat_id = Product.objects.get(slug = slug).subcategory_id
        product_id = Product.objects.get(slug = slug).id
        self.views['product_image'] = ProductImage.objects.filter(product_id=product_id)
        self.views['subcat_product'] = Product.objects.filter(subcategory_id=subcat_id)
        self.views['product_reviews'] = ProductReview.objects.filter(slug=slug)
        return render(request, 'product-detail.html', self.views)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username is already taken')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already taken')
                return redirect('/signup')
            else:
                data = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                data.save()
                return redirect('/accounts/login')
        else:
            messages.error(request, 'Password does not match !')
            return redirect('/signup')

    return render(request, 'signup.html')

def product_review(request,slug):
    if request.method == "POST":
        username = request.user.username
        email = request.user.email
        comment = request.POST['comment']
        star = request.POST['star']
        x = datetime.datetime.now()
        date = str(x.strftime("%c"))
        data = ProductReview.objects.create(
            username=username,
            email=email,
            comment=comment,
            star=star,
            date=date,
            slug=slug
        )
        data.save()
    return redirect(f'/details/{slug}')

def cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username,checkout=False).exists():
        quantity = Cart.objects.get(slug=slug, username=username,checkout=False).quantity
        price = Product.objects.get(slug=slug).price
        discounted_price =Product.objects.get(slug=slug).discounted_price
        quantity = quantity+1
        if discounted_price > 0:
            original_price = quantity * discounted_price
        else:
            original_price = quantity * price

        Cart.objects.filter(slug=slug, username=username, checkout=False).update(quantity=quantity,total=original_price)
        return redirect('/')
    else:
        price = Product.objects.get(slug=slug).price
        discounted_price = Product.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        data = Cart.objects.create(
            username=username,
            slug=slug,
            total=original_price,
            items=Product.objects.filter(slug=slug)[0]
        )
        data.save()
        return redirect('/')
