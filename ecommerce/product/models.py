import os
import uuid

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    id = models.UUIDField(
        verbose_name='ID da categoria', primary_key=True, default=uuid.uuid4,
        editable=False
    )
    name = models.CharField('nome', max_length=60)
    slug = models.SlugField('slug', unique=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField('criado em', auto_now_add=True)
    modified = models.DateTimeField('modificado em', auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    class Meta:
        ordering = ['created']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


def product_image_directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return '{0}/product/{1}{2}'.format(instance.slug, name, extension)


class Product(models.Model):
    id = models.UUIDField(
        verbose_name='ID do produto', primary_key=True, default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(
        'product.Category', verbose_name='categoria', on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField('nome', max_length=60)
    slug = models.SlugField('slug', unique=True, db_index=True)
    description = models.TextField('descrição', null=True, blank=True)
    value = models.DecimalField('valor', max_digits=22, decimal_places=16)
    stock = models.PositiveIntegerField('quantidade em estoque', default=0)
    image = models.ImageField(
        verbose_name='imagem', upload_to=product_image_directory_path,
        null=True, blank=True
    )
    created = models.DateTimeField('criado em', auto_now_add=True)
    modified = models.DateTimeField('modificado em', auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
