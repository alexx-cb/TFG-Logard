from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import PROTECT

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Must introduce an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'


class Category ( models.Model ):
    name = models.CharField( max_length=250, unique=True )

    def __str__(self):
        return self.name


class Product ( models.Model ):
    name = models.CharField( max_length=100, unique=True )
    description = models.TextField( null=True, blank=True )
    price = models.DecimalField( max_digits=10, decimal_places=2 )
    discount = models.DecimalField( max_digits=10, decimal_places=2, default=0 )
    image = models.ImageField( upload_to='products/', blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])] )
    category = models.ForeignKey(Category, on_delete=PROTECT)

    def __str__(self):
        return self.name

class Order(models.Model):
    address = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=PROTECT)

    def __str__(self):
        return f'Order #{self.id} by {self.user.email}'

class RowsOrder(models.Model):
    units = models.IntegerField()
    size = models.CharField(max_length=255, default='M')
    order = models.ForeignKey(Order, on_delete=PROTECT)
    product = models.ForeignKey(Product, on_delete=PROTECT)

    def __str__(self):
        return f'{self.units} x {self.product.name} (Order #{self.order.id})'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'Cart of {self.user.email}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.units} x {self.product.name} (Cart of {self.cart.user.email})'


