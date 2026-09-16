import os
import re

from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


def mvv_tab_side_image_upload_to(instance, filename):
    """صورة مستقلة لكل تبويب: mvv/tabs/vision/ … mission/ … values/"""
    tab = (instance.tab_key or "other").strip() or "other"
    base, ext = os.path.splitext(filename)
    safe = f"{base}{ext}" if ext else filename
    return f"mvv/tabs/{tab}/{safe}"

# Create your models here.






class HeroSlide(models.Model):
    """شرائح السلايدر في الصفحة الرئيسية — تُدار من الإدارة."""
    banner = models.ForeignKey(
        "HeroBannerSettings",
        on_delete=models.CASCADE,
        related_name="slides",
        verbose_name=_("Hero banner"),
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))
    tagline = models.CharField(max_length=200, blank=True, verbose_name=_("Subtitle (small line)"))
    heading = models.CharField(max_length=255, blank=True, verbose_name=_("Main heading"))
    lead = models.TextField(blank=True, verbose_name=_("Paragraph text"))
    background_image = models.ImageField(
        upload_to="hero/slides/",
        blank=True,
        null=True,
        verbose_name=_("Banner image"),
        help_text=_("Main slider image. Recommended size: 1920×950."),
    )
    foreground_image = models.ImageField(
        upload_to="hero/slides/",
        blank=True,
        null=True,
        verbose_name=_("Front image (optional)"),
    )
    button_text = models.CharField(max_length=80, blank=True, verbose_name=_("Button text"))
    button_link = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Button link"),
        help_text=_("Example: /#homecontact or a full URL. Leave empty to scroll to contact."),
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Hero slide")
        verbose_name_plural = _("Hero slides")

    def save(self, *args, **kwargs):
        if not self.banner_id:
            banner, _ = HeroBannerSettings.objects.get_or_create(pk=1)
            self.banner = banner
        super().save(*args, **kwargs)

    def __str__(self):
        if self.heading:
            return self.heading[:80]
        return f"Hero slide #{self.pk}"

    @property
    def background_url(self):
        if self.background_image:
            return self.background_image.url
        return ""


class HeroSlideBackgroundImage(models.Model):
    """صور خلفية إضافية لنفس شريحة الهيرو — كل صورة تظهر كشريحة منفصلة في Owl بنفس النص والزر."""

    slide = models.ForeignKey(
        HeroSlide,
        on_delete=models.CASCADE,
        related_name="extra_backgrounds",
        verbose_name=_("Hero slide"),
    )
    image = models.ImageField(upload_to="hero/slides/bg/", verbose_name=_("Background image"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Hero slide extra background")
        verbose_name_plural = _("Hero slide extra backgrounds")

    def __str__(self):
        return f"{self.slide_id} — {self.image.name}"


class HeroBannerSettings(models.Model):
    """صف واحد: شرائح السلايدر (صورة + نص لكل شريحة) أو فيديو خلفية."""

    prefer_video = models.BooleanField(
        default=False,
        verbose_name=_("Use video instead of image slider"),
        help_text=_("When enabled, shows one looping muted video; image carousel is hidden."),
    )
    background_video = models.FileField(
        upload_to="hero/video/",
        blank=True,
        null=True,
        verbose_name=_("Background video file"),
        help_text=_("MP4 or WebM. Plays muted, looped, autoplay."),
    )
    external_video_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("Video URL (optional)"),
        help_text=_("Direct link to an MP4/WebM file. If set, overrides the uploaded file."),
    )

    class Meta:
        verbose_name = _("Hero banner")
        verbose_name_plural = _("Hero banner")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return str(_("Hero banner"))


class HeroOverlayImage(models.Model):
    """صور إضافية أسفل الهيرو (فيديو أو سلايدر) — غالبًا الشكل الزخرفي السفلي."""

    banner = models.ForeignKey(
        HeroBannerSettings,
        on_delete=models.CASCADE,
        related_name="overlay_images",
    )
    image = models.ImageField(upload_to="hero/overlay/")
    order = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Hero bottom image")
        verbose_name_plural = _("Hero bottom images")

    def __str__(self):
        return f"{self.alt_text or self.image.name} (#{self.pk})"


class OurWorkImage(models.Model):
    """Home «Our work» gallery tile: upload either an image or a video (not both)."""

    image = models.ImageField(
        upload_to="our_work/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_("Use this or video — not both."),
    )
    video = models.FileField(
        upload_to="our_work/video/",
        blank=True,
        null=True,
        verbose_name=_("Video"),
        help_text=_("MP4 or WebM. Use this or image — not both."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Our work item")
        verbose_name_plural = _("Our work items")

    def clean(self):
        super().clean()
        has_image = bool(self.image)
        has_video = bool(self.video)
        if not has_image and not has_video:
            raise ValidationError(_("Please add either an image or a video."))
        if has_image and has_video:
            raise ValidationError(_("Please use only one: image or video."))

    def save(
        self,
        *,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        # Django 6+: Model.save() is keyword-only — do not use *args/**kwargs forwarding.
        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        kind = "video" if self.video else "image"
        return f"Our work item #{self.pk} ({kind})"


class HomeOfferStrip(models.Model):
    """
    Feature strip under the hero. Up to four items, each managed inline
    (icon + title, with optional text).
    """

    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — offer strip (below hero)")
        verbose_name_plural = _("Home — offer strip (below hero)")

    def __str__(self):
        if self.pk:
            first = self.items.first()
            if first and first.title and str(first.title).strip():
                return str(first.title).strip()[:80]
        return f"{_('Home offer strip')} — {self.get_language_display()}"


class IconClassMixin:
    """Shared handling of icon classes typed by editors in the admin."""

    # Font Awesome needs a family class next to the icon name; Remix icons don't.
    ICON_FAMILY_PREFIXES = ("fa-solid", "fa-regular", "fa-light", "fa-thin",
                            "fa-duotone", "fa-brands", "fa-sharp", "ri-")
    ICON_FAMILY_SHORTHANDS = ("fa", "fas", "far", "fal", "fat", "fad", "fab")
    DEFAULT_ICON_FAMILY = "fa-regular"

    @property
    def icon_classes(self):
        """Icon class ready for the template, with a family added when missing."""
        tokens = (self.icon_class or "").split()
        if not tokens:
            return ""
        has_family = any(
            token in self.ICON_FAMILY_SHORTHANDS
            or token.startswith(self.ICON_FAMILY_PREFIXES)
            for token in tokens
        )
        if not has_family:
            tokens.insert(0, self.DEFAULT_ICON_FAMILY)
        return " ".join(tokens)


class HomeOfferItem(IconClassMixin, models.Model):
    """One column of the strip: icon + title, and text only when needed."""

    MAX_ITEMS = 4

    strip = models.ForeignKey(
        HomeOfferStrip,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Strip"),
    )
    title = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Title"),
        help_text=_('Example: "+12 Years of Experience".'),
    )
    text = models.TextField(
        blank=True,
        verbose_name=_("Text (optional)"),
        help_text=_("Leave empty to show the icon and title only."),
    )
    icon_class = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Icon code (Font Awesome)"),
        help_text=_(
            'Paste the icon class from fontawesome.com, e.g. "fa-regular fa-clock" '
            'or just "fa-clock". Remix icons ("ri-truck-line") also work.'
        ),
    )
    icon = models.ImageField(
        upload_to="offer_strip/icons/",
        blank=True,
        null=True,
        verbose_name=_("Icon image (optional)"),
        help_text=_(
            "Used only when no icon code is set. Around 70×70 px. "
            "If both are empty, a default theme icon is used."
        ),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Offer strip item")
        verbose_name_plural = _("Offer strip items")

    def __str__(self):
        if self.title and str(self.title).strip():
            return str(self.title).strip()[:80]
        return f"{_('Offer item')} #{self.pk or '?'}"


class HomeHighlightsSection(models.Model):
    """Cards under the services list: icon + number + title + text."""

    label = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small label above the title"),
        help_text=_('Example: "Why Madayin" / «لماذا نحن».'),
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Section title"),
        help_text=_("Leave empty to show the cards without a heading."),
    )
    subtitle = models.TextField(
        blank=True,
        verbose_name=_("Intro text (under title)"),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — stats cards (under services)")
        verbose_name_plural = _("Home — stats cards (under services)")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else f"{_('Highlight cards')} — {self.get_language_display()}"


class HomeHighlightItem(IconClassMixin, models.Model):
    """One card: Font Awesome icon, big number, title and optional text."""

    MAX_ITEMS = 4

    section = models.ForeignKey(
        HomeHighlightsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Section"),
    )
    icon_class = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Icon code (Font Awesome)"),
        help_text=_(
            'Paste the icon class from fontawesome.com, e.g. "fa-regular fa-clock" '
            'or just "fa-clock". Remix icons ("ri-truck-line") also work.'
        ),
    )
    number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Number"),
        help_text=_('Example: "+12" or "25". Empty shows the card position instead.'),
    )
    title = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Title"),
        help_text=_('Example: "Years of Experience".'),
    )
    text = models.TextField(
        blank=True,
        verbose_name=_("Text (optional)"),
        help_text=_("Small line under the title. Leave empty to show the title only."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Highlight card")
        verbose_name_plural = _("Highlight cards")

    def __str__(self):
        if self.title and str(self.title).strip():
            return str(self.title).strip()[:80]
        return f"{_('Highlight card')} #{self.pk or '?'}"

    @property
    def number_parts(self):
        """Split '+12' into prefix/digits so the odometer can count up."""
        raw = (self.number or "").strip()
        match = re.match(r"^(.*?)(\d+)(.*)$", raw)
        if not match:
            return None
        return {
            "prefix": match.group(1),
            "digits": match.group(2),
            "suffix": match.group(3),
        }


class HomeServicesSection(models.Model):
    """خدماتنا — قائمة الخدمات فوق معرض الأعمال."""

    label = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small label above the title"),
        help_text=_('Example: "Our Awesome Services" / «خدماتنا».'),
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Section title"),
        help_text=_('Example: "Our services" / «خدماتنا»'),
    )
    subtitle = models.TextField(
        blank=True,
        verbose_name=_("Intro text (under title)"),
    )
    footer_note = models.TextField(
        blank=True,
        verbose_name=_("Closing note (below cards)"),
        help_text=_(
            "Optional paragraph shown under all four service cards "
            "(e.g. supervision by engineering team)."
        ),
    )
    side_image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
        verbose_name=_("Large side image"),
        help_text=_(
            "Fills the right half of the dark section (around 799×928 px). "
            "Hidden by the theme on screens narrower than 1366px."
        ),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — our services")
        verbose_name_plural = _("Home — our services")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else str(_("Our services section"))


class HomeServiceCard(models.Model):
    section = models.ForeignKey(
        HomeServicesSection,
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name=_("Section"),
    )
    title = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Service name"),
        help_text=_('Example: «Foundation works» / «أعمال الأساسات».'),
    )
    intro = models.TextField(
        blank=True,
        verbose_name=_("Short intro (optional)"),
        help_text=_("One line before the bullet list, if needed."),
    )
    points = models.TextField(
        blank=True,
        verbose_name=_("Bullet points"),
        help_text=_("One service point per line (each line becomes a bullet)."),
    )
    link_url = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Link (optional)"),
        help_text=_("Where the title and arrow point. Empty means the contact section."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Highlighted card"),
        help_text=_("Orange style by default (like the center card in the theme)."),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Service item")
        verbose_name_plural = _("Service items")

    def __str__(self):
        if self.title and str(self.title).strip():
            return str(self.title).strip()[:80]
        return f"{_('Service')} #{self.pk or '?'}"

    @property
    def bullet_lines(self):
        if not self.points:
            return []
        return [line.strip() for line in str(self.points).splitlines() if line.strip()]


class MissionVisionValuesBlock(models.Model):
    """
    Home "About" split block: two images + video button + counter on one side,
    tabs (رؤيتنا / رسالتنا / قيمنا) on the other.
    كل تبويب له صورته في MVVTabPanel.side_image.
    """

    subtitle = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small label above the title"),
        help_text=_('Example: "About Us" / «من نحن».'),
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Section title"),
        help_text=_("If empty, the site name is used."),
    )
    intro = models.TextField(
        blank=True,
        verbose_name=_("Intro paragraph"),
        help_text=_("Shown under the title. If empty, the footer About text is used."),
    )
    image_main = models.ImageField(
        upload_to="mvv/about/",
        blank=True,
        null=True,
        verbose_name=_("Top-left image"),
        help_text=_("Smaller image, around 359×400 px."),
    )
    image_large = models.ImageField(
        upload_to="mvv/about/",
        blank=True,
        null=True,
        verbose_name=_("Large right image"),
        help_text=_("Around 446×512 px. This one has the slide-in reveal animation."),
    )
    video_url = models.URLField(
        blank=True,
        verbose_name=_("Video link (YouTube / Vimeo)"),
        help_text=_(
            "Opens in a popup from the rotating “Watch Video” button. "
            "Leave both video fields empty to hide the button."
        ),
    )
    video_file = models.FileField(
        upload_to="mvv/about/video/",
        blank=True,
        null=True,
        verbose_name=_("Video file"),
        help_text=_("Used only when no video link is set."),
    )
    counter_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Counter number"),
        help_text=_("Counts up from zero when scrolled into view. Empty hides the counter box."),
    )
    counter_suffix = models.CharField(
        max_length=10,
        blank=True,
        default="+",
        verbose_name=_("Counter suffix"),
        help_text=_('Printed right after the number, e.g. "+".'),
    )
    counter_title = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Counter label"),
        help_text=_('Example: "Years of Experience".'),
    )
    author_photo = models.ImageField(
        upload_to="mvv/about/",
        blank=True,
        null=True,
        verbose_name=_("Signatory photo (optional)"),
    )
    author_signature = models.ImageField(
        upload_to="mvv/about/",
        blank=True,
        null=True,
        verbose_name=_("Signature image (optional)"),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — about / vision / mission / values")
        verbose_name_plural = _("Home — about / vision / mission / values")

    def __str__(self):
        return f"MVV — {self.get_language_display()}"

    @property
    def video_link(self):
        """Link for the popup video button, or empty when nothing is set."""
        if self.video_url:
            return self.video_url
        if self.video_file:
            return self.video_file.url
        return ""


class MVVPartnerLogo(models.Model):
    block = models.ForeignKey(
        MissionVisionValuesBlock,
        on_delete=models.CASCADE,
        related_name="partner_logos",
        verbose_name=_("Block"),
    )
    image = models.ImageField(upload_to="mvv/logos/", verbose_name=_("Logo image"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    alt_text = models.CharField(max_length=200, blank=True, verbose_name=_("Alt text"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("MVV — partner logo")
        verbose_name_plural = _("MVV — partner logos")

    def __str__(self):
        return f"Logo #{self.pk} ({self.block_id})"


class MVVTabPanel(models.Model):
    class TabKey(models.TextChoices):
        VISION = "vision", _("Vision")
        MISSION = "mission", _("Mission")
        VALUES = "values", _("Values")

    block = models.ForeignKey(
        MissionVisionValuesBlock,
        on_delete=models.CASCADE,
        related_name="tab_panels",
        verbose_name=_("Block"),
    )
    tab_key = models.CharField(
        max_length=20,
        choices=TabKey.choices,
        verbose_name=_("Tab"),
    )
    title = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Tab label"),
        help_text=_("e.g. رؤيتنا — shown on the pill button."),
    )
    body = RichTextField(blank=True, null=True, verbose_name=_("Body text"))
    side_image = models.ImageField(
        upload_to=mvv_tab_side_image_upload_to,
        blank=True,
        null=True,
        verbose_name=_("Side image for this tab only"),
        help_text=_(
            "صورة هذا التبويب فقط — رؤيتنا / رسالتنا / قيمنا لكل واحد صورة منفصلة."
        ),
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tab order"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("MVV — tab panel")
        verbose_name_plural = _("MVV — tab panels")
        constraints = [
            models.UniqueConstraint(
                fields=["block", "tab_key"],
                name="pages_mvvtabpanel_unique_block_tab_key",
            )
        ]

    def __str__(self):
        return f"{self.get_tab_key_display()} ({self.block_id})"


class MVVTabBullet(models.Model):
    panel = models.ForeignKey(
        MVVTabPanel,
        on_delete=models.CASCADE,
        related_name="bullets",
        verbose_name=_("Tab panel"),
    )
    text = models.CharField(max_length=400, verbose_name=_("Line text"))
    column = models.PositiveSmallIntegerField(
        choices=[(1, _("Column 1")), (2, _("Column 2"))],
        default=1,
        verbose_name=_("Column"),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("MVV — list line")
        verbose_name_plural = _("MVV — list lines")

    def __str__(self):
        return self.text[:60]


class FinalWordColumnLine(models.Model):
    """سطر نص داخل «كلمة أخيرة» — عمود 1 أو 2 يظهران جنب بعض على الموقع."""

    section = models.ForeignKey(
        "FinalWordSection",
        on_delete=models.CASCADE,
        related_name="column_lines",
        verbose_name=_("Section"),
    )
    text = models.CharField(max_length=500, verbose_name=_("Line text"))
    column = models.PositiveSmallIntegerField(
        choices=[(1, _("Column 1")), (2, _("Column 2"))],
        default=1,
        verbose_name=_("Column"),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Final word — column line")
        verbose_name_plural = _("Final word — column lines")

    def __str__(self):
        return self.text[:60]


class FinalWordSection(models.Model):
    """كلمة أخيرة — block before contact / newsletter."""

    label = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small label above the title"),
        help_text=_('Example: "Final word" / «كلمة أخيرة».'),
    )
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Title"))
    paragraph_1 = models.TextField(
        blank=True,
        verbose_name=_("Paragraph 1"),
        help_text=_("Several lines are fine. Each line break is kept on the page."),
    )
    paragraph_2 = models.TextField(
        blank=True,
        verbose_name=_("Paragraph 2"),
        help_text=_("Several lines are fine. Each line break is kept on the page."),
    )
    paragraph_3 = models.TextField(
        blank=True,
        verbose_name=_("Paragraph 3"),
        help_text=_("Several lines are fine. Each line break is kept on the page."),
    )
    body = RichTextField(
        blank=True,
        null=True,
        verbose_name=_("Body (legacy)"),
        help_text=_("Used only when the three paragraphs below are empty."),
    )
    image = models.ImageField(
        upload_to="final_word/",
        blank=True,
        null=True,
        verbose_name=_("Background image"),
        help_text=_(
            "Fills the dark panel behind the text. The theme overlay (dark on the left, "
            "fading out to the right) stays on top of the photo."
        ),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — final word")
        verbose_name_plural = _("Home — final word")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else f"Final word — {self.get_language_display()}"

    def lines_for_column(self, column):
        return self.column_lines.filter(column=column)

    @property
    def col1_lines(self):
        return self.lines_for_column(1)

    @property
    def col2_lines(self):
        return self.lines_for_column(2)

    @property
    def paragraphs(self):
        return [
            text
            for text in (self.paragraph_1, self.paragraph_2, self.paragraph_3)
            if text and str(text).strip()
        ]


class HomePartnersSection(models.Model):
    """شركاء الصفحة الرئيسية — العنوان يُدار من الإدارة."""

    label = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small label above the title"),
        help_text=_('Example: "Our Partners" / «شركاؤنا».'),
    )
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Section title"))
    subtitle = models.TextField(blank=True, verbose_name=_("Intro text (under title)"))
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="en",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — partners")
        verbose_name_plural = _("Home — partners")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else str(_("Partners section"))


class HomePartner(models.Model):
    PLACEMENT_FEATURED_WIDE = "featured_wide"
    PLACEMENT_FEATURED_TALL = "featured_tall"
    PLACEMENT_SLIDER = "slider"
    PLACEMENT_CHOICES = (
        (PLACEMENT_FEATURED_WIDE, _("Top left — wide image (898×450)")),
        (PLACEMENT_FEATURED_TALL, _("Top right — tall image (868×900)")),
        (PLACEMENT_SLIDER, _("Bottom slider — same size")),
    )
    MAX_SLIDER = 6

    section = models.ForeignKey(
        HomePartnersSection,
        on_delete=models.CASCADE,
        related_name="partners",
        verbose_name=_("Section"),
    )
    tag = models.CharField(
        max_length=80,
        blank=True,
        verbose_name=_("Small tag (on hover)"),
        help_text=_('Example: "Metallurgy" / «شريك». Shown as the small badge on hover.'),
    )
    name = models.CharField(
        max_length=160,
        verbose_name=_("Title (on hover)"),
        help_text=_("The larger line under the tag, e.g. the partner name."),
    )
    description = models.TextField(blank=True, verbose_name=_("Short description"))
    logo = models.ImageField(
        upload_to="partners/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_(
            "Top left: 898×450. Top right: 868×900. Slider items: same size, e.g. 868×450."
        ),
    )
    link_url = models.URLField(blank=True, verbose_name=_("Link (optional)"))
    placement = models.CharField(
        max_length=20,
        choices=PLACEMENT_CHOICES,
        default=PLACEMENT_SLIDER,
        verbose_name=_("Position"),
        help_text=_(
            "Use one wide + one tall on top. The rest (up to 6) go in the slider."
        ),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    def __str__(self):
        return (self.name or "").strip()[:80] or f"{_('Partner')} #{self.pk or '?'}"

    @property
    def display_image(self):
        return self.logo or None

    @property
    def card_href(self):
        url = (self.link_url or "").strip()
        if url:
            return url
        if self.logo:
            try:
                return self.logo.url
            except ValueError:
                return "#"
        return "#"

    @property
    def opens_image_popup(self):
        return not (self.link_url or "").strip() and bool(self.logo)


class HomeTruckDealersSection(models.Model):
    """سلايدر وكلاء الشاحنات — العنوان والصور من الإدارة."""

    label = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small label above the title"),
        help_text=_('Example: "Truck dealers" / «وكلاء الشاحنات».'),
    )
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Section title"))
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="en",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — truck dealers")
        verbose_name_plural = _("Home — truck dealers")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else str(_("Truck dealers"))


class HomeTruckDealer(models.Model):
    section = models.ForeignKey(
        HomeTruckDealersSection,
        on_delete=models.CASCADE,
        related_name="dealers",
        verbose_name=_("Section"),
    )
    title = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Optional. Shown on the image (hover)."),
    )
    image = models.ImageField(
        upload_to="truck_dealers/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_("Same size for all cards. Recommended: 768×889."),
    )
    link_url = models.URLField(blank=True, verbose_name=_("Link (optional)"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Truck dealer")
        verbose_name_plural = _("Truck dealers")

    def __str__(self):
        return (self.title or "").strip()[:80] or f"{_('Dealer')} #{self.pk or '?'}"

    @property
    def card_href(self):
        url = (self.link_url or "").strip()
        if url:
            return url
        if self.image:
            try:
                return self.image.url
            except ValueError:
                return "#"
        return "#"

    @property
    def opens_image_popup(self):
        return not (self.link_url or "").strip() and bool(self.image)


class HomeBasePartnersSection(models.Model):
    """شريط لوجوهات الشركاء الأساسيين — صور غير محدودة من الإدارة."""

    label = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Small tag (optional)"),
        help_text=_('Optional small tag above the title. Leave empty to hide it.'),
    )
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Section title"))
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="en",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — base partners")
        verbose_name_plural = _("Home — base partners")

    def __str__(self):
        t = (self.title or self.label or "").strip()
        return t[:80] if t else str(_("Base partners"))


class HomeBasePartner(models.Model):
    section = models.ForeignKey(
        HomeBasePartnersSection,
        on_delete=models.CASCADE,
        related_name="logos",
        verbose_name=_("Section"),
    )
    title = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Name"),
        help_text=_("Optional. Used as the image alt text."),
    )
    image = models.ImageField(
        upload_to="base_partners/",
        blank=True,
        null=True,
        verbose_name=_("Logo"),
        help_text=_("Add as many logos as you need. They show in a 6-up slider."),
    )
    link_url = models.URLField(blank=True, verbose_name=_("Link (optional)"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Base partner logo")
        verbose_name_plural = _("Base partner logos")

    def __str__(self):
        return (self.title or "").strip()[:80] or f"{_('Logo')} #{self.pk or '?'}"