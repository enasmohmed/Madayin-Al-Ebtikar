from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0043_base_partners_label_optional"),
    ]

    operations = [
        migrations.DeleteModel(name="HomeBasePartner"),
        migrations.DeleteModel(name="HomeBasePartnersSection"),
    ]
