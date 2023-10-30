from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    picture =  models.ImageField(verbose_name="عکس", upload_to="upload/product/")
    name = models.CharField(verbose_name="نام محصول", max_length=40)
    quantity = models.IntegerField(verbose_name="تعداد")
    price = models.DecimalField(verbose_name="قیمت", default=0, decimal_places=0, max_digits=12)


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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return self.name
