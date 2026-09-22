from modeltranslation.translator import translator, TranslationOptions
from .models import (
    HeroSlide,
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


class HeroSlideTranslationOptions(TranslationOptions):
    fields = ('tagline', 'heading', 'lead', 'button_text')


class HomeOfferItemTranslationOptions(TranslationOptions):
    fields = ("title", "text")


class HomeHighlightsSectionTranslationOptions(TranslationOptions):
    fields = ("label", "title", "subtitle")


class HomeHighlightItemTranslationOptions(TranslationOptions):
    fields = ("title", "text")


class HomeServicesSectionTranslationOptions(TranslationOptions):
    fields = ("label", "title", "subtitle", "footer_note")


class HomeServiceCardTranslationOptions(TranslationOptions):
    fields = ("title", "intro", "points")


class MissionVisionValuesBlockTranslationOptions(TranslationOptions):
    fields = ("subtitle", "title", "intro", "counter_title")


class MVVPartnerLogoTranslationOptions(TranslationOptions):
    fields = ("alt_text",)


class MVVTabPanelTranslationOptions(TranslationOptions):
    fields = ("title", "body")


class MVVTabBulletTranslationOptions(TranslationOptions):
    fields = ("text",)


class FinalWordColumnLineTranslationOptions(TranslationOptions):
    fields = ("text",)


class FinalWordSectionTranslationOptions(TranslationOptions):
    fields = ("label", "title", "paragraph_1", "paragraph_2", "paragraph_3", "body")


class HomePartnersSectionTranslationOptions(TranslationOptions):
    fields = ("label", "title", "subtitle")


class HomePartnerTranslationOptions(TranslationOptions):
    fields = ("tag", "name", "description")


class HomeTruckDealersSectionTranslationOptions(TranslationOptions):
    fields = ("label", "title")


class HomeTruckDealerTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(HeroSlide, HeroSlideTranslationOptions)
translator.register(HomeOfferItem, HomeOfferItemTranslationOptions)
translator.register(HomeHighlightsSection, HomeHighlightsSectionTranslationOptions)
translator.register(HomeHighlightItem, HomeHighlightItemTranslationOptions)
translator.register(HomeServicesSection, HomeServicesSectionTranslationOptions)
translator.register(HomeServiceCard, HomeServiceCardTranslationOptions)
translator.register(MissionVisionValuesBlock, MissionVisionValuesBlockTranslationOptions)
translator.register(MVVPartnerLogo, MVVPartnerLogoTranslationOptions)
translator.register(MVVTabPanel, MVVTabPanelTranslationOptions)
translator.register(MVVTabBullet, MVVTabBulletTranslationOptions)
translator.register(FinalWordColumnLine, FinalWordColumnLineTranslationOptions)
translator.register(FinalWordSection, FinalWordSectionTranslationOptions)
translator.register(HomePartnersSection, HomePartnersSectionTranslationOptions)
translator.register(HomePartner, HomePartnerTranslationOptions)
translator.register(HomeTruckDealersSection, HomeTruckDealersSectionTranslationOptions)
translator.register(HomeTruckDealer, HomeTruckDealerTranslationOptions)
