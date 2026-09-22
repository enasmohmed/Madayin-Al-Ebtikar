from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.cache import cache

from core.models import SiteSettings, FooterSection, Sections
from pages.models import (
    HeroSlide,
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
    MVVTabPanel,
    MVVTabBullet,
    FinalWordSection,
    FinalWordColumnLine,
)


LOGO_CANDIDATES = [
    Path("/media/enas/01DCA27B13BCF520/Data/projects/Media Glow/Madayin Al-btikar/Asset 29@4x.png"),
]


ABOUT_SHORT = (
    "Madayin Al Ebtikar Trading (MET) was launched to be part of Vision 2030, "
    "localizing opportunities and ideas. We supply hydraulic equipment and spare "
    "parts to national entities, and fabricate metal products inside Saudi Arabia."
)

ABOUT_FOOTER = (
    "Registered supplier with SEC and other governmental entities, with Engineering, "
    "Sales, and After Sales teams across the Kingdom."
)

VISION = (
    "Empowering our locally made products, and participating in increasing local content "
    "while importing know-how from international experience — aligning with Vision 2030."
)

MESSAGE = (
    "High standards in all our services. Quality is not negotiable. "
    "After-sale is more important than the sale itself."
)


class Command(BaseCommand):
    help = "Load Madayin Al Ebtikar company-profile content into the CMS."

    def handle(self, *args, **options):
        site, _ = SiteSettings.objects.get_or_create(pk=1)
        site.site_name = "Madayin Al Ebtikar"
        if hasattr(site, "site_name_en"):
            site.site_name_en = "Madayin Al Ebtikar"
        site.email = "info@madayin.com"
        site.website = "https://madayin.com"
        site.phone_mobile = "+966538375237"
        site.phone_landline = "+966125789825"
        site.phone = "+966538375237"
        site.address = "Riyadh, Kingdom of Saudi Arabia"
        if hasattr(site, "address_en"):
            site.address_en = site.address
        site.working_hours = ""
        if hasattr(site, "working_hours_en"):
            site.working_hours_en = ""
        site.footer_about = ABOUT_SHORT
        site.primary_color = "#F5A623"
        site.secondary_color = "#0B1B3A"
        site.theme_red = "#E30613"
        site.default_language = "en"
        site.our_work_section_title = "After Sales Coverage"
        site.our_work_section_subtitle = (
            "Service and spare parts network from our headquarters and factory in Riyadh."
        )
        site.save()

        logo_path = next((p for p in LOGO_CANDIDATES if p.exists()), None)
        if logo_path:
            with logo_path.open("rb") as fh:
                site.logo.save("madayin-al-ebtikar.png", File(fh), save=False)
            with logo_path.open("rb") as fh:
                site.preloader_logo.save("madayin-preloader.png", File(fh), save=False)
            with logo_path.open("rb") as fh:
                site.favicon.save("madayin-favicon.png", File(fh), save=False)
            site.save()

        footer, _ = FooterSection.objects.get_or_create(pk=1)
        footer.site_name = "Madayin Al Ebtikar"
        footer.description = ABOUT_FOOTER
        footer.email = "info@madayin.com"
        footer.website = "https://madayin.com"
        footer.phone_mobile = "+966538375237"
        footer.phone_landline = "+966125789825"
        footer.address = "Riyadh, Kingdom of Saudi Arabia"
        footer.copyright_text = "© 2026 Madayin Al Ebtikar Trading. All rights reserved."
        footer.quick_links = [
            {"title": "Home", "url": "home"},
            {"title": "About", "url": "about"},
            {"title": "Services", "url": "services"},
            {"title": "Partners", "url": "partners"},
            {"title": "Contact", "url": "contact"},
        ]
        footer.is_active = True
        if logo_path:
            with logo_path.open("rb") as fh:
                footer.logo.save("madayin-footer.png", File(fh), save=False)
        footer.save()

        nav_items = [
            (1, "Home", "home"),
            (2, "About", "about"),
            (3, "Services", "services"),
            (4, "Partners", "partners"),
            (5, "Contact", "contact"),
        ]
        Sections.objects.all().delete()
        for order, title, slug in nav_items:
            section = Sections(order=order, slug=slug, is_visible=True, show_in_nav=True)
            section.title = title
            if hasattr(section, "title_en"):
                section.title_en = title
            if hasattr(section, "slug_en"):
                section.slug_en = slug
            section.save()

        HeroSlide.objects.all().delete()
        HeroSlide.objects.create(
            order=1,
            is_active=True,
            tagline="Building a Better Future",
            heading="Reliable Hydraulic Solutions for the Kingdom",
            lead=(
                "Madayin Al Ebtikar Trading supplies hydraulic equipment, spare parts, "
                "and locally fabricated metal products — with Engineering, Sales, and "
                "After Sales teams across Saudi Arabia."
            ),
            button_text="Services Request",
            button_link="/#services",
        )
        HeroSlide.objects.create(
            order=2,
            is_active=True,
            tagline="Vision 2030",
            heading="National Supplier of Special Products",
            lead=(
                "Registered supplier with SEC and other governmental entities. "
                "We localize opportunities and fabricate metal products inside Saudi Arabia."
            ),
            button_text="Contact Us",
            button_link="/#simply-contact",
        )

        HomeOfferStrip.objects.all().delete()
        offer_strip = HomeOfferStrip.objects.create(language="en", is_active=True)
        for order, (title, text) in enumerate(
            [
                (
                    "+12 Years of Experience",
                    "A well-experienced team in Engineering, Sales, and After Sales across the Kingdom.",
                ),
                (
                    "25 Cities — Service & Spare Parts",
                    "A service and spare-parts network from the far north to the far south, based in Riyadh.",
                ),
                (
                    "8 Global Agencies",
                    "International partners for hydraulic equipment, safety tools, cables, and diagnostic devices.",
                ),
                ("+2500 Clients", ""),
            ],
            start=1,
        ):
            HomeOfferItem.objects.create(
                strip=offer_strip,
                order=order,
                is_active=True,
                title=title,
                text=text,
            )

        HomeServiceCard.objects.all().delete()
        HomeServicesSection.objects.all().delete()
        services = HomeServicesSection.objects.create(
            language="en",
            is_active=True,
            label="Our Awesome Services",
            title="Hydraulic equipment, fabrication, and after sales",
            subtitle=(
                "Manufacturing and supplying special hydraulic products, metal fabrication, "
                "and a cradle-to-grave after-sales package unmatched in our industry."
            ),
            footer_note=(
                "We work closely with truck dealers across Saudi Arabia and neighboring countries "
                "to deliver complete turnkey body construction on the chassis of your choice."
            ),
        )
        HomeServiceCard.objects.create(
            section=services,
            order=1,
            is_active=True,
            is_featured=True,
            title="Metal Fabrication",
            intro="Manufacturing of all kinds of metal fabrication products inside Saudi Arabia.",
            points="Local manufacturing\nMetal fabricated products\nSupport for national entities",
        )
        HomeServiceCard.objects.create(
            section=services,
            order=2,
            is_active=True,
            title="Hydraulic Products",
            intro="Manufacturing and supplying of special hydraulic products.",
            points="Hydraulic cranes\nInsulated & non-insulated manlifts\nCable drum handler",
        )
        HomeServiceCard.objects.create(
            section=services,
            order=3,
            is_active=True,
            title="After Sales Service",
            intro=(
                "Trustworthy service response and a reliable spare-parts division, "
                "with training for mechanics and operators — including on-site support."
            ),
            points="Genuine spare parts from Riyadh stock\nBodywork, repair, welding and repainting\nHydraulic maintenance: valves, cylinders, PTOs",
        )
        HomeServiceCard.objects.create(
            section=services,
            order=4,
            is_active=True,
            title="Truck Bodybuilding",
            intro=(
                "Detailed knowledge of chassis models with dealers in the Kingdom and neighboring countries. "
                "A single-source turnkey that includes the chassis of your choice."
            ),
            points="Chassis specification support\nBody construction logistics\nMercedes-Benz, Volvo, MAN, Scania, Iveco and more",
        )

        HomeHighlightItem.objects.all().delete()
        HomeHighlightsSection.objects.all().delete()
        highlights = HomeHighlightsSection.objects.create(
            language="en",
            is_active=True,
        )
        HomeHighlightItem.objects.create(
            section=highlights,
            order=1,
            is_active=True,
            icon_class="fa-regular fa-clock",
            number="+12",
            title="Years of experience",
        )
        HomeHighlightItem.objects.create(
            section=highlights,
            order=2,
            is_active=True,
            icon_class="fa-solid fa-gears",
            number="25",
            title="City service and spare parts",
        )
        HomeHighlightItem.objects.create(
            section=highlights,
            order=3,
            is_active=True,
            icon_class="fa-solid fa-globe",
            number="8",
            title="Global agencies",
        )
        HomeHighlightItem.objects.create(
            section=highlights,
            order=4,
            is_active=True,
            icon_class="fa-regular fa-file-invoice",
            number="12",
            title="One-month warranty tax invoice",
        )

        MVVTabBullet.objects.all().delete()
        MVVTabPanel.objects.all().delete()
        MissionVisionValuesBlock.objects.all().delete()
        mvv = MissionVisionValuesBlock.objects.create(
            language="en",
            is_active=True,
            subtitle="About Us",
            title="Madayin Al Ebtikar",
            intro=ABOUT_SHORT,
            counter_number=12,
            counter_suffix="+",
            counter_title="Years of Experience",
        )
        MVVTabPanel.objects.create(
            block=mvv,
            tab_key=MVVTabPanel.TabKey.VISION,
            title="Vision",
            body=f"<p>{VISION}</p>",
            order=1,
        )
        MVVTabPanel.objects.create(
            block=mvv,
            tab_key=MVVTabPanel.TabKey.MISSION,
            title="Message",
            body=f"<p>{MESSAGE}</p><p><strong>Goal:</strong> {MESSAGE}</p>",
            order=2,
        )
        values = MVVTabPanel.objects.create(
            block=mvv,
            tab_key=MVVTabPanel.TabKey.VALUES,
            title="Values",
            body="<p>Our work is built on lasting partnerships and uncompromising standards.</p>",
            order=3,
        )
        for i, text in enumerate(
            [
                "Solid customer relationship",
                "Quality",
                "Reliable",
                "Aftersales service",
            ],
            start=1,
        ):
            MVVTabBullet.objects.create(panel=values, text=text, column=1, order=i)

        FinalWordColumnLine.objects.all().delete()
        FinalWordSection.objects.all().delete()
        final = FinalWordSection.objects.create(
            language="en",
            is_active=True,
            label="Final word",
            title="After Sales Service",
            paragraph_1=(
                "Genuine spare parts — manufacturer warranty and stock in Riyadh.\n"
                "Bodywork and repair — boxes, tippers, tanks, chassis, welding, and repainting."
            ),
            paragraph_2=(
                "Hydraulic maintenance — valves, cylinders, PTOs, and pressure adjustment.\n"
                "Training for mechanics and operators, including on-site support."
            ),
            paragraph_3=(
                "Kingdom-wide coverage from our Riyadh headquarters and factory.\n"
                "Equipment operating from the far north to the far south of the Kingdom."
            ),
        )

        HomePartner.objects.all().delete()
        HomePartnersSection.objects.all().delete()
        partners_section = HomePartnersSection.objects.create(
            language="en",
            is_active=True,
            label="Our Partners",
            title="Global agencies and local manufacturing",
            subtitle="Client base of +2500 clients and growing.",
        )
        partners = [
            ("SOFAMEL", "Spain", "Spain — electrical connection materials and safety equipment.", "featured_wide"),
            ("CO.ME.T. Officine", "Italy", "Italy — insulated aerial platforms up to 46 kV.", "featured_tall"),
            ("HC Industries", "Partner", "Articulated hydraulic cranes, 3–5 tons.", "slider"),
            ("Ferrari International", "Italy", "Italy — fiberglass individual baskets for cranes.", "slider"),
            ("Aristoncavi", "Italy", "Italy — cables and electrical conductors.", "slider"),
            ("MET", "Saudi Arabia", "Saudi Arabia — MET cable reel holders, fabricated locally.", "slider"),
            ("THINKCAR", "China", "China — testing, measuring, and diagnostic devices.", "slider"),
            ("Interpump", "Italy", "Italy — hydraulic pumps in all sizes.", "slider"),
        ]
        for order, (name, tag, description, placement) in enumerate(partners, start=1):
            HomePartner.objects.create(
                section=partners_section,
                name=name,
                tag=tag,
                description=description,
                placement=placement,
                order=order,
                is_active=True,
            )

        HomeTruckDealer.objects.all().delete()
        HomeTruckDealersSection.objects.all().delete()
        dealers_section = HomeTruckDealersSection.objects.create(
            language="en",
            is_active=True,
            label="Truck dealers",
            title="Chassis partners across the Kingdom",
        )
        for order, name in enumerate(
            ("Mercedes-Benz", "Volvo", "MAN", "Scania", "Iveco"),
            start=1,
        ):
            HomeTruckDealer.objects.create(
                section=dealers_section,
                title=name,
                order=order,
                is_active=True,
            )

        cache.clear()
        self.stdout.write(self.style.SUCCESS("Madayin company profile data loaded."))
