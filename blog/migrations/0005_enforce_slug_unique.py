from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0004_populate_post_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=120, unique=True, blank=True, null=False),
        ),
    ]
