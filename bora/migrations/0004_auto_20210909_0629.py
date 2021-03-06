# Generated by Django 3.2.6 on 2021-09-09 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bora', '0003_auto_20210906_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='exhreview',
        ),
        migrations.AddField(
            model_name='product',
            name='exhinfo',
            field=models.TextField(max_length=200, null=True, verbose_name='전시 정보'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exhreview', models.TextField(max_length=200, verbose_name='전시 리뷰')),
                ('exhibit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bora.product', verbose_name='리뷰 전시회')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bora.user', verbose_name='리뷰 작성자')),
            ],
            options={
                'verbose_name': '리뷰',
                'verbose_name_plural': '리뷰',
                'db_table': 'Review',
            },
        ),
    ]
