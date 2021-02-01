# Generated by Django 3.1.3 on 2021-01-24 18:27

from django.db import migrations, models
import django.db.models.deletion
import main.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_bb'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bb',
            options={'ordering': ['-created_at'], 'verbose_name': 'Объявления', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=main.utilities.get_timestamp_path, verbose_name='Изображения')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bb', verbose_name='Объявления')),
            ],
            options={
                'verbose_name': 'Дополнительная иллюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
    ]