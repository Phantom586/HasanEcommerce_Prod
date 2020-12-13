# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    name = models.CharField(db_column='Name', primary_key=True, max_length=150)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categories'
        unique_together = (('name', 'gender'),)

    def __str__(self):
        return f'{self.name} | {self.gender}'


class Clothing(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    brand_name = models.CharField(db_column='Brand_Name', max_length=255)  # Field name made lowercase.
    product_name = models.CharField(db_column='Product_Name', max_length=256)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=5)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clothing'

    def __str__(self):
        return f'{self.id} | {self.product_name} | {self.quantity}'


class Color(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=7)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'color'
        unique_together = (('id', 'name'),)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Size(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'size'
        unique_together = (('id', 'name'),)

    def __str__(self):
        return f'{self.id} | {self.name}'


class ProductImages(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_images'
        unique_together = (('id', 'name'),)

    def __str__(self):
        return f'{self.id} | {self.name}'
