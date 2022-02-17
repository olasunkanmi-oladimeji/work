import imp
from itertools import product
from django.shortcuts import render,get_object_or_404
from .models import (Banner,Category,SubCategory,Item,
                        OrderItem,Order,Address,Brand,Payment,
                        Coupon,Refund,Wishlist)
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth


from django.http import JsonResponse,HttpResponse
# Filter Data

def category(request,category_slug):
    #Category
    categories = Category.objects.all().order_by('name')
    category = None
    subcategory =SubCategory.objects.all().order_by('name')
    branded =Brand.objects.all().order_by('name')
    items=Item.objects.all().order_by('-id')
    minprice = request.GET.get('minPrice')
    maxprice = request.GET.get('maxPrice')
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        item = items.filter(category=category)
        #sub_cat=subcategory.filter(category=category)
        #brands=branded.filter(category=category)
        
    #pagination and item
   

    page = request.GET.get('page', 1)

    paginator = Paginator(item, 12)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request,'shop.html',{   
                                                    'category':category,
                                                    'page_obj':page_obj,
                                                    #'sub_cat':sub_cat,
                                                    'categories' : categories,
                                                    #'brands':brands,
                                                    'subcategory  ':subcategory,
                                                    

                                                   } )

def filter_data(request):
    colors=request.GET.getlist('color[]')
    categories=request.GET.getlist('category[]')
    brands=request.GET.getlist('brand[]')
    sizes=request.GET.getlist('size[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts=Item.objects.all().order_by('-id').distinct()
    allProducts=allProducts.filter(price__gte=minPrice)
    allProducts=allProducts.filter(price__lte=maxPrice)
    if len(colors)>0:
        allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('shop.html',{'data':allProducts})
    return JsonResponse({'data':t})



def search(request):
    #subcategory = Category.objects.all().order_by('-id')
    items = Item.objects.all().order_by('-id')
    #branded=Brand.objects.all().order_by('name')

    #Search
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
        queryset = (Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(category__name__icontains=query)|
            Q(brand__name__icontains=query)|
            Q(subcategory__name__icontains=query))
        results =  Item.objects.filter(queryset).distinct()

    else:
       results = []

    return render(request, 'shop.html',{'results':results,
                                                'query':query,
                                                'page_obj':items,
                                                #'brand':branded

                                                   } )
