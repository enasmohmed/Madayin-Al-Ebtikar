from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline

import pages.translation  # noqa: F401 — قبل TranslationAdmin (تسجيل HeroSlide وغيره)

from .models import (
    HeroSlide,
    HeroSlideBackgroundImage,
    HeroBannerSettings,
    HeroOverlayImage,
    OurWorkImage,
    HomeOfferStrip,
    HomeOfferItem,
    HomeHighlightsSection,
    HomeHighlightItem,
    HomeServicesSection,
    HomeServiceCard,
    HomePartnersSection,
    HomePartner,
    HomeTruckDealersSection,
    HomeTruckDealer,
    MissionVisionValuesBlock,
    MVVPartnerLogo,
    MVVTabPanel,
    MVVTabBullet,
    FinalWordSection,
    FinalWordColumnLine,
)

class HeroOverlayImageInline(admin.TabularInline):
    model = HeroOverlayImage
    extra = 0
    ordering = ("order",)
    verbose_name = _("Bottom overlay image")
    verbose_name_plural = _("Bottom overlay images")


class HeroSlideInline(TranslationStackedInline):
    model = HeroSlide
    extra = 1
    ordering = ("order", "id")
    show_change_link = True
    fields = (
        "background_image",
        "tagline",
        "heading",
        "lead",
        "button_text",
        "button_link",
        "order",
        "is_active",
    )


@admin.register(HeroBannerSettings)
class HeroBannerSettingsAdmin(admin.ModelAdmin):
    """صف واحد: أضيفي شرائح السلايدر من هنا (صورة + نص + زر لكل شريحة)."""

    inlines = (HeroSlideInline, HeroOverlayImageInline)
    fieldsets = (
        (
            _("Video background (optional)"),
            {
                "classes": ("collapse",),
                "fields": ("prefer_video", "background_video", "external_video_url"),
                "description": _(
                    "Leave this closed to use the image slider. "
                    "Add each banner below: image, subtitle, heading, text, and button."
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not HeroBannerSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = HeroBannerSettings.objects.get_or_create(pk=1)
        return redirect(reverse("admin:pages_herobannersettings_change", args=[obj.pk]))


class HeroSlideBackgroundImageInline(admin.TabularInline):
    model = HeroSlideBackgroundImage
    extra = 0
    ordering = ("order",)
    verbose_name = _("Extra background (same text)")
    verbose_name_plural = _("Extra backgrounds (same text)")


@admin.register(HeroSlide)
class HeroSlideAdmin(TranslationAdmin):
    list_display = ("thumb", "heading", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("thumb", "heading")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    inlines = (HeroSlideBackgroundImageInline,)
    fieldsets = (
        (
            _("Banner image"),
            {
                "fields": ("background_image",),
                "description": _(
                    "This is the large photo behind the slide text. "
                    "Recommended size: 1920×950."
                ),
            },
        ),
        (
            _("Slide text"),
            {
                "fields": ("tagline", "heading", "lead"),
            },
        ),
        (
            _("Button"),
            {
                "fields": ("button_text", "button_link"),
            },
        ),
        (
            _("Display"),
            {
                "fields": ("order", "is_active", "foreground_image"),
            },
        ),
    )

    @admin.display(description=_("Image"))
    def thumb(self, obj):
        if not obj.background_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="96" height="48" '
            'style="object-fit:cover;border-radius:4px;background:#111"/>',
            obj.background_image.url,
        )


class HomeServiceCardInline(TranslationStackedInline):
    model = HomeServiceCard
    extra = 1
    ordering = ("order", "id")
    show_change_link = True
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "intro",
                    "points",
                    "link_url",
                    "order",
                    "is_featured",
                    "is_active",
                ),
                "description": _(
                    "«Points»: enter one bullet per line. "
                    "Example: «Excavation and backfill» on its own line."
                ),
            },
        ),
    )


@admin.register(HomeServicesSection)
class HomeServicesSectionAdmin(TranslationAdmin):
    list_display = ("title", "language", "is_active", "card_count", "side_image_thumb")
    list_filter = ("is_active", "language")
    inlines = (HomeServiceCardInline,)
    fieldsets = (
        (
            _("Section heading"),
            {"fields": ("label", "title", "subtitle", "footer_note")},
        ),
        (
            _("Side image"),
            {
                "fields": ("side_image",),
                "description": _(
                    "Big image on the right of the dark services band. "
                    "Each service has its own hover image inside its own box below."
                ),
            },
        ),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )

    @admin.display(description=_("Services"))
    def card_count(self, obj):
        return obj.cards.filter(is_active=True).count()

    @admin.display(description=_("Side image"))
    def side_image_thumb(self, obj):
        if not obj.side_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="48" height="56" '
            'style="object-fit:cover;border-radius:4px"/>',
            obj.side_image.url,
        )


@admin.register(HomeServiceCard)
class HomeServiceCardAdmin(TranslationAdmin):
    """Add or edit one service on its own page — name, text, bullet points."""

    list_display = ("title", "section", "intro", "order", "is_active")
    list_filter = ("section", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("section", "order", "id")
    fieldsets = (
        (
            None,
            {
                "fields": ("section", "title", "intro", "points", "link_url"),
                "description": _(
                    "The name is used in the admin only — the page shows the text "
                    "and the bullet points. «Points»: one bullet per line."
                ),
            },
        ),
        (_("Options"), {"fields": ("order", "is_featured", "is_active")}),
    )


class HomePartnerInline(TranslationStackedInline):
    model = HomePartner
    extra = 1
    ordering = ("order", "id")
    readonly_fields = ("thumb",)
    fields = (
        "thumb",
        "logo",
        "tag",
        "name",
        "placement",
        "link_url",
        "order",
        "is_active",
    )

    @admin.display(description=_("Preview"))
    def thumb(self, obj):
        if not obj.pk or not obj.logo:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="72" height="48" '
            'style="object-fit:cover;border-radius:4px"/>',
            obj.logo.url,
        )


@admin.register(HomePartnersSection)
class HomePartnersSectionAdmin(TranslationAdmin):
    list_display = ("title", "language", "is_active", "partner_count")
    list_filter = ("is_active", "language")
    inlines = (HomePartnerInline,)
    fieldsets = (
        (
            _("Section heading"),
            {
                "fields": ("label", "title", "subtitle"),
                "description": _(
                    "Small label (Our Partners) + title. "
                    "Add 8 partners below: 1 wide, 1 tall, and 6 in the slider. "
                    "Hover shows the tag then the title."
                ),
            },
        ),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )

    @admin.display(description=_("Partners"))
    def partner_count(self, obj):
        return obj.partners.filter(is_active=True).count()


class HomeTruckDealerInline(TranslationStackedInline):
    model = HomeTruckDealer
    extra = 1
    ordering = ("order", "id")
    readonly_fields = ("thumb",)
    fields = ("thumb", "image", "title", "link_url", "order", "is_active")

    @admin.display(description=_("Preview"))
    def thumb(self, obj):
        if not obj.pk or not obj.image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="48" height="64" '
            'style="object-fit:cover;border-radius:4px"/>',
            obj.image.url,
        )


@admin.register(HomeTruckDealersSection)
class HomeTruckDealersSectionAdmin(TranslationAdmin):
    list_display = ("title", "language", "is_active", "dealer_count")
    list_filter = ("is_active", "language")
    inlines = (HomeTruckDealerInline,)
    fieldsets = (
        (
            _("Section heading"),
            {
                "fields": ("label", "title"),
                "description": _(
                    "Dark slider like the theme: small label + title, then dealer "
                    "photos (same size, 768×889) with a title on each image."
                ),
            },
        ),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )

    @admin.display(description=_("Dealers"))
    def dealer_count(self, obj):
        return obj.dealers.filter(is_active=True).count()


class HomeOfferItemInline(TranslationStackedInline):
    model = HomeOfferItem
    extra = 1
    max_num = HomeOfferItem.MAX_ITEMS
    ordering = ("order", "id")
    fields = ("icon_class", "icon", "title", "text", "order", "is_active")

    def get_formset(self, request, obj=None, **kwargs):
        # Admin only hides the "add" link at max_num; this also rejects extras on save.
        kwargs["validate_max"] = True
        return super().get_formset(request, obj, **kwargs)


@admin.register(HomeOfferStrip)
class HomeOfferStripAdmin(admin.ModelAdmin):
    list_display = ("__str__", "language", "is_active", "item_count")
    list_filter = ("is_active", "language")
    inlines = (HomeOfferItemInline,)
    fieldsets = ((_("Visibility"), {"fields": ("language", "is_active")}),)

    @admin.display(description=_("Items"))
    def item_count(self, obj):
        return obj.items.filter(is_active=True).count()


class HomeHighlightItemInline(TranslationStackedInline):
    model = HomeHighlightItem
    extra = 0
    max_num = HomeHighlightItem.MAX_ITEMS
    ordering = ("order", "id")
    show_change_link = True
    fields = ("icon_class", "number", "title", "text", "order", "is_active")
    verbose_name = _("Stat card")
    verbose_name_plural = _("Stat cards (4 only)")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return HomeHighlightItem.MAX_ITEMS
        return max(0, HomeHighlightItem.MAX_ITEMS - obj.items.count())

    def get_formset(self, request, obj=None, **kwargs):
        kwargs["validate_max"] = True
        return super().get_formset(request, obj, **kwargs)


@admin.register(HomeHighlightsSection)
class HomeHighlightsSectionAdmin(TranslationAdmin):
    list_display = ("__str__", "language", "is_active", "item_count")
    list_filter = ("is_active", "language")
    inlines = (HomeHighlightItemInline,)
    fieldsets = (
        (
            _("Section heading"),
            {
                "fields": ("label", "title", "subtitle"),
                "description": _("Optional. Leave empty to show the four cards only."),
            },
        ),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )

    @admin.display(description=_("Cards"))
    def item_count(self, obj):
        return obj.items.filter(is_active=True).count()


@admin.register(HomeHighlightItem)
class HomeHighlightItemAdmin(TranslationAdmin):
    """Edit one stat card: Font Awesome icon, number, title, optional text."""

    list_display = ("icon_class", "number", "title", "section", "order", "is_active")
    list_editable = ("number", "title", "order", "is_active")
    list_display_links = ("icon_class",)
    list_filter = ("section", "is_active")
    ordering = ("section", "order", "id")
    fieldsets = (
        (
            None,
            {
                "fields": ("section", "icon_class", "number", "title", "text"),
                "description": _(
                    "Icon: paste a Font Awesome class, e.g. fa-regular fa-clock. "
                    "Number: +12. Title: Years of experience."
                ),
            },
        ),
        (_("Options"), {"fields": ("order", "is_active")}),
    )


@admin.register(OurWorkImage)
class OurWorkImageAdmin(admin.ModelAdmin):
    # `thumb` first + list_display_links: required when using list_editable (Django admin rules).
    list_display = ("thumb", "order", "media_kind", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("thumb",)
    list_filter = ("is_active",)
    list_per_page = 50
    ordering = ("order", "id")

    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" alt="" width="56" height="56" style="object-fit:cover;border-radius:4px"/>',
                obj.image.url,
            )
        if obj.video:
            return format_html(
                '<span style="display:inline-block;padding:6px 10px;background:#1e293b;color:#f8fafc;'
                'border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
                "VIDEO",
            )
        return "—"

    @admin.display(description="Type")
    def media_kind(self, obj):
        if obj.video:
            return "Video"
        if obj.image:
            return "Image"
        return "—"


class _MVVTabularInlineAdminMixin:
    class Media:
        css = {"all": ("admin/css/mvv_inlines.css",)}


class MVVPartnerLogoInline(_MVVTabularInlineAdminMixin, TranslationTabularInline):
    model = MVVPartnerLogo
    extra = 0
    ordering = ("order",)


class MVVTabPanelInline(TranslationStackedInline):
    """رؤيتنا + رسالتنا + قيمنا — كل تبويب بصورة ونص مستقلين."""

    model = MVVTabPanel
    extra = 0
    min_num = 3
    max_num = 3
    can_delete = False
    ordering = ("order",)
    readonly_fields = ("tab_key", "tab_label_ar")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "tab_key",
                    "tab_label_ar",
                    "side_image",
                    "title",
                ),
            },
        ),
        (_("Tab text"), {"fields": ("body",)}),
    )

    @admin.display(description=_("Tab"))
    def tab_label_ar(self, obj):
        labels = {
            "vision": "رؤيتنا",
            "mission": "رسالتنا",
            "values": "قيمنا",
        }
        return labels.get(obj.tab_key, obj.get_tab_key_display())


@admin.register(MissionVisionValuesBlock)
class MissionVisionValuesBlockAdmin(TranslationAdmin):
    list_display = ("__str__", "title", "language", "is_active", "images_preview")
    list_filter = ("is_active", "language")
    fieldsets = (
        (_("Text"), {"fields": ("subtitle", "title", "intro")}),
        (
            _("Images & video"),
            {
                "fields": ("image_main", "image_large", "video_url", "video_file"),
                "description": _(
                    "Two images like the template: a smaller one top-left and a large "
                    "one on the right. The video button only shows when a link or file is set."
                ),
            },
        ),
        (_("Counter"), {"fields": ("counter_number", "counter_suffix", "counter_title")}),
        (_("Signature"), {"fields": ("author_photo", "author_signature")}),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )
    inlines = (MVVTabPanelInline, MVVPartnerLogoInline)

    @admin.display(description=_("Images"))
    def images_preview(self, obj):
        images = [image for image in (obj.image_main, obj.image_large) if image]
        if not images:
            return "—"
        return format_html_join(
            "",
            '<img src="{}" alt="" width="56" height="40" '
            'style="object-fit:cover;border-radius:4px;margin-inline-end:4px"/>',
            ((image.url,) for image in images),
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for key, order in (("vision", 0), ("mission", 1), ("values", 2)):
            MVVTabPanel.objects.get_or_create(
                block=obj,
                tab_key=key,
                defaults={"order": order},
            )


class MVVTabBulletInline(_MVVTabularInlineAdminMixin, TranslationTabularInline):
    model = MVVTabBullet
    extra = 1
    ordering = ("order", "id")
    fields = ("text", "column", "order")


@admin.register(MVVTabPanel)
class MVVTabPanelAdmin(_MVVTabularInlineAdminMixin, TranslationAdmin):
    """تعديل النقاط (bullets) — الصورة والنص الأساسي من صفحة Home — vision / mission / values."""

    list_display = ("block", "tab_key", "title", "side_image_thumb", "order")
    list_filter = ("tab_key", "block")
    list_editable = ("order",)
    list_display_links = ("tab_key",)
    ordering = ("block", "order", "id")
    raw_id_fields = ("block",)
    inlines = (MVVTabBulletInline,)
    fieldsets = (
        (
            _("This tab only"),
            {
                "fields": ("block", "tab_key", "title", "order", "side_image"),
                "description": _(
                    "Each tab (vision / mission / values) has its own image file. "
                    "Upload a different image for each tab — they are not shared."
                ),
            },
        ),
        (_("Tab text"), {"fields": ("body",)}),
    )

    @admin.display(description=_("Image"))
    def side_image_thumb(self, obj):
        if not obj.side_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="72" height="48" style="object-fit:cover;border-radius:4px"/>',
            obj.side_image.url,
        )


class FinalWordColumnLineInline(_MVVTabularInlineAdminMixin, TranslationTabularInline):
    model = FinalWordColumnLine
    extra = 1
    ordering = ("order", "id")
    fields = ("text", "column", "order")


@admin.register(FinalWordSection)
class FinalWordSectionAdmin(_MVVTabularInlineAdminMixin, TranslationAdmin):
    list_display = ("title", "language", "is_active", "background_thumb")
    list_filter = ("is_active", "language")
    fieldsets = (
        (
            _("Heading"),
            {"fields": ("label", "title")},
        ),
        (
            _("Three paragraphs"),
            {
                "fields": ("paragraph_1", "paragraph_2", "paragraph_3"),
                "description": _(
                    "Each box is one paragraph. Press Enter for a new line inside the same paragraph."
                ),
            },
        ),
        (
            _("Background image"),
            {
                "fields": ("image",),
                "description": _(
                    "Photo behind the text. The dark fade (opacity) is applied automatically."
                ),
            },
        ),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )

    @admin.display(description=_("Background"))
    def background_thumb(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="72" height="48" '
            'style="object-fit:cover;border-radius:4px"/>',
            obj.image.url,
        )
