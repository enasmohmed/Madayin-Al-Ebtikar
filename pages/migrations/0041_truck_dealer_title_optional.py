from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0040_truck_dealers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hometruckdealer",
            name="title",
            field=models.CharField(
                blank=True,
                help_text="Optional. Shown on the image (hover).",
                max_length=160,
                verbose_name="Title",
            ),
        ),
        migrations.AlterField(
            model_name="hometruckdealer",
            name="title_en",
            field=models.CharField(
                blank=True,
                help_text="Optional. Shown on the image (hover).",
                max_length=160,
                null=True,
                verbose_name="Title",
            ),
        ),
        migrations.AlterField(
            model_name="hometruckdealer",
            name="title_ar",
            field=models.CharField(
                blank=True,
                help_text="Optional. Shown on the image (hover).",
                max_length=160,
                null=True,
                verbose_name="Title",
            ),
        ),
    ]
