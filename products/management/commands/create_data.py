from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete()
        products_to_create = []

        categories = [
            "tech",
            "electronics",
            "home",
        ]
        category_objects = [
            Category.objects.get_or_create(name=name)[0] for name in categories
        ]

        for i in range(options["count"]):
            price = i * 10
            products_to_create.append(
                Product(
                    name=f"Item {i}",
                    price_amount=price,
                    description="test description",
                ),
            )

        Product.objects.bulk_create(products_to_create)

        for i, product in enumerate(products_to_create):
            product.category.set([category_objects[i % len(category_objects)]])

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, help="Number of products to create", default=5
        )
