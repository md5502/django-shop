import random
from io import BytesIO

import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker

from account.models import User
from shop.models import Cart, CartItem, Category, Order, OrderLine, Product, Review, Tag


class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
            )
            users.append(user)

        # Create Tags
        tags = []
        for _ in range(10):
            tag = Tag.objects.create(name=fake.word())
            tags.append(tag)

        # Create Categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.word(),
                slug=fake.slug(),
                description=fake.text(),
            )
            category.tags.set(random.sample(tags, k=3))
            categories.append(category)

        # Create Products
        products = []
        for _ in range(20):
            # Download and save image
            image_url = fake.image_url()
            response = requests.get(image_url)
            if response.status_code == 200:
                img_temp = BytesIO(response.content)
                img_filename = f"product_{fake.uuid4()}.jpg"

                product = Product.objects.create(
                    name=fake.word(),
                    summary=fake.text(),
                    description=fake.text(),
                    sku=fake.unique.ean(length=8),
                    categories=random.choice(categories),
                    price=random.uniform(10.0, 100.0),
                    discount_type=random.choice(["N", "P", "A"]),
                    discount_value=random.uniform(0.0, 50.0) if random.choice([True, False]) else None,
                )

                product.img.save(img_filename, File(img_temp), save=True)
                product.tags.set(random.sample(tags, k=3))
                products.append(product)
            else:
                self.stdout.write(self.style.WARNING(f"Failed to download image for product {product.name}"))

        # Create Reviews
        for _ in range(50):
            Review.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                rating=random.randint(1, 5),
                comment=fake.text(),
            )

        # Create Carts and CartItems
        for user in users:
            cart = Cart.objects.create(
                created_by=user,
                status=random.choice(["A", "O", "B"]),
            )
            for _ in range(random.randint(1, 5)):
                CartItem.objects.create(
                    cart=cart,
                    product=random.choice(products),
                    price=random.uniform(10.0, 100.0),
                    quantity=random.randint(1, 5),
                )

        # Create Orders and OrderLines
        for user in users:
            order = Order.objects.create(user=user)
            for _ in range(random.randint(1, 5)):
                OrderLine.objects.create(
                    order=order,
                    product=random.choice(products),
                    price=random.uniform(10.0, 100.0),
                    quantity=random.randint(1, 5),
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated the database with fake data"))
