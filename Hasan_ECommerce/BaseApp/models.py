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
    product_desc = models.CharField(db_column='Product_Desc', max_length=255)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=15)  # Field name made lowercase.
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


class InvoiceTable(models.Model):
    receipt_no = models.BigAutoField(db_column='Receipt_No', primary_key=True)  # Field name made lowercase.
    txn_id = models.CharField(db_column='Txn_ID', max_length=255)  # Field name made lowercase.
    order_id = models.CharField(db_column='Order_ID', max_length=255)  # Field name made lowercase.
    payment_mode = models.CharField(db_column='Payment_Mode', max_length=50)  # Field name made lowercase.
    user = models.CharField(db_column='User', max_length=13)  # Field name made lowercase.
    total_mrp = models.FloatField(db_column='Total_MRP')  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice_table'

    def __str__(self):
        return f'{self.receipt_no} | {self.user} | {self.timestamp}'


class BasketTable(models.Model):
    user_id = models.IntegerField(db_column='User_ID', primary_key=True)  # Field name made lowercase.
    cloth_id = models.IntegerField(db_column='Cloth_ID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp')  # Field name made lowercase.
    mrp = models.FloatField(db_column='MRP')  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=5)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=50)  # Field name made lowercase.
    total_mrp = models.FloatField(db_column='Total_MRP')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'basket_table'
        unique_together = (('user_id', 'cloth_id'),)

    def __str__(self):
        return f'{self.user} | {self.cloth_id} | {self.quantity}'


class UserTable(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    phone_no = models.CharField(db_column='Phone_No', max_length=13)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=60)  # Field name made lowercase.
    signup_timestamp = models.DateTimeField(db_column='SignUp_Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_table'

    def __str__(self):
        return f'{self.id} | {self.name}'