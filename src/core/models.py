from django.db import models
from django.conf import settings
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse
from django.utils.html import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug= models.SlugField()
    image=models.ImageField(upload_to="category_imgs/",null=True)
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def get_absolute_url(self):
        return reverse('core:category', args=[self.slug])

    class Meta:
        verbose_name_plural='2. Categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category=models.ForeignKey('Category',on_delete=models.CASCADE,related_name='subcategories')
    name=models.CharField(max_length=100,unique=True)
    slug= models.SlugField()
    
    def get_absolute_url(self):
        return reverse('core:subcategory', args=[self.slug])

    class Meta:
        verbose_name_plural='3. Subcategory'
        unique_together = (
            ('category', 'name'),          # since slug is based on name,
                                           # we are sure slug will be unique too
        )

    def __str__(self):
        return self.name

class Brand(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    slug= models.SlugField()

    def get_absolute_url(self):
        return reverse('core:brands', args=[self.slug])


    class Meta:
        verbose_name_plural='4 Brands'

    def __str__(self):
        return self.name

LABEL_CHOICES = (
    ('b','blue'),
    ('r','red'),
)


class Item(models.Model):
    status=models.BooleanField(default=False)
    title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=400)
    category =models.ForeignKey('Category',on_delete=models.CASCADE)
    brand =models.ForeignKey('Brand',on_delete=models.CASCADE)
    subcategory = models.ForeignKey("SubCategory",on_delete=models.CASCADE)
    description =models.TextField()
    price=models.PositiveIntegerField(default=500)
    discount_price=models.PositiveIntegerField(default=0,null=True,blank=True)
    image=models.ImageField(upload_to="product_imgs/",null=True)
    label = models.CharField(choices=LABEL_CHOICES,max_length=2,null=True,blank=True)
    label_text=models.CharField(blank=True,null=True,max_length=10)

    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def get_absolute_url(self):
        return reverse('core:product', kwargs={'slug': self.slug})
    def get_add_to_cart_url(self):
        return reverse('core:add_to_cart', kwargs={'slug': self.slug})
    def get_remove_from_cart_url(self):
        return reverse('core:remove_from_cart', kwargs={'slug': self.slug})
    def get_remove_item_cart_url(self):
        return reverse('core:remove_item_cart', kwargs={'slug': self.slug})
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='5. Products'


#link of item to cart
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def get_discount_percentage(self):
        if self.item.discount_price:
            a= 100*(self.item.price -self.item.discount_price)/self.item.price
            return a

    
    class Meta:
        verbose_name_plural='6. orderd Items'
#cart
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        #if self.coupon:
        #    total -= self.coupon.amount
        return total
    class Meta:
        verbose_name_plural='7. Order'

RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

ADDRESS_CHOICES = (
    ('P','Pickup'),
    ('S', 'Delivery'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    phone_no =PhoneNumberField()
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
    
    class Meta:
        verbose_name_plural='8. Adddress'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural='9. Payment'


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=9, decimal_places=2,blank=True,null=True)

    def __str__(self):
        return self.code
    class Meta:
        verbose_name_plural='10. Coupon'



class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
    
    class Meta:
        verbose_name_plural='11 Refund'

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Item,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'