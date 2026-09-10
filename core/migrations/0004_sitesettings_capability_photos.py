from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_sitesettings_partner_logos'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='capability_photos',
            field=models.JSONField(blank=True, default=dict, help_text='Capability example photos keyed by capability name'),
        ),
    ]