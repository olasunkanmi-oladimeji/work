from core import views
from core import filters
from django.urls import path



app_name='core'

urlpatterns = [

    path('',views.homepage,name='home'),
    path('About-us',views.aboutpage,name='about'),
    path('Contact-us',views.contactpage,name='contact'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('product/<slug>/',views.ProductPage,name='product'),
    #cart function
    path('order-summary',views.ordersummary.as_view(),name='order-summary'),
    path("confirm_order/", views.confirm_order, name="confirm_order"),
    path('Add-To-cart/<slug>',views.add_to_cart,name='add_to_cart'),
    path('Remove-FROM-cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
    path('Remove-Item-cart/<slug>',views.remove_single_item_from_cart,name='remove_item_cart'),
    #checkout
    path('checkout',views.CheckoutView.as_view(),name='checkout'),
    path('payment/<payment_option>',views.Paymentview.as_view(),name='payment'),
    path('payment/verify/<id>',views.verify,name='verify'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/',views.RequestRefundView.as_view(), name='request-refund'),
    #filter functions
    path('search/',filters.search,name='search'),
    path('filter_data/',filters.filter_data,name='filter_data'),
    path('product-category/<slug:category_slug>',filters.category,name='category'),
    path('product-subcatgory/<slug:subcategory_slug>/',views.subcategory,name='subcategory'),
    path('product-brands/<slug:brand_slug>/',views.Brandeds,name='brands'),
    path('filter/price/',views.price,name='price'),
    path('filter/product-instock/',views.instock,name='instock'),
    path('add-wishlist/<id>',views.add_wishlist, name='add_wishlist'),
    path('delete-item-wishlist/<id>',views.delete_wishlist, name='delete_wishlist'),

]

