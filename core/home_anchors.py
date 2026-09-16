"""Landing-page section slugs → HTML anchor ids (shared by navbar & footer links)."""

HOME_ANCHOR_ALIASES = {
    "home": "home",
    "hero": "home",
    "about": "homeabout",
    "homeabout": "homeabout",
    "من-نحن": "homeabout",
    "services": "homeservices",
    "homeservices": "homeservices",
    "خدماتنا": "homeservices",
    "our-services": "homeservices",
    "portfolio": "homeportfolio",
    "homeportfolio": "homeportfolio",
    "معرض-الاعمال": "homeportfolio",
    "معرض-الأعمال": "homeportfolio",
    "our-work": "homeportfolio",
    "projects": "homeportfolio",
    "company-vision": "vision",
    "vision": "vision",
    "رؤية-الشركة": "vision",
    "company-mission": "mission",
    "mission": "mission",
    "رسالة-الشركة": "mission",
    "values": "values",
    "contact": "homecontact",
    "homecontact": "homecontact",
    "simply-contact": "homecontact",
    "partners": "partners",
    "our-partners": "partners",
    "base-partners": "base-partners",
    "basepartners": "base-partners",
    "truck-dealers": "truck-dealers",
    "truckdealers": "truck-dealers",
    "dealers": "truck-dealers",
    "final-word": "final-word",
    "after-sales": "final-word",
    "blog": "final-word",
}


def anchor_for_slug(slug):
    if not slug:
        return "home"
    normalized = str(slug).strip().lower().lstrip("/").lstrip("#")
    return HOME_ANCHOR_ALIASES.get(normalized, normalized or "home")
