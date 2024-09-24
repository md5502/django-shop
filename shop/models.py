from django.db import models

from account.models import User
from common.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="categories")

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    DISCOUNT_CHOICES = (
        ("N", "None"),
        ("P", "Percent"),
        ("A", "Amount"),
    )
    name = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    sku = models.CharField(max_length=100)
    categories = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.FloatField()
    img = models.ImageField(upload_to="media", default="product_default.png")
    tags = models.ManyToManyField(Tag, related_name="products")
    discount_type = models.CharField(max_length=1, choices=DISCOUNT_CHOICES, default=DISCOUNT_CHOICES[0][0])
    discount_value = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self) -> str:
        return f"{self.user}, {self.product}"


class Cart(BaseModel):
    CART_CHOICES = (
        ("A", "active"),
        ("O", "ordered"),
        ("B", "abandoned"),
    )
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=CART_CHOICES, default=CART_CHOICES[0][0])

    def __str__(self) -> str:
        return f"{self.created_by}, {self.status}"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.cart}, {self.product}"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user


class OrderLine(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_lines")
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.order}, {self.product}"
