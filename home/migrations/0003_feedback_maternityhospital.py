# Generated by Django 3.0.4 on 2020-03-10 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_delete_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaternityHospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('maternity_hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.MaternityHospital')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.User')),
            ],
        ),
    ]
