# Generated by Django 4.0.3 on 2022-05-02 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_order_razorpay_order_id_order_razorpay_pay_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='razorpay_amount_total',
            field=models.IntegerField(default=0),
        ),
    ]