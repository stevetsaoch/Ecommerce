from django.conf import settings
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.full_name


class Image(models.Model):
    image = models.ImageField(upload_to="images/product_img/", default="images/product_img/product_default.png")
    image_name = models.CharField(max_length=255, blank=False, default="book_img")

    def __str__(self):
        return self.image_name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name="product_author")
    description = models.TextField(blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="product_image")
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    inventory = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title
