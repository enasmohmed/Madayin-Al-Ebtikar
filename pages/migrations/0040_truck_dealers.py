from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0039_partners_gallery"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeTruckDealersSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text='Example: "Truck dealers" / «وكلاء الشاحنات».',
                        max_length=120,
                        verbose_name="Small label above the title",
                    ),
                ),
                (
                    "label_en",
                    models.CharField(
                        blank=True,
                        help_text='Example: "Truck dealers" / «وكلاء الشاحنات».',
                        max_length=120,
                        null=True,
                        verbose_name="Small label above the title",
                    ),
                ),
                (
                    "label_ar",
                    models.CharField(
                        blank=True,
                        help_text='Example: "Truck dealers" / «وكلاء الشاحنات».',
                        max_length=120,
                        null=True,
                        verbose_name="Small label above the title",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=200, verbose_name="Section title")),
                ("title_en", models.CharField(blank=True, max_length=200, null=True, verbose_name="Section title")),
                ("title_ar", models.CharField(blank=True, max_length=200, null=True, verbose_name="Section title")),
                (
                    "language",
                    models.CharField(
                        choices=[("en", "English"), ("ar", "Arabic")],
                        default="en",
                        max_length=5,
                        verbose_name="Language row",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible")),
            ],
            options={
                "verbose_name": "Home — truck dealers",
                "verbose_name_plural": "Home — truck dealers",
            },
        ),
        migrations.CreateModel(
            name="HomeTruckDealer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "title",
                    models.CharField(
                        help_text="Shown on the image (hover).",
                        max_length=160,
                        verbose_name="Title",
                    ),
                ),
                (
                    "title_en",
                    models.CharField(
                        help_text="Shown on the image (hover).",
                        max_length=160,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "title_ar",
                    models.CharField(
                        help_text="Shown on the image (hover).",
                        max_length=160,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Same size for all cards. Recommended: 768×889.",
                        null=True,
                        upload_to="truck_dealers/",
                        verbose_name="Image",
                    ),
                ),
                ("link_url", models.URLField(blank=True, verbose_name="Link (optional)")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible")),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dealers",
                        to="pages.hometruckdealerssection",
                        verbose_name="Section",
                    ),
                ),
            ],
            options={
                "verbose_name": "Truck dealer",
                "verbose_name_plural": "Truck dealers",
                "ordering": ["order", "id"],
            },
        ),
    ]
