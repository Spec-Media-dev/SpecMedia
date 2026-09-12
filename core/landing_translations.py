"""
Landing page translations dictionary for Spec Media.
Supports English (en), Arabic (ar), French (fr), Spanish (es), and German (de).
"""
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Base translations loaded from JSON if present, supplemented with comprehensive phrase mappings
JSON_FILE = BASE_DIR / "landing_translations.json"

try:
    if JSON_FILE.exists():
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            LANDING_TRANSLATIONS = json.load(f)
    else:
        LANDING_TRANSLATIONS = {"en": {}, "ar": {}, "fr": {}, "es": {}, "de": {}}
except Exception:
    LANDING_TRANSLATIONS = {"en": {}, "ar": {}, "fr": {}, "es": {}, "de": {}}

# Comprehensive supplemental dictionary covering all visible landing page elements
SUPPLEMENTAL = {
    "en": {
        "[ work ]": "[ work ]",
        "[ studio ]": "[ studio ]",
        "[ capabilities ]": "[ capabilities ]",
        "[ initiate inquiry &rarr; ]": "[ initiate inquiry &rarr; ]",
        "[ initiate inquiry → ]": "[ initiate inquiry → ]",
        "scene 02": "scene 02",
        "keep scrolling or drag mouse to play · frame pauses instantly": "keep scrolling or drag mouse to play · frame pauses instantly",
        "60 FPS SMOOTH SCRUB": "60 FPS SMOOTH SCRUB",
        "07 / REVIEWS — VERIFIED VOICES": "07 / REVIEWS — VERIFIED VOICES",
        "07 / REVIEWS · VERIFIED VOICES": "07 / REVIEWS · VERIFIED VOICES",
        "REVIEWS — VERIFIED VOICES": "REVIEWS — VERIFIED VOICES",
        "Beyond clients.": "Beyond clients.",
        "Trusted partners.": "Trusted partners.",
        "INSTAGRAM FEED · DOUBLE-TAP TO HEART": "INSTAGRAM FEED · DOUBLE-TAP TO HEART",
        "Liked by": "Liked by",
        "and": "and",
        "others": "others",
        "INITIATE INQUIRY": "INITIATE INQUIRY",
        "Your Name": "Your Name",
        "Your Email": "Your Email",
        "Company / Organization": "Company / Organization",
        "Brief Project Scope": "Brief Project Scope",
        "Submit Transmission": "Submit Transmission",
        "All Rights Reserved.": "All Rights Reserved.",
        "Brand Strategy": "Brand Strategy",
        "Campaign Production": "Campaign Production",
        "Performance Media": "Performance Media",
        "Content Systems": "Content Systems",
        "01 / Hero": "01 / Hero",
        "02 / Frame Scrub": "02 / Frame Scrub",
        "03 / Work Grid": "03 / Work Grid",
        "03b / Statement": "03b / Statement",
        "04 / The Reel · Partners": "04 / The Reel · Partners",
        "05 / Capabilities": "05 / Capabilities",
        "06 / Colour Pass": "06 / Colour Pass",
        "07 / Reviews": "07 / Reviews",
        "08 / Contact": "08 / Contact",
    },
    "ar": {
        "[ work ]": "[ الأعمال ]",
        "[ studio ]": "[ الاستوديو ]",
        "[ capabilities ]": "[ القدرات ]",
        "[ initiate inquiry &rarr; ]": "[ ابدأ التواصل &larr; ]",
        "[ initiate inquiry → ]": "[ ابدأ التواصل ← ]",
        "scene 02": "المشهد 02",
        "keep scrolling or drag mouse to play · frame pauses instantly": "واصل التمرير أو اسحب الفأرة للتشغيل · يتوقف الإطار فوراً",
        "60 FPS SMOOTH SCRUB": "تمرير سلس 60 إطار بالثانية",
        "07 / REVIEWS — VERIFIED VOICES": "<span dir=\"ltr\" style=\"unicode-bidi:isolate;font-family:ui-monospace,monospace;display:inline-block;margin-left:6px;\">07 //</span> آراء الشركاء · شهادات موثقة",
        "07 / REVIEWS · VERIFIED VOICES": "<span dir=\"ltr\" style=\"unicode-bidi:isolate;font-family:ui-monospace,monospace;display:inline-block;margin-left:6px;\">07 //</span> آراء الشركاء · شهادات موثقة",
        "REVIEWS — VERIFIED VOICES": "آراء الشركاء · شهادات موثقة",
        "Beyond clients.": "أكثر من مجرد عملاء.",
        "Trusted partners.": "شركاء موثوقون.",
        "INSTAGRAM FEED · DOUBLE-TAP TO HEART": "خلاصة إنستغرام · انقر مرتين للإعجاب",
        "Liked by": "أُعجب به",
        "and": "و",
        "others": "آخرون",
        "INITIATE INQUIRY": "ابدأ استفسارك",
        "Your Name": "الاسم الكامل",
        "Your Email": "البريد الإلكتروني",
        "Company / Organization": "الشركة / المؤسسة",
        "Brief Project Scope": "نطاق المشروع باختصار",
        "Submit Transmission": "إرسال البيانات",
        "All Rights Reserved.": "جميع الحقوق محفوظة.",
        "Brand Strategy": "استراتيجية العلامة",
        "Campaign Production": "إنتاج الحملات",
        "Performance Media": "وسائط الأداء",
        "Content Systems": "أنظمة المحتوى",
        "01 / Hero": "01 / البداية",
        "02 / Frame Scrub": "02 / المعاينة الحركية",
        "selected projects": "مشاريع مختارة",
        "selected work": "أعمال مختارة",
        "Selected projects": "مشاريع مختارة",
        "Selected Work": "الأعمال المختارة",
        "02 / FRAME SCRUB —": "02 / المعاينة الحركية —",
        "02 / FRAME SCRUB": "02 / المعاينة الحركية",
        "FRAME SCRUB": "المعاينة الحركية",
        "03 / Work Grid": "03 / الأعمال المختارة",
        "03b / Statement": "03ب / فلسفتنا",
        "04 / The Reel · Partners": "04 / شركاء النجاح",
        "05 / Capabilities": "05 / قدراتنا",
        "06 / Colour Pass": "06 / المعالجة اللونية",
        "07 / Reviews": "07 / آراء الشركاء",
        "08 / Contact": "08 / تواصل معنا",
    }
}

for lang, mapping in SUPPLEMENTAL.items():
    if lang not in LANDING_TRANSLATIONS:
        LANDING_TRANSLATIONS[lang] = {}
    for k, v in mapping.items():
        if k not in LANDING_TRANSLATIONS[lang] or not LANDING_TRANSLATIONS[lang][k]:
            LANDING_TRANSLATIONS[lang][k] = v
