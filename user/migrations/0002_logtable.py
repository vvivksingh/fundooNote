

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hit_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('type_of_request', models.CharField(max_length=250)),
                ('response', models.CharField(max_length=200)),
            ],
        ),
    ]
