# Generated manually for partners gallery layout.

from django.db import migrations, models


def assign_partner_placements(apps, schema_editor):
    HomePartner = apps.get_model("pages", "HomePartner")
    HomePartnersSection = apps.get_model("pages", "HomePartnersSection")
    for section in HomePartnersSection.objects.all():
        if not section.label:
            section.label = "Our Partners"
            section.label_en = section.label_en or "Our Partners"
            section.save(update_fields=["label", "label_en"])
        partners = list(
            HomePartner.objects.filter(section_id=section.pk).order_by("order", "id")
        )
        for index, partner in enumerate(partners):
            if index == 0:
                partner.placement = "featured_wide"
            elif index == 1:
                partner.placement = "featured_tall"
            else:
                partner.placement = "slider"
            partner.save(update_fields=["placement"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0038_final_word_paragraphs"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepartnerssection",
            name="label",
            field=models.CharField(
                blank=True,
                help_text='Example: "Our Partners" / «شركاؤنا».',
                max_length=120,
                verbose_name="Small label above the title",
            ),
        ),
        migrations.AddField(
            model_name="homepartnerssection",
            name="label_en",
            field=models.CharField(
                blank=True,
                help_text='Example: "Our Partners" / «شركاؤنا».',
                max_length=120,
                null=True,
                verbose_name="Small label above the title",
            ),
        ),
        migrations.AddField(
            model_name="homepartnerssection",
            name="label_ar",
            field=models.CharField(
                blank=True,
                help_text='Example: "Our Partners" / «شركاؤنا».',
                max_length=120,
                null=True,
                verbose_name="Small label above the title",
            ),
        ),
        migrations.AddField(
            model_name="homepartner",
            name="tag",
            field=models.CharField(
                blank=True,
                help_text='Example: "Metallurgy" / «شريك». Shown as the small badge on hover.',
                max_length=80,
                verbose_name="Small tag (on hover)",
            ),
        ),
        migrations.AddField(
            model_name="homepartner",
            name="tag_en",
            field=models.CharField(
                blank=True,
                help_text='Example: "Metallurgy" / «شريك». Shown as the small badge on hover.',
                max_length=80,
                null=True,
                verbose_name="Small tag (on hover)",
            ),
        ),
        migrations.AddField(
            model_name="homepartner",
            name="tag_ar",
            field=models.CharField(
                blank=True,
                help_text='Example: "Metallurgy" / «شريك». Shown as the small badge on hover.',
                max_length=80,
                null=True,
                verbose_name="Small tag (on hover)",
            ),
        ),
        migrations.AddField(
            model_name="homepartner",
            name="link_url",
            field=models.URLField(blank=True, verbose_name="Link (optional)"),
        ),
        migrations.AddField(
            model_name="homepartner",
            name="placement",
            field=models.CharField(
                choices=[
                    ("featured_wide", "Top left — wide image (898×450)"),
                    ("featured_tall", "Top right — tall image (868×900)"),
                    ("slider", "Bottom slider — same size"),
                ],
                default="slider",
                help_text="Use one wide + one tall on top. The rest (up to 6) go in the slider.",
                max_length=20,
                verbose_name="Position",
            ),
        ),
        migrations.AlterField(
            model_name="homepartner",
            name="logo",
            field=models.ImageField(
                blank=True,
                help_text="Top left: 898×450. Top right: 868×900. Slider items: same size, e.g. 868×450.",
                null=True,
                upload_to="partners/",
                verbose_name="Image",
            ),
        ),
        migrations.AlterField(
            model_name="homepartner",
            name="name",
            field=models.CharField(
                help_text="The larger line under the tag, e.g. the partner name.",
                max_length=160,
                verbose_name="Title (on hover)",
            ),
        ),
        migrations.AlterField(
            model_name="homepartner",
            name="name_en",
            field=models.CharField(
                help_text="The larger line under the tag, e.g. the partner name.",
                max_length=160,
                null=True,
                verbose_name="Title (on hover)",
            ),
        ),
        migrations.AlterField(
            model_name="homepartner",
            name="name_ar",
            field=models.CharField(
                help_text="The larger line under the tag, e.g. the partner name.",
                max_length=160,
                null=True,
                verbose_name="Title (on hover)",
            ),
        ),
        migrations.RunPython(assign_partner_placements, noop_reverse),
    ]
