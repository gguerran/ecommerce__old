from datetime import datetime

from django.test import TestCase

from ecommerce.product.models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Teste')
        self.category.save()

    def test_create(self):
        self.assertTrue(Category.objects.exists())

    def test_str(self):
        self.assertEquals(str(self.category), 'Teste')

    def test_name_can_not_be_blank_and_null(self):
        field = Category._meta.get_field('name')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_slug_can_not_be_blank_and_null(self):
        field = Category._meta.get_field('slug')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_parent_can_be_blank_and_null(self):
        field = Category._meta.get_field('parent')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_name_value(self):
        self.assertEquals(self.category.name, 'Teste')

    def test_slug_value(self):
        self.assertEquals(self.category.slug, 'teste')

    def test_parent_value(self):
        self.assertEquals(self.category.parent, None)

    def test_created(self):
        self.assertIsInstance(self.category.created, datetime)

    def test_modified_at(self):
        self.assertIsInstance(self.category.modified, datetime)


class SubCategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Teste')
        self.category.save()
        self.subcategory = Category.objects.create(
            name='Sub teste', parent=self.category
        )

    def test_create(self):
        self.assertTrue(Category.objects.exists())

    def test_str(self):
        self.assertEquals(str(self.subcategory), 'Teste -> Sub teste')

    def test_name_value(self):
        self.assertEquals(self.subcategory.name, 'Sub teste')

    def test_slug_value(self):
        self.assertEquals(self.subcategory.slug, 'sub-teste')

    def test_parent_value(self):
        self.assertEquals(self.subcategory.parent, self.category)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Teste')
        self.category.save()
        self.product = Product.objects.create(
            category=self.category, name='Produto Teste',
            description='Lorem ipsum', value=15.5, stock=10
        )
        self.product.save()

    def test_create(self):
        self.assertTrue(Product.objects.exists())

    def test_str(self):
        self.assertEquals(str(self.product), 'Produto Teste')

    def test_category_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('category')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_name_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('name')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_slug_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('slug')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_description_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('description')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_value_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('value')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_stock_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('stock')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_image_can_not_be_blank_and_null(self):
        field = Product._meta.get_field('image')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_category_value(self):
        self.assertEquals(self.product.category, self.category)

    def test_name_value(self):
        self.assertEquals(self.product.name, 'Produto Teste')

    def test_slug_value(self):
        self.assertEquals(self.product.slug, 'produto-teste')

    def test_description_value(self):
        self.assertEquals(self.product.description, 'Lorem ipsum')

    def test_value_value(self):
        self.assertEquals(self.product.value, 15.5)

    def test_stock_value(self):
        self.assertEquals(self.product.stock, 10)

    def test_created(self):
        self.assertIsInstance(self.product.created, datetime)

    def test_modified(self):
        self.assertIsInstance(self.product.modified, datetime)
