from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    picture =  models.ImageField(verbose_name="عکس محصول", upload_to="upload/product/", null=True, blank=True)
    name = models.CharField(verbose_name="نام محصول", max_length=40)
    quantity = models.IntegerField(verbose_name="موجودی محصول", default=0)
    price = models.DecimalField(verbose_name="قیمت محصول", max_digits=12, decimal_places=2)


    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = (
        ("1", "سبد خرید"),
        ("2", "در انتظار پرداخت"),
        ("3", "در انتظار تایید"),
        ("4", "در حال ارسال"),
        ("5", "تحویل شد"),
        ("6", "انصراف داده شد"),
    )
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="کاربر", on_delete=models.CASCADE)
    order_full_price = models.PositiveBigIntegerField(verbose_name="قیمت کل سفارش", default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")

    def update_price(self):
        order_items = self.orderitem_set.all()
        sum_price = 0
        for i in order_items:
            sum_price += ((i.product.price - i.product.discount) * i.product_count)
        self.order_full_price = sum_price
        self.save()


    @classmethod
    def get_basket(cls, user):
        basket = cls.objects.filter(user=user.id, status="1")
        if basket.exists():
            return basket.get()
        return None


    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return self.name
    

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="محصول")
    product_price = models.PositiveBigIntegerField(verbose_name="قیمت محصول")
    product_discount = models.PositiveBigIntegerField(
        verbose_name="تخفیف محصول", default=0)
    product_count = models.IntegerField(verbose_name="تعداد محصول")


    def get_actual_price(self):
        if self.product.discount:
            return self.product.price - self.product.discount
        else:
            return self.product.price

    @classmethod
    def add(cls, order, product, count):
        prod = Product.objects.get(pk=product)
        data = cls.objects.filter(order=order, product__id=product)
        if data.exists():
            my_order_item = data.get()
            my_order_item.product_price = my_order_item.product.price
            my_order_item.product_discount = my_order_item.product.discount
            my_order_item.product_count = my_order_item.product_count + 1
            my_order_item.save()
            my_order_item.order.update_price()
            return True
        else:
            instance = cls(order=order, product_price=prod.price, product_discount=prod.discount, product=prod, product_count=count)
            instance.save()
            instance.order.update_price()
            return True

    @classmethod
    def remove(cls, order, product, count):
        data = cls.objects.filter(order=order, product__id=product)
        if data.exists():
            my_order_item = data.get()
            if my_order_item.product_count - count <= 0:
                target_order = my_order_item.order
                my_order_item.delete()
                target_order.update_price()
                return True
            else:

                my_order_item.product_count -= count
                my_order_item.save()
                my_order_item.order.update_price()
                return True
        else:
            return False

    class Meta:
        verbose_name = "آیتم"
        verbose_name_plural = "آیتم‌ها"
