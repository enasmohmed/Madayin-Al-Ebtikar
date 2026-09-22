from django.contrib import messages
from django.db.models import Prefetch
from django.utils.translation import gettext as _
from django.views.generic import FormView
from contact.forms import HomeContactForm
from contact.services import submit_contact_message
from pages.models import (
    HeroBannerSettings,
    HeroSlide,
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


class HomeView(FormView):
    template_name = 'pages/index.html'
    form_class = HomeContactForm

    def _offer_strip_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        item_qs = HomeOfferItem.objects.filter(is_active=True).order_by("order", "id")
        base_qs = HomeOfferStrip.objects.filter(is_active=True).prefetch_related(
            Prefetch("items", queryset=item_qs),
        )
        strip = base_qs.filter(language=lang).first()
        if strip and strip.items.all():
            return strip
        for candidate in base_qs.order_by("-language", "id"):
            if candidate.items.all():
                return candidate
        return strip or base_qs.first()

    def _highlights_section_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        item_qs = HomeHighlightItem.objects.filter(is_active=True).order_by("order", "id")
        base_qs = HomeHighlightsSection.objects.filter(is_active=True).prefetch_related(
            Prefetch("items", queryset=item_qs),
        )
        section = base_qs.filter(language=lang).first()
        if section and section.items.all():
            return section
        for candidate in base_qs.order_by("-language", "id"):
            if candidate.items.all():
                return candidate
        return section or base_qs.first()

    def _services_section_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        card_qs = HomeServiceCard.objects.filter(is_active=True).order_by("order", "id")
        base_qs = HomeServicesSection.objects.filter(is_active=True).prefetch_related(
            Prefetch("cards", queryset=card_qs),
        )
        section = base_qs.filter(language=lang).first()
        if section and section.cards.all():
            return section
        for candidate in base_qs.order_by("-language", "id"):
            if candidate.cards.all():
                return candidate
        return section or base_qs.first()

    def _mvv_block_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        qs = MissionVisionValuesBlock.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "partner_logos",
                queryset=MVVPartnerLogo.objects.order_by("order", "id"),
            ),
            Prefetch(
                "tab_panels",
                queryset=MVVTabPanel.objects.order_by("order", "id").prefetch_related(
                    Prefetch(
                        "bullets",
                        queryset=MVVTabBullet.objects.order_by("order", "id"),
                    )
                ),
            ),
        )
        return qs.filter(language=lang).first() or qs.first()

    def _final_word_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        qs = FinalWordSection.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "column_lines",
                queryset=FinalWordColumnLine.objects.order_by("order", "id"),
            )
        )
        return qs.filter(language=lang).first() or qs.first()

    def _partners_section_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        partner_qs = HomePartner.objects.filter(is_active=True).order_by("order", "id")
        base_qs = HomePartnersSection.objects.filter(is_active=True).prefetch_related(
            Prefetch("partners", queryset=partner_qs),
        )
        section = base_qs.filter(language=lang).first()
        if section and section.partners.all():
            return section
        for candidate in base_qs.order_by("-language", "id"):
            if candidate.partners.all():
                return candidate
        return section or base_qs.first()

    def _truck_dealers_section_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "en"
        dealer_qs = HomeTruckDealer.objects.filter(is_active=True).order_by("order", "id")
        base_qs = HomeTruckDealersSection.objects.filter(is_active=True).prefetch_related(
            Prefetch("dealers", queryset=dealer_qs),
        )
        section = base_qs.filter(language=lang).first()
        if section and section.dealers.all():
            return section
        for candidate in base_qs.order_by("-language", "id"):
            if candidate.dealers.all():
                return candidate
        return section or base_qs.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order', 'id').prefetch_related(
            'extra_backgrounds',
        )
        hero_banner = HeroBannerSettings.objects.prefetch_related(
            "overlay_images",
        ).first()
        context['hero_banner'] = hero_banner
        offer_strip = self._offer_strip_for_request()
        context['offer_strip'] = offer_strip
        context['offer_items'] = (
            list(offer_strip.items.all())[: HomeOfferItem.MAX_ITEMS]
            if offer_strip
            else []
        )
        context['use_hero_video'] = bool(
            hero_banner
            and hero_banner.prefer_video
            and (hero_banner.external_video_url or hero_banner.background_video)
        )
        work_items = [
            o
            for o in OurWorkImage.objects.filter(is_active=True).order_by("order", "id")
            if o.image or o.video
        ]
        context["our_work_images"] = work_items
        columns = [[] for _ in range(4)]
        for i, o in enumerate(work_items):
            columns[i % 4].append(o)
        context["our_work_columns"] = [c for c in columns if c]
        services_section = self._services_section_for_request()
        context["services_section"] = services_section
        context["services_cards"] = (
            list(services_section.cards.all()) if services_section else []
        )
        highlights_section = self._highlights_section_for_request()
        context["highlights_section"] = highlights_section
        context["highlight_items"] = (
            list(highlights_section.items.all())[: HomeHighlightItem.MAX_ITEMS]
            if highlights_section
            else []
        )
        context["mvv_block"] = self._mvv_block_for_request()
        context["final_word_section"] = self._final_word_for_request()
        partners_section = self._partners_section_for_request()
        partners = list(partners_section.partners.all()) if partners_section else []
        featured_wide = None
        featured_tall = None
        slider_items = []
        unplaced = []
        for partner in partners:
            if partner.placement == HomePartner.PLACEMENT_FEATURED_WIDE and featured_wide is None:
                featured_wide = partner
            elif partner.placement == HomePartner.PLACEMENT_FEATURED_TALL and featured_tall is None:
                featured_tall = partner
            elif partner.placement == HomePartner.PLACEMENT_SLIDER:
                if len(slider_items) < HomePartner.MAX_SLIDER:
                    slider_items.append(partner)
            else:
                unplaced.append(partner)
        for partner in unplaced:
            if featured_wide is None:
                featured_wide = partner
            elif featured_tall is None:
                featured_tall = partner
            elif len(slider_items) < HomePartner.MAX_SLIDER:
                slider_items.append(partner)
        context["partners_section"] = partners_section
        context["partners"] = partners
        context["partner_featured_wide"] = featured_wide
        context["partner_featured_tall"] = featured_tall
        context["partner_slider"] = slider_items
        truck_dealers_section = self._truck_dealers_section_for_request()
        context["truck_dealers_section"] = truck_dealers_section
        context["truck_dealers"] = (
            list(truck_dealers_section.dealers.all()) if truck_dealers_section else []
        )
        site_name = ""
        if isinstance(context.get("site_settings"), dict):
            site_name = (context["site_settings"].get("site_name") or "").strip()
        context["hero_stroke"] = site_name.split()[0] if site_name else ""
        return context

    def get_success_url(self):
        return f"{self.request.path}#homecontact"

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            submit_contact_message(
                name=data["name"],
                email=data["email"],
                message=data["message"],
            )
        except Exception:
            messages.error(
                self.request,
                _("We could not send your message. Please try again later."),
                extra_tags="contact",
            )
            return self.form_invalid(form)

        messages.success(
            self.request,
            _("Your message was sent successfully. We will get back to you soon."),
            extra_tags="contact",
        )
        return super().form_valid(form)
