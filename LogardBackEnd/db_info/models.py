from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.

class User ( models.Model ):
    name = models.CharField( max_length=100 )
    surname = models.CharField( max_length=100 )
    email = models.CharField( max_length=100, unique=True )
    password = models.CharField( max_length=255 )
    role = models.CharField( max_length=20 , default='user' )
    confirmed = models.BooleanField( default=False )
    token = models.CharField( max_length=255 )
    token_exp = models.DateTimeField( null=True, blank=True )

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id} by {self.user.email}'

class RowsOrder(models.Model):
    units = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

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


