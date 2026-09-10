from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sitesettings_alter_workproject_hero_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='partner_logos',
            field=models.JSONField(blank=True, default=list, help_text='Partner logo URLs or image data URIs displayed in the landing reel'),
        ),
    ]