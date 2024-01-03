from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = first_name = models.CharField(max_length=30,blank=False,null=False)
    last_name = models.CharField(max_length=30,blank=False,null=False)
    email = models.EmailField(max_length=254,blank=False,null=False)
    phone = models.CharField(max_length=10,blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='address')
    address_line_1 = models.CharField(max_length=100,blank=False,null=False)
    address_line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50,blank=False,null=False)
    state = models.CharField(max_length=30,blank=False,null=False)
    zip = models.CharField(max_length=6,blank=False,null=False)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,blank=False,null=False)
    image = models.ImageField(upload_to='images/',blank=False,null=False)
    cost = models.PositiveBigIntegerField(blank=False,null=False)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField()

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,blank=False,null=False)

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='review')
    rating = models.PositiveSmallIntegerField(blank=False,null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='like')
    review_id = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='like_review')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'review_id'], name='unique_like')
        ]

class DisLike(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='dislike')
    review_id = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='dislike_review')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'review_id'], name='unique_dislike')
        ]