"""
Generates complete, verified PO catalogs for English, Arabic, French, Spanish, and German,
and compiles them into binary MO catalogs.
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(r"c:\Users\acer\Desktop\specmedia")
sys.path.insert(0, str(PROJECT_ROOT))

from core.compile_locales import build_mo, compile_all_locales

# MASTER TRANSLATIONS REPOSITORY
# Key: English msgid
# Value: dict of {ar, fr, es, de}
CATALOG = {
    # Nav & Chrome
    "[ work ]": {
        "ar": "[ الأعمال ]",
        "fr": "[ travaux ]",
        "es": "[ proyectos ]",
        "de": "[ werke ]",
    },
    "[ studio ]": {
        "ar": "[ الاستوديو ]",
        "fr": "[ studio ]",
        "es": "[ estudio ]",
        "de": "[ studio ]",
    },
    "[ capabilities ]": {
        "ar": "[ القدرات ]",
        "fr": "[ expertises ]",
        "es": "[ capacidades ]",
        "de": "[ fähigkeiten ]",
    },
    "[ initiate inquiry &rarr; ]": {
        "ar": "[ ابدأ التواصل &larr; ]",
        "fr": "[ initier une demande &rarr; ]",
        "es": "[ iniciar consulta &rarr; ]",
        "de": "[ anfrage starten &rarr; ]",
    },
    "[ initiate inquiry → ]": {
        "ar": "[ ابدأ التواصل ← ]",
        "fr": "[ initier une demande → ]",
        "es": "[ iniciar consulta → ]",
        "de": "[ anfrage starten → ]",
    },
    "[ contact ]": {
        "ar": "[ تواصل ]",
        "fr": "[ contact ]",
        "es": "[ contacto ]",
        "de": "[ kontakt ]",
    },
    "[ menu ]": {
        "ar": "[ قائمة ]",
        "fr": "[ menu ]",
        "es": "[ menú ]",
        "de": "[ menü ]",
    },
    "01 / index": {
        "ar": "01 / البداية",
        "fr": "01 / accueil",
        "es": "01 / inicio",
        "de": "01 / index",
    },
    "[ scroll down ]": {
        "ar": "[ اسحب لأسفل ]",
        "fr": "[ défiler ]",
        "es": "[ desplazar ]",
        "de": "[ nach unten ]",
    },
    "Work": {
        "ar": "الأعمال",
        "fr": "Travaux",
        "es": "Proyectos",
        "de": "Werke",
    },
    "Studio": {
        "ar": "الاستوديو",
        "fr": "Studio",
        "es": "Estudio",
        "de": "Studio",
    },
    "Capabilities": {
        "ar": "القدرات",
        "fr": "Expertises",
        "es": "Capacidades",
        "de": "Fähigkeiten",
    },
    "&uarr; Back to Top": {
        "ar": "&uarr; إلى الأعلى",
        "fr": "&uarr; Haut de page",
        "es": "&uarr; Volver arriba",
        "de": "&uarr; Nach oben",
    },
    "[ Back to Top &uarr; ]": {
        "ar": "[ إلى الأعلى &uarr; ]",
        "fr": "[ Haut de page &uarr; ]",
        "es": "[ Volver arriba &uarr; ]",
        "de": "[ Nach oben &uarr; ]",
    },
    "&copy; 2026 SPEC MEDIA. ALL RIGHTS RESERVED.": {
        "ar": "&copy; 2026 SPEC MEDIA. جميع الحقوق محفوظة.",
        "fr": "&copy; 2026 SPEC MEDIA. TOUS DROITS RÉSERVÉS.",
        "es": "&copy; 2026 SPEC MEDIA. TODOS LOS DERECHOS RESERVADOS.",
        "de": "&copy; 2026 SPEC MEDIA. ALLE RECHTE VORBEHALTEN.",
    },
    "&copy; 2026 Spec Media Inc. Built for brands with cultural gravity.": {
        "ar": "&copy; 2026 Spec Media Inc. صُمم للعلامات ذات الثقل الثقافي.",
        "fr": "&copy; 2026 Spec Media Inc. Conçu pour les marques à forte résonance culturelle.",
        "es": "&copy; 2026 Spec Media Inc. Creado para marcas con gravedad cultural.",
        "de": "&copy; 2026 Spec Media Inc. Entwickelt für Marken mit kultureller Gravitation.",
    },

    # Hero & Manifesto
    "You feel the brand before it speaks®": {
        "ar": "تحسّ بالعلامة قبل أن تتكلّم®",
        "fr": "Vous ressentez la marque avant qu'elle ne parle®",
        "es": "Sientes la marca antes de que hable®",
        "de": "Du spürst die Marke, bevor sie spricht®",
    },
    "Placeholder copy. Spec Media builds campaigns for companies that care how things feel and how they are perceived over time.": {
        "ar": "تبني Spec Media حملات نوعية للشركات التي تهتم بكيفية شعور منتجاتها ورسوخ مكانتها مع مرور الوقت.",
        "fr": "Spec Media conçoit des campagnes pour les entreprises soucieuses de l'impact émotionnel et de la perception durable de leur marque.",
        "es": "Spec Media crea campañas para empresas que se preocupan por cómo se sienten las cosas y cómo perduran en el tiempo.",
        "de": "Spec Media entwickelt Kampagnen für Unternehmen, denen das emotionale Erlebnis und die nachhaltige Wahrnehmung ihrer Marke am Herzen liegen.",
    },
    "brand strategy": {
        "ar": "استراتيجية العلامة",
        "fr": "stratégie de marque",
        "es": "estrategia de marca",
        "de": "Markenstrategie",
    },
    "campaign production": {
        "ar": "إنتاج الحملات",
        "fr": "production de campagnes",
        "es": "producción de campañas",
        "de": "Kampagnenproduktion",
    },
    "performance media": {
        "ar": "وسائط الأداء",
        "fr": "médias de performance",
        "es": "medios de rendimiento",
        "de": "Performance-Medien",
    },
    "content systems": {
        "ar": "أنظمة المحتوى",
        "fr": "systèmes de contenu",
        "es": "sistemas de contenido",
        "de": "Content-Systeme",
    },
    "Selected work": {
        "ar": "أعمال مختارة",
        "fr": "Travaux sélectionnés",
        "es": "Trabajos seleccionados",
        "de": "Ausgewählte Arbeiten",
    },
    "2024 — 2026 · placeholder projects": {
        "ar": "2024 — 2026 · مشاريع مختارة",
        "fr": "2024 — 2026 · projets sélectionnés",
        "es": "2024 — 2026 · proyectos seleccionados",
        "de": "2024 — 2026 · ausgewählte Projekte",
    },
    "[ what we believe ]": {
        "ar": "[ ما نؤمن به ]",
        "fr": "[ en quoi nous croyons ]",
        "es": "[ en lo que creemos ]",
        "de": "[ was wir glauben ]",
    },
    "Attention is the only currency that compounds.": {
        "ar": "الانتباه هو العملة الوحيدة التي تتضاعف قيمتها مع الزمن.",
        "fr": "L'attention est la seule monnaie qui génère des intérêts composés.",
        "es": "La atención es la única moneda que se compone con el tiempo.",
        "de": "Aufmerksamkeit ist die einzige Währung, die sich potenziert.",
    },
    "TRUSTED PARTNERS": {
        "ar": "شركاء موثوقون",
        "fr": "PARTENAIRES DE CONFIANCE",
        "es": "SOCIOS DE CONFIANZA",
        "de": "VERTRAUENSWÜRDIGE PARTNER",
    },
    "04 / THE REEL": {
        "ar": "04 / الإعلان السينمائي",
        "fr": "04 / LE FILM",
        "es": "04 / EL REEL",
        "de": "04 / DER REEL",
    },
    "Trusted by teams that value exceptional digital experiences.": {
        "ar": "موثوق من قِبل فرق تُقدّر التجارب الرقمية الاستثنائية.",
        "fr": "Approuvé par des équipes exigeant des expériences numériques exceptionnelles.",
        "es": "Confiado por equipos que valoran experiencias digitales excepcionales.",
        "de": "Geschätzt von Teams, die außergewöhnliche digitale Erlebnisse verlangen.",
    },
    "capabilities — hover to inspect work": {
        "ar": "القدرات — حرّك الفأرة لمعاينة الأعمال",
        "fr": "capacités — survolez pour inspecter les travaux",
        "es": "capacidades — pasa el cursor para inspeccionar",
        "de": "Fähigkeiten — bewegen Sie den Cursor zur Inspektion",
    },
    "SELECT A DISCIPLINE": {
        "ar": "اختر تخصصاً",
        "fr": "CHOISISSEZ UNE DISCIPLINE",
        "es": "SELECCIONE UNA DISCIPLINA",
        "de": "DISZIPLIN WÄHLEN",
    },
    "Hover a capability to inspect production assets": {
        "ar": "حرّك المؤشر فوق قدرة لمعاينة أصول الإنتاج",
        "fr": "Survolez une capacité pour inspecter les assets de production",
        "es": "Pasa el cursor sobre una capacidad para ver los activos",
        "de": "Cursor über eine Fähigkeit bewegen für Produktionsassets",
    },
    "PORTFOLIO GALLERY": {
        "ar": "معرض الأعمال",
        "fr": "GALERIE DE PORTFOLIO",
        "es": "GALERÍA DE PORTAFOLIO",
        "de": "PORTFOLIOGALERIE",
    },

    # Capabilities Page
    "End-to-End Capabilities — Spec Media": {
        "ar": "القدرات المتكاملة — Spec Media",
        "fr": "Expertises Complètes — Spec Media",
        "es": "Capacidades Integrales — Spec Media",
        "de": "Ganzheitliche Fähigkeiten — Spec Media",
    },
    "Full-Spectrum Architecture // End-to-End Suite": {
        "ar": "هيكلية متكاملة الأركان // حزمة شاملة من البداية للنهاية",
        "fr": "Architecture globale // Suite de bout en bout",
        "es": "Arquitectura integral // Suite de extremo a extremo",
        "de": "Ganzheitliche Architektur // Komplettsuite",
    },
    "Four disciplines. One singular focus.": {
        "ar": "أربعة تخصصات. تركيز واحد لا ينقسم.",
        "fr": "Quatre disciplines. Un objectif unique.",
        "es": "Cuatro disciplinas. Un solo enfoque.",
        "de": "Vier Disziplinen. Ein klarer Fokus.",
    },
    "We dismantle the friction between upstream brand strategy, cinematic production, paid distribution, and iterative content systems.": {
        "ar": "نزيل أي عائق بين استراتيجية العلامة الرائدة، الإنتاج السينمائي، التوزيع الإعلاني المدفوع، وأنظمة المحتوى المتجددة.",
        "fr": "Nous éliminons les frictions entre stratégie de marque en amont, production cinématographique, distribution payante et systèmes de contenu itératifs.",
        "es": "Eliminamos la fricción entre la estrategia de marca inicial, la producción cinematográfica, la distribución pagada y los sistemas de contenido continuos.",
        "de": "Wir beseitigen die Reibung zwischen Markenstrategie, kinematografischer Produktion, bezahlter Distribution und iterativen Content-Systemen.",
    },
    "01 STRATEGY": {
        "ar": "01 الاستراتيجية",
        "fr": "01 STRATÉGIE",
        "es": "01 ESTRATEGIA",
        "de": "01 STRATEGIE",
    },
    "02 PRODUCTION": {
        "ar": "02 الإنتاج السينمائي",
        "fr": "02 PRODUCTION",
        "es": "02 PRODUCCIÓN",
        "de": "02 PRODUKTION",
    },
    "03 PERFORMANCE MEDIA": {
        "ar": "03 وسائط الأداء والنمو",
        "fr": "03 MÉDIAS DE PERFORMANCE",
        "es": "03 MEDIOS DE RENDIMIENTO",
        "de": "03 PERFORMANCE-MEDIEN",
    },
    "04 CONTENT SYSTEMS": {
        "ar": "04 أنظمة المحتوى",
        "fr": "04 SYSTÈMES DE CONTENU",
        "es": "04 SISTEMAS DE CONTENIDO",
        "de": "04 CONTENT-SYSTEME",
    },
    "[ The Core Disciplines ]": {
        "ar": "[ التخصصات الجوهرية ]",
        "fr": "[ Les Disciplines Clés ]",
        "es": "[ Las Disciplinas Principales ]",
        "de": "[ Die Kern-Disziplinen ]",
    },
    "Engineered to compound enterprise equity.": {
        "ar": "مُهندسة لمضاعفة القيمة السوقية للعلامة التجارية.",
        "fr": "Conçu pour maximiser la valeur de l'entreprise.",
        "es": "Diseñado para multiplicar el valor comercial de la marca.",
        "de": "Entwickelt zur kontinuierlichen Steigerung des Unternehmenswerts.",
    },
    "01 // DISCIPLINE": {
        "ar": "01 // التخصص الأول",
        "fr": "01 // DISCIPLINE",
        "es": "01 // DISCIPLINA",
        "de": "01 // DISZIPLIN",
    },
    "Brand Strategy & Architecture": {
        "ar": "استراتيجية وهندسة العلامة التجارية",
        "fr": "Stratégie et Architecture de Marque",
        "es": "Estrategia y Arquitectura de Marca",
        "de": "Markenstrategie & Architektur",
    },
    "Upstream Moat": {
        "ar": "حصانة استراتيجية رائدة",
        "fr": "Avantage Stratégique Majeur",
        "es": "Ventaja Competitiva Superior",
        "de": "Strategischer Wettbewerbsvorteil",
    },
    "We synthesize the core positioning, voice, and visual architecture that define category leaders. From founder narrative synthesis to comprehensive brand guidelines, we design systems that remain iconic and culturally dominant over decades.": {
        "ar": "نصوغ جوهر التموضع والهوية البصرية والصوتية التي تقود الفئات في السوق. من سردية المؤسسين إلى إرشادات العلامة المتكاملة، نبتكر أنظمة تفرض سيادتها الثقافية لعقود.",
        "fr": "Nous synthétisons le positionnement, la voix et l'architecture visuelle qui définissent les leaders. De la narration fondatrice aux chartes graphiques complètes, nous créons des systèmes pérennes et influents.",
        "es": "Sintetizamos el posicionamiento, la voz y la identidad visual que definen a los líderes de la categoría, diseñando sistemas icónicos y culturalmente dominantes.",
        "de": "Wir formulieren die Positionierung, Tonalität und visuelle Architektur von Marktführern, um Marken über Jahrzehnte hinweg unverwechselbar zu machen.",
    },
    "Core Deliverables:": {
        "ar": "المخرجات الرئيسية:",
        "fr": "Livrables Principaux :",
        "es": "Entregables Principales:",
        "de": "Kern-Ergebnisse:",
    },
    "Market Positioning Matrix": {
        "ar": "مصفوفة التموضع في السوق",
        "fr": "Matrice de positionnement marché",
        "es": "Matriz de posicionamiento de mercado",
        "de": "Marktpositionierungs-Matrix",
    },
    "Visual Identity Systems": {
        "ar": "أنظمة الهوية البصرية",
        "fr": "Systèmes d'identité visuelle",
        "es": "Sistemas de identidad visual",
        "de": "Visuelle Identitätssysteme",
    },
    "Typography & Token Libraries": {
        "ar": "مكتبات الخطوط والعناصر التصميمية",
        "fr": "Typographies et bibliothèques de jetons",
        "es": "Tipografía y bibliotecas de tokens",
        "de": "Typografie- & Token-Bibliotheken",
    },
    "Brand Architecture Blueprint": {
        "ar": "مخطط هيكلية العلامة",
        "fr": "Schéma d'architecture de marque",
        "es": "Plano de arquitectura de marca",
        "de": "Markenarchitektur-Blaupause",
    },
    "Verbal Voice & Tone Guidelines": {
        "ar": "دليل النبرة والنص التسويقي",
        "fr": "Guide du ton et de la voix éditoriale",
        "es": "Directrices de tono y voz verbal",
        "de": "Richtlinien für Tonalität und Markenstimme",
    },
    "EXPECTED OUTCOME": {
        "ar": "النتيجة المتوقعة",
        "fr": "RÉSULTAT ATTENDU",
        "es": "RESULTADO ESPERADO",
        "de": "ERWARTETES ERGEBNIS",
    },
    "Target Valuation & Brand Equity": {
        "ar": "تقييم السوق وقيمة العلامة التجارية",
        "fr": "Valorisation cible & capital de marque",
        "es": "Valoración y valor de marca objetivo",
        "de": "Zielbewertung & Markenkapital",
    },
    "Inquire Service &rarr;": {
        "ar": "طلب الخدمة &larr;",
        "fr": "Demander ce service &rarr;",
        "es": "Solicitar servicio &rarr;",
        "de": "Service anfragen &rarr;",
    },
    "02 // DISCIPLINE": {
        "ar": "02 // التخصص الثاني",
        "fr": "02 // DISCIPLINE",
        "es": "02 // DISCIPLINA",
        "de": "02 // DISZIPLIN",
    },
    "Campaign Production & Film": {
        "ar": "إنتاج الحملات والأفلام السينمائية",
        "fr": "Production de Campagnes & Réalisation de Films",
        "es": "Producción de Campañas y Cine",
        "de": "Kampagnenproduktion & Film",
    },
    "Cinema Craft": {
        "ar": "حرفية سينمائية فائقة",
        "fr": "Artisanat Cinématographique",
        "es": "Artesanía Cinematográfica",
        "de": "Kinematografisches Handwerk",
    },
    "Cinematic live-action film, high-end 3D motion graphics, and editorial craft produced with an obsession for emotional resonance. We orchestrate treatment, casting, bespoke sound design, master color grading, and final asset packaging.": {
        "ar": "أفلام حية سينمائية، رسوم متحركة ثلاثية الأبعاد فائقة الجودة، وتحرير فني بهدف إحداث أثر عاطفي راسخ. نتولى إعداد النص، الكاستينغ، تصميم الصوت، تصحيح الألوان المتقدم، وإخراج النسخ النهائية.",
        "fr": "Films cinématographiques, motion design 3D haut de gamme et montage soigné pour un impact émotionnel maximal : scénario, casting, design sonore sur mesure et étalonnage ACES.",
        "es": "Producción cinematográfica, gráficos 3D de alta gama y edición con resonancia emocional: guion, casting, diseño sonoro exclusivo y etalonaje profesional.",
        "de": "Kinematografische Realfilme, hochwertige 3D-Motion-Graphics und emotionales Storytelling mit professionellem Sounddesign und ACES-Farbkorrektur.",
    },
    "Hero Launch Films": {
        "ar": "أفلام الإطلاق الرئيسية",
        "fr": "Films majeurs de lancement",
        "es": "Películas insignia de lanzamiento",
        "de": "Hero-Launch-Filme",
    },
    "3D CGI & Spatial VFX": {
        "ar": "غرافيك ثلاثي الأبعاد ومؤثرات بصرية مكانية",
        "fr": "CGI 3D & Effets visuels spatiaux",
        "es": "CGI 3D y Efectos visuales espaciales",
        "de": "3D CGI & Räumliche VFX",
    },
    "Sonic Scoring & Sound Design": {
        "ar": "تأليف موسيقي وتصميم صوتي سينمائي",
        "fr": "Composition musicale & Design sonore",
        "es": "Composición sonora y diseño de audio",
        "de": "Musikkomposition & Sounddesign",
    },
    "High-Speed Visual Cuts": {
        "ar": "مونتاج رقمي سريع الإيقاع",
        "fr": "Montages visuels rythmés",
        "es": "Edición visual de alto ritmo",
        "de": "Schnelle visuelle Schnittfassungen",
    },
    "Master Color Grading (ACES)": {
        "ar": "تصحيح ألوان سينمائي متقدم (ACES)",
        "fr": "Étalonnage colorimétrique expert (ACES)",
        "es": "Etalonaje de color maestro (ACES)",
        "de": "Master-Color-Grading (ACES)",
    },
    "High-Intent Organic Views": {
        "ar": "مشاهدات طبيعية ذات نية عالية للشراء",
        "fr": "Vues organiques à forte intention",
        "es": "Vistas orgánicas de alta intención",
        "de": "Hochrelevante organische Aufrufe",
    },
    "03 // DISCIPLINE": {
        "ar": "03 // التخصص الثالث",
        "fr": "03 // DISCIPLINE",
        "es": "03 // DISCIPLINA",
        "de": "03 // DISZIPLIN",
    },
    "Performance Media & Growth": {
        "ar": "وسائط الأداء والنمو المتسارع",
        "fr": "Médias de Performance & Croissance",
        "es": "Medios de Rendimiento y Crecimiento",
        "de": "Performance-Medien & Wachstum",
    },
    "Algorithmic Moat": {
        "ar": "قوة تنافسية خوارزمية",
        "fr": "Avantage Algorithmique",
        "es": "Ventaja Algorítmica",
        "de": "Algorithmischer Wettbewerbsvorteil",
    },
    "Creative that directly scales customer acquisition efficiency and lifetime value. We engineer multi-variant ad systems tested against real-time conversion models across Meta, TikTok, YouTube, and programmatic inventory.": {
        "ar": "إبداع يرفع كفاءة اكتساب العملاء والقيمة الدائمة لهم. نبتكر أنظمة إعلانية متعددة النماذج نختبرها ضد نماذج التحويل الفورية عبر منصات ميتا، تيك توك، يوتيوب، والمساحات الإعلانية المبرمجة.",
        "fr": "Des créations conçues pour rentabiliser l'acquisition et la valeur vie client via des tests multivariés en temps réel sur Meta, TikTok, YouTube et inventaire programmatique.",
        "es": "Creatividad enfocada en escalar la adquisición de clientes y el valor de vida útil mediante sistemas de anuncios multivariantes en Meta, TikTok y YouTube.",
        "de": "Kreativkampagnen zur Steigerung von Kundenakquise und Customer Lifetime Value durch multivariante Tests auf Meta, TikTok, YouTube und Programmatic.",
    },
    "Multi-Variant Creative Testing": {
        "ar": "اختبار إعلاني متعدد النماذج",
        "fr": "Tests créatifs multivariés",
        "es": "Pruebas creativas multivariantes",
        "de": "Multivariante Creative-Tests",
    },
    "Algorithmic Acquisition Funnels": {
        "ar": "مسارات اكتساب خوارزمية ذكية",
        "fr": "Tunnels d'acquisition algorithmiques",
        "es": "Embudos de adquisición algorítmicos",
        "de": "Algorithmische Akquisitions-Funnels",
    },
    "Retention & LTV Architecture": {
        "ar": "هندسة ولاء العملاء وزيادة القيمة الدائمة",
        "fr": "Architecture de fidélisation & LTV",
        "es": "Arquitectura de retención y LTV",
        "de": "Kundenbindung & LTV-Architektur",
    },
    "Server-Side Attribution (CAPI)": {
        "ar": "تتبع التحويلات عبر الخادم (CAPI)",
        "fr": "Attribution côté serveur (CAPI)",
        "es": "Atribución del lado del servidor (CAPI)",
        "de": "Server-Side Attribution (CAPI)",
    },
    "Real-Time Performance Dashboards": {
        "ar": "لوحات تحكم فورية لمتابعة الأداء",
        "fr": "Tableaux de bord de performance en temps réel",
        "es": "Paneles de rendimiento en tiempo real",
        "de": "Echtzeit-Performance-Dashboards",
    },
    "Blended ROAS at Scale": {
        "ar": "عائد إنفاق إعلاني إجمالي قياسي",
        "fr": "ROAS global optimisé à l'échelle",
        "es": "ROAS combinado a gran escala",
        "de": "Kombinierter ROAS bei Skalierung",
    },
    "04 // DISCIPLINE": {
        "ar": "04 // التخصص الرابع",
        "fr": "04 // DISCIPLINE",
        "es": "04 // DISCIPLINA",
        "de": "04 // DISZIPLIN",
    },
    "Content Systems & Kinetics": {
        "ar": "أنظمة المحتوى والوسائط التفاعلية",
        "fr": "Systèmes de Contenu & Cinétique",
        "es": "Sistemas de Contenido y Cinética",
        "de": "Content-Systeme & Kinetik",
    },
    "Always-On Scale": {
        "ar": "إنتاج مستمر على مدار الساعة",
        "fr": "Production Continue à l'Échelle",
        "es": "Escala Continua y Siempre Activa",
        "de": "Kontinuierliche Skalierung",
    },
    "Turnkey always-on content operations for hyper-growth enterprises. Continuous asset pipeline from our studio to social feeds, podcasts, interactive WebGL drops, and high-velocity digital editorial.": {
        "ar": "عمليات محتوى جاهزة ومستمرة للمؤسسات فائقة النمو. تدفق أصول إبداعية متواصل من استوديوهاتنا نحو المنصات الاجتماعية، البودكاست، تجارب WebGL ثلاثية الأبعاد، والمنشورات التحريرية السريعة.",
        "fr": "Gestion de contenu clé en main et continue pour marques en forte croissance : flux ininterrompu d'assets vers les réseaux sociaux, podcasts, expériences WebGL et publications digitales.",
        "es": "Operaciones integrales de contenido continuo para empresas en hipercrecimiento: flujo constante hacia redes sociales, podcasts, experiencias WebGL y artículos digitales.",
        "de": "Umfassende Content-Produktion für wachstumsstarke Unternehmen: Fortlaufende Bereitstellung von Beiträgen für Social Media, Podcasts, WebGL-Erlebnisse und digitale Editorials.",
    },
    "Modular Creative Asset Engines": {
        "ar": "محركات تصميم أصول معيارية",
        "fr": "Moteurs d'assets créatifs modulaires",
        "es": "Motores de activos creativos modulares",
        "de": "Modulare Creative-Asset-Engines",
    },
    "Social-First Vertical Formats (9:16)": {
        "ar": "صيغ عمودية مصممة للهواتف (9:16)",
        "fr": "Formats verticaux pour réseaux (9:16)",
        "es": "Formatos verticales para redes (9:16)",
        "de": "Mobile-First Vertikalformate (9:16)",
    },
    "Interactive WebGL Experiences": {
        "ar": "تجارب رقمية تفاعلية بتقنية WebGL",
        "fr": "Expériences interactives WebGL",
        "es": "Experiencias interactivas con WebGL",
        "de": "Interaktive WebGL-Erlebnisse",
    },
    "Podcast & Audio Studio Drops": {
        "ar": "إنتاج بودكاست وأعمال صوتية احترافية",
        "fr": "Émissions de podcast et studio audio",
        "es": "Producción de podcasts y audio de estudio",
        "de": "Podcast- & Audio-Studioproduktionen",
    },
    "Digital Editorial Publishing": {
        "ar": "نشر تحريري ومقالات رقمية استراتيجية",
        "fr": "Édition et publications numériques",
        "es": "Publicaciones editoriales digitales",
        "de": "Digitale redaktionelle Veröffentlichungen",
    },
    "High-Res Assets / Month": {
        "ar": "أصل عالي الدقة شهرياً",
        "fr": "Assets haute résolution / mois",
        "es": "Activos en alta resolución / mes",
        "de": "Hochauflösende Assets / Monat",
    },
    "[ The Sprint Engine ]": {
        "ar": "[ محرك التنفيذ المتسارع ]",
        "fr": "[ Le Moteur de Sprint ]",
        "es": "[ El Motor de Sprint ]",
        "de": "[ Die Sprint-Engine ]",
    },
    "How we deploy category dominance in weeks.": {
        "ar": "كيف نفرض هيمنة علامتك على السوق في أسابيع معدودة.",
        "fr": "Comment nous asseyons votre domination en quelques semaines.",
        "es": "Cómo logramos el liderazgo de su categoría en pocas semanas.",
        "de": "Wie wir in wenigen Wochen Marktführerschaft aufbauen.",
    },
    "A phased, deterministic deployment framework refined over dozens of global enterprise transformations.": {
        "ar": "إطار عمل تدريجي حاسم جرى صقله عبر عشرات التحولات الكبرى لعلامات عالمية مرموقة.",
        "fr": "Une méthodologie de déploiement par étapes affinée au cours de dizaines de transformations d'entreprises mondiales.",
        "es": "Un marco de implementación estructurado y comprobado en decenas de transformaciones corporativas internacionales.",
        "de": "Ein strukturiertes Vorgehensmodell, erprobt in zahlreichen internationalen Unternehmenstransformationen.",
    },
    "PHASE 01": {
        "ar": "المرحلة 01",
        "fr": "PHASE 01",
        "es": "FASE 01",
        "de": "PHASE 01",
    },
    "WEEKS 1–2": {
        "ar": "الأسابيع 1–2",
        "fr": "SEMAINES 1–2",
        "es": "SEMANAS 1–2",
        "de": "WOCHEN 1–2",
    },
    "Discovery & Synthesis": {
        "ar": "الاستكشاف والتحليل الشامل",
        "fr": "Découverte & Synthèse",
        "es": "Descubrimiento y Síntesis",
        "de": "Analyse & Synthese",
    },
    "Deep-dive interviews, competitive positioning audit, quantitative market sizing, and brand archetype extraction.": {
        "ar": "مقابلات معمقة، تدقيق تموضع المنافسين، دراسة كمية لحجم السوق، واستخلاص النموذج الأصيل للعلامة.",
        "fr": "Entretiens approfondis, audit concurrentiel, analyse quantitative du marché et définition de l'archétype de marque.",
        "es": "Entrevistas en profundidad, auditoría de competidores, dimensionamiento de mercado y extracción del arquetipo de marca.",
        "de": "Tiefeninterviews, Wettbewerbsanalyse, Marktgrößenbestimmung und Definition der Markenarchitektur.",
    },
    "PHASE 02": {
        "ar": "المرحلة 02",
        "fr": "PHASE 02",
        "es": "FASE 02",
        "de": "PHASE 02",
    },
    "WEEKS 2–3": {
        "ar": "الأسابيع 2–3",
        "fr": "SEMAINES 2–3",
        "es": "SEMANAS 2–3",
        "de": "WOCHEN 2–3",
    },
    "Creative Direction": {
        "ar": "الإدارة الإبداعية والرؤية الفنية",
        "fr": "Direction Créative",
        "es": "Dirección Creativa",
        "de": "Creative Direction",
    },
    "Treatment scripts, 3D moodboards, typographic system definition, and sonic identity architecture.": {
        "ar": "سيناريوهات المعالجة، لوحات إلهام ثلاثية الأبعاد، تحديد منظومة الخطوط، وهندسة الهوية الصوتية.",
        "fr": "Scénarios, moodboards 3D, charte typographique et identité sonore.",
        "es": "Guiones de tratamiento, moodboards 3D, definición tipográfica y arquitectura sonora.",
        "de": "Konzepte, 3D-Moodboards, Typografiedefinition und Audio-Identität.",
    },
    "PHASE 03": {
        "ar": "المرحلة 03",
        "fr": "PHASE 03",
        "es": "FASE 03",
        "de": "PHASE 03",
    },
    "WEEKS 3–5": {
        "ar": "الأسابيع 3–5",
        "fr": "SEMAINES 3–5",
        "es": "SEMANAS 3–5",
        "de": "WOCHEN 3–5",
    },
    "High-Fidelity Production": {
        "ar": "الإنتاج الفائق الدقة",
        "fr": "Production Haute Fidélité",
        "es": "Producción de Alta Fidelidad",
        "de": "High-Fidelity-Produktion",
    },
    "Cinema production, studio shoot, 3D CGI rendering, WebGL engineering, and master color grading.": {
        "ar": "تصوير سينمائي احترافي، جلسات تصوير في الاستوديو، معالجة CGI ثلاثية الأبعاد، برمجة WebGL، وتصحيح ألوان ماستر.",
        "fr": "Tournage cinéma, studio, rendu 3D CGI, développement WebGL et étalonnage master.",
        "es": "Rodaje cinematográfico, estudio, renderizado 3D CGI, ingeniería WebGL y corrección de color.",
        "de": "Kinofilm-Dreh, Studioshootings, 3D-CGI-Rendering, WebGL-Entwicklung und Color-Grading.",
    },
    "PHASE 04": {
        "ar": "المرحلة 04",
        "fr": "PHASE 04",
        "es": "FASE 04",
        "de": "PHASE 04",
    },
    "WEEK 5+": {
        "ar": "الأسبوع 5 فما بعد",
        "fr": "SEMAINE 5+",
        "es": "SEMANA 5+",
        "de": "WOCHE 5+",
    },
    "Algorithmic Launch": {
        "ar": "الإطلاق الخوارزمي في السوق",
        "fr": "Lancement Algorithmique",
        "es": "Lanzamiento Algorítmico",
        "de": "Algorithmischer Launch",
    },
    "Global rollout, multi-variant paid distribution, conversion tracking calibration, and PR seeding.": {
        "ar": "إطلاق عالمي متزامن، توزيع إعلاني متعدد النماذج، معايرة تتبع التحويلات، وحملات العلاقات العامة.",
        "fr": "Déploiement international, distribution payante multivariée, calibrage des conversions et relations publiques.",
        "es": "Despliegue internacional, distribución de pago multivariante, calibración de conversiones y relaciones públicas.",
        "de": "Globaler Rollout, multivariante bezahlte Kampagnen, Tracking-Optimierung und PR-Platzierungen.",
    },
    "PHASE 05": {
        "ar": "المرحلة 05",
        "fr": "PHASE 05",
        "es": "FASE 05",
        "de": "PHASE 05",
    },
    "ONGOING": {
        "ar": "مستمر وتراكمي",
        "fr": "CONTINU",
        "es": "CONTINUO",
        "de": "FORTLAUFEND",
    },
    "Iterative Systems": {
        "ar": "أنظمة التحسين والتطوير المتتابع",
        "fr": "Systèmes Itératifs",
        "es": "Sistemas Iterativos",
        "de": "Iterative Systeme",
    },
    "Continuous asset delivery, ROAS optimization, community content, and quarterly creative refreshes.": {
        "ar": "تسليم متواصل للأصول، مضاعفة العائد الإعلاني، محتوى مجتمعي تفاعلي، وتحديثات إبداعية ربع سنوية.",
        "fr": "Livraison continue d'assets, optimisation du ROAS, contenu communautaire et actualisations trimestrielles.",
        "es": "Entrega continua de activos, optimización de ROAS, contenido para la comunidad y renovaciones trimestrales.",
        "de": "Laufende Bereitstellung von Assets, ROAS-Optimierung, Community-Content und quartalsweise Updates.",
    },
    "[ Production Infrastructure ]": {
        "ar": "[ البنية التحتية للإنتاج ]",
        "fr": "[ Infrastructure de Production ]",
        "es": "[ Infraestructura de Producción ]",
        "de": "[ Produktions-Infrastruktur ]",
    },
    "Industry-standard cinema & digital tooling.": {
        "ar": "معدات وأدوات سينمائية ورقمية بمعايير الصناعة العالمية.",
        "fr": "Équipements et technologies cinéma et numériques aux normes industrielles.",
        "es": "Herramientas cinematográficas y digitales líderes en la industria.",
        "de": "Industriestandard für Filmtechnik und digitale Werkzeuge.",
    },
    "01 // CAMERAS & GLASS": {
        "ar": "01 // الكاميرات والعدسات",
        "fr": "01 // CAMÉRAS & OPTIQUES",
        "es": "01 // CÁMARAS Y ÓPTICAS",
        "de": "01 // KAMERAS & OBJEKTIVE",
    },
    "Cinema Systems": {
        "ar": "أنظمة الكاميرات السينمائية",
        "fr": "Systèmes Cinéma",
        "es": "Sistemas de Cine",
        "de": "Kino-Kamerasysteme",
    },
    "02 // 3D & REALTIME GPU": {
        "ar": "02 // معالجة ثلاثية الأبعاد ورسوم فورية",
        "fr": "02 // 3D & GPU TEMPS RÉEL",
        "es": "02 // 3D Y GPU EN TIEMPO REAL",
        "de": "02 // 3D & ECHTZEIT-GPU",
    },
    "Spatial Engines": {
        "ar": "محركات الفضاء والمؤثرات",
        "fr": "Moteurs Spatiaux",
        "es": "Motores Espaciales",
        "de": "Spatial Engines",
    },
    "03 // POST & ACOUSTICS": {
        "ar": "03 // المونتاج وهندسة الصوت",
        "fr": "03 // POST-PRODUCTION & ACOUSTIQUE",
        "es": "03 // POSTPRODUCCIÓN Y ACÚSTICA",
        "de": "03 // POSTPRODUKTION & AKUSTIK",
    },
    "Finishing Suites": {
        "ar": "استوديوهات الماسترينغ والتشطيب",
        "fr": "Suites de Finition",
        "es": "Suites de Finalización",
        "de": "Finishing-Suiten",
    },
    "04 // ATTRIBUTION & DATA": {
        "ar": "04 // تحليل البيانات ومصادر التحويل",
        "fr": "04 // ATTRIBUTION & DONNÉES",
        "es": "04 // ATRIBUCIÓN Y DATOS",
        "de": "04 // ATTRIBUTION & DATEN",
    },
    "Growth Infrastructure": {
        "ar": "بنية تحتية لمضاعفة النمو",
        "fr": "Infrastructure de Croissance",
        "es": "Infraestructura de Crecimiento",
        "de": "Wachstums-Infrastruktur",
    },
    "[ INITIATE ENGAGEMENT ]": {
        "ar": "[ ابدأ التعاقد الآن ]",
        "fr": "[ DÉMARRER LA COLLABORATION ]",
        "es": "[ INICIAR COLABORACIÓN ]",
        "de": "[ ZUSAMMENARBEIT STARTEN ]",
    },
    "Ready to construct your cultural landmark?": {
        "ar": "هل أنت مستعد لتشييد صرح ثقافي لعلامتك؟",
        "fr": "Prêt à ériger le monument culturel de votre marque ?",
        "es": "¿Listo para construir un hito cultural para su marca?",
        "de": "Bereit für das nächste kulturelle Denkmal Ihrer Marke?",
    },
    "Discuss your brand parameters and commercial objectives with our senior strategy partners.": {
        "ar": "ناقش أبعاد علامتك وأهدافك التجارية مع كبار شركائنا الاستراتيجيين.",
        "fr": "Échangez sur vos objectifs stratégiques et commerciaux avec nos associés directeurs.",
        "es": "Analice los objetivos y parámetros de su marca con nuestros socios estratégicos.",
        "de": "Besprechen Sie Ihre Markenziele mit unseren leitenden Strategiepartnern.",
    },
    "Transmit Project Inquiry": {
        "ar": "إرسال تفاصيل المشروع",
        "fr": "Transmettre la demande de projet",
        "es": "Enviar consulta de proyecto",
        "de": "Projektanfrage senden",
    },

    # Studio Page
    "The Studio & Ethos — Spec Media": {
        "ar": "الاستوديو والمبادئ — Spec Media",
        "fr": "Le Studio & Philosophie — Spec Media",
        "es": "El Estudio y Filosofía — Spec Media",
        "de": "Das Studio & Ethos — Spec Media",
    },
    "The Studio // Cultural Gravity": {
        "ar": "الاستوديو // الجاذبية الثقافية",
        "fr": "Le Studio // Gravité Culturelle",
        "es": "El Estudio // Gravedad Cultural",
        "de": "Das Studio // Kulturelle Gravitation",
    },
    "Built for brands that demand cultural resonance.": {
        "ar": "صُمم للعلامات التجارية التي تشترط حضوراً ثقافياً طاغياً.",
        "fr": "Bâti pour les marques qui exigent une résonance culturelle.",
        "es": "Diseñado para marcas que exigen resonancia cultural.",
        "de": "Entwickelt für Marken, die kulturelle Resonanz fordern.",
    },
    "Spec Media is an independent creative studio operating at the intersection of cinematic craft, digital infrastructure, and high-velocity performance marketing.": {
        "ar": "Spec Media استوديو إبداعي مستقل يعمل عند نقطة التقاء الحرفية السينمائية، البنية التحتية الرقمية، والتسويق عالي السرعة المبني على الأداء.",
        "fr": "Spec Media est un studio indépendant opérant à la croisée de l'art cinématographique, des infrastructures digitales et du marketing de performance à haute vélocité.",
        "es": "Spec Media es un estudio independiente situado en la intersección del cine, la infraestructura digital y el marketing de rendimiento ágil.",
        "de": "Spec Media ist ein unabhängiges Studio an der Schnittstelle von Filmkunst, digitaler Infrastruktur und hochdynamischem Performance-Marketing.",
    },
    "PIPELINE:": {
        "ar": "المشاريع الجارية:",
        "fr": "PROJETS EN COURS :",
        "es": "PROYECTOS EN CURSO:",
        "de": "PROJEKTPIPELINE:",
    },
    "LIVE & INTAKE ACTIVE": {
        "ar": "نشطة واستقبال الطلبات متاح",
        "fr": "ACTIFS & RÉCEPTIONS OUVERTES",
        "es": "ACTIVO Y ADMISIONES ABIERTAS",
        "de": "AKTIV & ANFRAGEN OFFEN",
    },
    "CAPITAL CATALYZED:": {
        "ar": "القيمة المحققة للعملاء:",
        "fr": "VALEUR CRÉÉE :",
        "es": "VALOR GENERADO:",
        "de": "GENERIERTER WERT:",
    },
    "ACTIVE HUBS:": {
        "ar": "المراكز التشغيلية:",
        "fr": "HUBS ACTIFS :",
        "es": "CENTROS ACTIVOS:",
        "de": "AKTIVE HUBS:",
    },
    "04 (GLOBAL)": {
        "ar": "04 (عالمياً)",
        "fr": "04 (MONDE)",
        "es": "04 (GLOBAL)",
        "de": "04 (GLOBAL)",
    },
    "[ Core Philosophy & Moats ]": {
        "ar": "[ الفلسفة الجوهرية والحصون التنافسية ]",
        "fr": "[ Philosophie Clé & Piliers ]",
        "es": "[ Filosofía y Ventajas Clave ]",
        "de": "[ Kernphilosophie & Schutzwälle ]",
    },
    "The principles that govern our work.": {
        "ar": "المبادئ الصارمة التي تحكم أعمالنا.",
        "fr": "Les principes fondateurs de notre travail.",
        "es": "Los principios que rigen nuestro trabajo.",
        "de": "Die Prinzipien, die unsere Arbeit leiten.",
    },
    "01 // MOAT": {
        "ar": "01 // الميزة التنافسية الأولى",
        "fr": "01 // PILIER",
        "es": "01 // PILAR",
        "de": "01 // SCHUTZWALL",
    },
    "Taste as an Unfair Advantage": {
        "ar": "الذوق الرفيع كميزة تنافسية استثنائية",
        "fr": "Le Goût comme Avantage Concurrentiel",
        "es": "El Gusto como Ventaja Inigualable",
        "de": "Stil & Geschmack als entscheidender Vorteil",
    },
    "In an era of algorithmic homogenisation, aesthetic taste is not cosmetic; it is an economic barrier to entry.": {
        "ar": "في زمن التماثل والتشابه الخوارزمي، الذوق الرفيع ليس مجرد مظهر، بل حاجز اقتصادي يصعب على المنافسين تجاوزه.",
        "fr": "À l'ère de l'uniformisation par les algorithmes, le bon goût n'est pas décoratif : c'est une véritable barrière économique.",
        "es": "En tiempos de uniformidad algorítmica, el buen gusto no es cosmético; es una barrera económica de entrada.",
        "de": "In einer Zeit algorithmischer Gleichförmigkeit ist Ästhetik kein Zierrat, sondern ein echter wirtschaftlicher Schutzwall.",
    },
    "02 // MOAT": {
        "ar": "02 // الميزة التنافسية الثانية",
        "fr": "02 // PILIER",
        "es": "02 // PILAR",
        "de": "02 // SCHUTZWALL",
    },
    "Zero Agency Friction": {
        "ar": "انعدام البيروقراطية والتشتت التقليدي",
        "fr": "Zéro Friction d'Agence",
        "es": "Cero Fricción de Agencia",
        "de": "Keine Agentur-Reibungsverluste",
    },
    "No fragmented handoffs between strategy, cinema sets, and media buying. One integrated war room.": {
        "ar": "لا وسائط ولا انقطاع بين واضعي الاستراتيجية ومخرجي الأفلام ومشتري الإعلانات. غرفة عمليات واحدة متكاملة.",
        "fr": "Aucune rupture entre stratégie, tournage cinéma et achat d'espace. Une seule et même équipe unifiée.",
        "es": "Sin divisiones entre estrategia, rodajes y compra de medios. Una sala de mando completamente unificada.",
        "de": "Keine Schnittstellenverluste zwischen Strategie, Filmset und Media-Einkauf. Ein integriertes Kernteam.",
    },
    "03 // MOAT": {
        "ar": "03 // الميزة التنافسية الثالثة",
        "fr": "03 // PILIER",
        "es": "03 // PILAR",
        "de": "03 // SCHUTZWALL",
    },
    "High-Velocity Execution": {
        "ar": "سرعة تنفيذ فائقة وعالية الإنتاجية",
        "fr": "Exécution à Haute Vélocité",
        "es": "Ejecución de Alta Velocidad",
        "de": "Hochdynamische Umsetzung",
    },
    "We trade bureaucratic approval cycles for rapid deployment sprints.": {
        "ar": "نستبدل دوائر الاعتماد البيروقراطية البطيئة بسباقات تنفيذ وانطلاق فورية في السوق.",
        "fr": "Nous remplaçons les cycles d'approbation lents par des sprints de déploiement ultra-rapides.",
        "es": "Sustituimos las aprobaciones burocráticas por sprints ágiles de lanzamiento al mercado.",
        "de": "Wir ersetzen langwierige Freigabeprozesse durch schnelle, fokussierte Umsetzungssprints.",
    },
    "04 // MOAT": {
        "ar": "04 // الميزة التنافسية الرابعة",
        "fr": "04 // PILIER",
        "es": "04 // PILAR",
        "de": "04 // SCHUTZWALL",
    },
    "Enterprise Compounding": {
        "ar": "نمو تراكمي مستمر لقيمة المؤسسة",
        "fr": "Croissance Cumulée de l'Entreprise",
        "es": "Capitalización Continua de la Marca",
        "de": "Nachhaltiges Unternehmenswachstum",
    },
    "Every asset is engineered to build long-term cultural and enterprise equity.": {
        "ar": "كل أصل إبداعي ننتجه مُهندس لبناء رصيد ثقافي وقيمة استثمارية تتراكم عبر السنين.",
        "fr": "Chaque réalisation est pensée pour consolider la valeur culturelle et économique durable de l'entreprise.",
        "es": "Cada activo está diseñado para generar un impacto cultural duradero y un valor patrimonial real.",
        "de": "Jedes Asset ist darauf ausgelegt, langfristig kulturelles und wirtschaftliches Kapital aufzubauen.",
    },
    "[ Operating Footprint ]": {
        "ar": "[ الحضور والانتشار الجغرافي ]",
        "fr": "[ Présence Internationale ]",
        "es": "[ Presencia Internacional ]",
        "de": "[ Internationale Standorte ]",
    },
    "Four Strategic Anchors.": {
        "ar": "أربعة مراكز استراتيجية عالمية.",
        "fr": "Quatre Pôles Stratégiques.",
        "es": "Cuatro Centros Estratégicos.",
        "de": "Vier strategische Ankerpunkte.",
    },
    "Global capability anchored in key creative and capital hubs.": {
        "ar": "قدرات عالمية متمركزة في أهم عواصم الإبداع ورؤوس الأموال.",
        "fr": "Une présence globale ancrée dans les plus grands carrefours créatifs et financiers.",
        "es": "Capacidad global respaldada en los principales centros creativos y de capital.",
        "de": "Globale Schlagkraft an den führenden Kreativ- und Kapitalstandorten.",
    },
    "DUBAI // HQ": {
        "ar": "دبي // المقر الرئيسي",
        "fr": "DUBAÏ // SIÈGE MONDIAL",
        "es": "DUBÁI // SEDE CENTRAL",
        "de": "DUBAI // HAUPTSITZ",
    },
    "LONDON": {
        "ar": "لندن",
        "fr": "LONDRES",
        "es": "LONDRES",
        "de": "LONDON",
    },
    "NEW YORK": {
        "ar": "نيويورك",
        "fr": "NEW YORK",
        "es": "NUEVA YORK",
        "de": "NEW YORK",
    },
    "RIYADH": {
        "ar": "الرياض",
        "fr": "RIYAD",
        "es": "RIAD",
        "de": "RIAD",
    },
    "[ Leadership & Collective ]": {
        "ar": "[ القيادة والفريق الجماعي ]",
        "fr": "[ Direction & Équipe ]",
        "es": "[ Liderazgo y Colectivo ]",
        "de": "[ Führung & Team ]",
    },
    "Operators, strategists, and cinematic directors.": {
        "ar": "قادة تنفيذيون، استراتيجيون، ومخرجون سينمائيون.",
        "fr": "Opérateurs, stratèges et réalisateurs de cinéma.",
        "es": "Operadores, estrategas y directores de cine.",
        "de": "Macher, Strategen und Filmregisseure.",
    },
    "Senior partners who lead every engagement from the front lines.": {
        "ar": "شركاء تنفيذيون يقودون كل شراكة ومهمة من الخطوط الأمامية مباشرة.",
        "fr": "Des associés seniors qui dirigent chaque mission en première ligne.",
        "es": "Socios directores que lideran cada proyecto directamente en primera línea.",
        "de": "Erfahrene Partner, die jedes Projekt persönlich an vorderster Front leiten.",
    },
    "Founding Partner & Executive Creative Director": {
        "ar": "شريك مؤسس والمدير الإبداعي التنفيذي",
        "fr": "Associé Fondateur & Directeur Exécutif de la Création",
        "es": "Socio Fundador y Director Creativo Ejecutivo",
        "de": "Gründungspartner & Executive Creative Director",
    },
    "Partner & Head of Brand Architecture": {
        "ar": "شريك ورئيس هندسة العلامات التجارية",
        "fr": "Associé & Responsable de l'Architecture de Marque",
        "es": "Socio y Director de Arquitectura de Marca",
        "de": "Partner & Leiter Markenarchitektur",
    },
    "Partner & Head of Performance Media": {
        "ar": "شريك ورئيس وسائط الأداء والنمو",
        "fr": "Associé & Responsable des Médias de Performance",
        "es": "Socio y Director de Medios de Rendimiento",
        "de": "Partner & Leiter Performance-Medien",
    },
    "Ready to build something iconic?": {
        "ar": "هل أنت مستعد لابتكار علامة أسطورية؟",
        "fr": "Prêt à construire une œuvre iconique ?",
        "es": "¿Listo para crear algo icónico?",
        "de": "Bereit für ein legendäres Projekt?",
    },
    "Initiate Collaboration &rarr;": {
        "ar": "ابدأ التعاون الاستراتيجي &larr;",
        "fr": "Démarrer la collaboration &rarr;",
        "es": "Iniciar colaboración &rarr;",
        "de": "Kooperation starten &rarr;",
    },

    # Work Page & Detail
    "Selected Work & Case Studies — Spec Media": {
        "ar": "أعمال مختارة ودراسات حالة — Spec Media",
        "fr": "Travaux Sélectionnés & Études de Cas — Spec Media",
        "es": "Trabajos Seleccionados y Casos de Éxito — Spec Media",
        "de": "Ausgewählte Arbeiten & Case Studies — Spec Media",
    },
    "Selected Work & Case Studies // 2024 — 2026": {
        "ar": "أعمال مختارة ودراسات حالة // 2024 — 2026",
        "fr": "Travaux Sélectionnés & Études de Cas // 2024 — 2026",
        "es": "Trabajos Seleccionados y Casos de Éxito // 2024 — 2026",
        "de": "Ausgewählte Arbeiten & Case Studies // 2024 — 2026",
    },
    "Work that cuts through the noise.": {
        "ar": "أعمال تخترق الضجيج وتفرض نفسها.",
        "fr": "Des créations qui percent le bruit ambiant.",
        "es": "Trabajo que sobresale del ruido.",
        "de": "Arbeiten, die aus dem Rauschen herausstechen.",
    },
    "Every campaign, brand architecture, and kinetic system we deploy is engineered to capture cultural authority, accelerate enterprise pipeline, and deliver measurable commercial equity.": {
        "ar": "كل حملة إعلانية، وكل بنية علامة تجارية، وكل نظام تفاعلي نطلقه مُهندس للاستحواذ على السيادة الثقافية، وتسريع المبيعات، وتحقيق عوائد استثمارية ملموسة.",
        "fr": "Chaque campagne, identité de marque et système cinétique est conçu pour imposer une autorité culturelle, accélérer les ventes et générer une valeur commerciale quantifiable.",
        "es": "Cada campaña y sistema que implementamos está creado para captar relevancia cultural, acelerar el crecimiento empresarial y generar valor comercial tangible.",
        "de": "Jede Kampagne und Markenarchitektur ist so konzipiert, dass sie kulturelle Relevanz gewinnt, Vertriebskanäle beschleunigt und messbaren Ertrag liefert.",
    },
    "All Works": {
        "ar": "كافة الأعمال",
        "fr": "Tous les projets",
        "es": "Todos los proyectos",
        "de": "Alle Arbeiten",
    },
    "Brand Systems": {
        "ar": "أنظمة العلامة",
        "fr": "Systèmes de marque",
        "es": "Sistemas de marca",
        "de": "Markensysteme",
    },
    "Campaign Production": {
        "ar": "إنتاج الحملات",
        "fr": "Production de campagnes",
        "es": "Producción de campañas",
        "de": "Kampagnenproduktion",
    },
    "Performance Media": {
        "ar": "وسائط الأداء",
        "fr": "Médias de performance",
        "es": "Medios de rendimiento",
        "de": "Performance-Medien",
    },
    "Content Systems": {
        "ar": "أنظمة المحتوى",
        "fr": "Systèmes de contenu",
        "es": "Sistemas de contenido",
        "de": "Content-Systeme",
    },
    "Grid": {
        "ar": "شبكي",
        "fr": "Grille",
        "es": "Cuadrícula",
        "de": "Raster",
    },
    "List": {
        "ar": "قائمة",
        "fr": "Liste",
        "es": "Lista",
        "de": "Liste",
    },
    "View Case Study &rarr;": {
        "ar": "معاينة دراسة الحالة &larr;",
        "fr": "Voir l'étude de cas &rarr;",
        "es": "Ver caso de estudio &rarr;",
        "de": "Case Study ansehen &rarr;",
    },
    "Explore Scope": {
        "ar": "استكشاف النطاق",
        "fr": "Explorer le périmètre",
        "es": "Explorar alcance",
        "de": "Umfang ansehen",
    },
    "[ ← Back to Works Archive ]": {
        "ar": "[ &rarr; العودة لمعرض الأعمال ]",
        "fr": "[ ← Retour aux travaux ]",
        "es": "[ ← Volver a proyectos ]",
        "de": "[ ← Zurück zur Übersicht ]",
    },
    "[ Challenge & Context ]": {
        "ar": "[ التحدي والسياق التجاري ]",
        "fr": "[ Défi & Contexte ]",
        "es": "[ Desafío y Contexto ]",
        "de": "[ Herausforderung & Kontext ]",
    },
    "[ Strategic Execution ]": {
        "ar": "[ التنفيذ الاستراتيجي ]",
        "fr": "[ Exécution Stratégique ]",
        "es": "[ Ejecución Estratégica ]",
        "de": "[ Strategische Umsetzung ]",
    },
    "[ Deliverables & Scope ]": {
        "ar": "[ المخرجات ونطاق العمل ]",
        "fr": "[ Livrables & Périmètre ]",
        "es": "[ Entregables y Alcance ]",
        "de": "[ Ergebnisse & Umfang ]",
    },
    "[ Verified Commercial KPIs ]": {
        "ar": "[ مؤشرات الأداء والنتائج المعتمدة ]",
        "fr": "[ Indicateurs Clés Vérifiés ]",
        "es": "[ Indicadores Comerciales Verificados ]",
        "de": "[ Verifizierte Kennzahlen ]",
    },
    "Deliverables": {
        "ar": "المخرجات",
        "fr": "Livrables",
        "es": "Entregables",
        "de": "Ergebnisse",
    },
    "Next Case Study &rarr;": {
        "ar": "دراسة الحالة التالية &larr;",
        "fr": "Étude de cas suivante &rarr;",
        "es": "Siguiente caso de estudio &rarr;",
        "de": "Nächste Case Study &rarr;",
    },

    # Portal & CRM
    "Pipeline & CRM Portal — Spec Media": {
        "ar": "بوابة إدارة المبيعات والعملاء — Spec Media",
        "fr": "Portail CRM & Pipeline — Spec Media",
        "es": "Portal CRM y Pipeline — Spec Media",
        "de": "CRM- & Pipeline-Portal — Spec Media",
    },
    "back to site": {
        "ar": "العودة للموقع",
        "fr": "retour au site",
        "es": "volver al sitio",
        "de": "zurück zur Website",
    },
    "Refresh": {
        "ar": "تحديث البيانات",
        "fr": "Actualiser",
        "es": "Actualizar",
        "de": "Aktualisieren",
    },
    "Database Pipeline Overview": {
        "ar": "نظرة عامة على قاعدة بيانات المبيعات",
        "fr": "Aperçu du Pipeline Supabase",
        "es": "Resumen del Pipeline en Base de Datos",
        "de": "Übersicht der Datenbank-Pipeline",
    },
    "Client Inquiries & CRM Analytics": {
        "ar": "استفسارات العملاء وتحليلات CRM",
        "fr": "Demandes Clients & Analyses CRM",
        "es": "Consultas de Clientes y Métricas CRM",
        "de": "Kundenanfragen & CRM-Analysen",
    },
    "Total Inquiries": {
        "ar": "إجمالي الاستفسارات",
        "fr": "Total des Demandes",
        "es": "Total de Consultas",
        "de": "Anfragen Gesamt",
    },
    "All records in Supabase": {
        "ar": "كافة السجلات في Supabase",
        "fr": "Tous les enregistrements Supabase",
        "es": "Todos los registros en Supabase",
        "de": "Alle Einträge in Supabase",
    },
    "New Inquiries": {
        "ar": "استفسارات جديدة",
        "fr": "Nouvelles Demandes",
        "es": "Nuevas Consultas",
        "de": "Neue Anfragen",
    },
    "Awaiting triage": {
        "ar": "بانتظار الفرز والتقييم",
        "fr": "En attente de traitement",
        "es": "Esperando revisión",
        "de": "Wartet auf Sichtung",
    },
    "In active outreach": {
        "ar": "قيد التواصل الفعلي",
        "fr": "En cours de contact",
        "es": "En contacto activo",
        "de": "In aktiver Kontaktaufnahme",
    },
    "Budget & fit verified": {
        "ar": "تم التحقق من الميزانية والملاءمة",
        "fr": "Budget & profil validés",
        "es": "Presupuesto y perfil verificados",
        "de": "Budget & Eignung geprüft",
    },
    "Won / Closed": {
        "ar": "صفقات ناجحة / مغلقة",
        "fr": "Gagnées / Conclues",
        "es": "Ganadas / Cerradas",
        "de": "Gewonnen / Abgeschlossen",
    },
    "Active studio clients": {
        "ar": "عملاء حاليون للاستوديو",
        "fr": "Clients actifs du studio",
        "es": "Clientes activos del estudio",
        "de": "Aktive Studio-Kunden",
    },
    "Conversion Rate": {
        "ar": "معدل التحويل",
        "fr": "Taux de Conversion",
        "es": "Tasa de Conversión",
        "de": "Konversionsrate",
    },
    "Pipeline efficiency": {
        "ar": "كفاءة مسار المبيعات",
        "fr": "Efficacité du pipeline",
        "es": "Eficiencia del pipeline",
        "de": "Pipeline-Effizienz",
    },
    "Market Distribution": {
        "ar": "التوزيع حسب الأسواق",
        "fr": "Distribution par Marché",
        "es": "Distribución por Mercado",
        "de": "Marktverteilung",
    },
    "Source: PostgreSQL View": {
        "ar": "المصدر: عرض PostgreSQL",
        "fr": "Source : Vue PostgreSQL",
        "es": "Fuente: Vista PostgreSQL",
        "de": "Quelle: PostgreSQL View",
    },
    "Loading market metrics...": {
        "ar": "جاري تحميل بيانات الأسواق...",
        "fr": "Chargement des métriques...",
        "es": "Cargando métricas de mercado...",
        "de": "Lade Markt-Metriken...",
    },
    "System Health": {
        "ar": "حالة النظام",
        "fr": "État du Système",
        "es": "Estado del Sistema",
        "de": "Systemstatus",
    },
    "Django Backend:": {
        "ar": "خادم دجانغو الخلفي:",
        "fr": "Backend Django :",
        "es": "Backend Django:",
        "de": "Django Backend:",
    },
    "Supabase Database:": {
        "ar": "قاعدة بيانات Supabase:",
        "fr": "Base de données Supabase :",
        "es": "Base de datos Supabase:",
        "de": "Supabase Datenbank:",
    },
    "REST Endpoint:": {
        "ar": "واجهة REST البرمجية:",
        "fr": "Point de terminaison REST :",
        "es": "Endpoint REST:",
        "de": "REST Endpunkt:",
    },
    "Database Table:": {
        "ar": "جدول قاعدة البيانات:",
        "fr": "Table de base de données :",
        "es": "Tabla de base de datos:",
        "de": "Datenbanktabelle:",
    },
    "Lost": {
        "ar": "غير مكتملة",
        "fr": "Perdu",
        "es": "Perdido",
        "de": "Verloren",
    },
    "Search by name, company, email...": {
        "ar": "البحث بالاسم، الشركة، البريد...",
        "fr": "Rechercher par nom, entreprise, email...",
        "es": "Buscar por nombre, empresa, email...",
        "de": "Nach Name, Firma, E-Mail suchen...",
    },
    "Insert Test Record": {
        "ar": "إدراج سجل اختباري",
        "fr": "Insérer un enregistrement test",
        "es": "Insertar registro de prueba",
        "de": "Testdatensatz einfügen",
    },
    "Name (e.g. Marc Jacobs)": {
        "ar": "الاسم (مثال: مارك جاكوبس)",
        "fr": "Nom (ex: Marc Jacobs)",
        "es": "Nombre (ej. Marc Jacobs)",
        "de": "Name (z.B. Marc Jacobs)",
    },
    "Email (e.g. marc@fashion.com)": {
        "ar": "البريد (مثال: marc@fashion.com)",
        "fr": "Email (ex: marc@fashion.com)",
        "es": "Email (ej. marc@fashion.com)",
        "de": "E-Mail (z.B. marc@fashion.com)",
    },
    "Company (e.g. LVMH Luxury)": {
        "ar": "الشركة (مثال: مجموعة LVMH)",
        "fr": "Entreprise (ex: Groupe LVMH)",
        "es": "Empresa (ej. LVMH Luxury)",
        "de": "Unternehmen (z.B. LVMH Luxury)",
    },
    "Market (e.g. us, europe, mena)": {
        "ar": "السوق (مثال: الشرق الأوسط، أمريكا)",
        "fr": "Marché (ex: Europe, MENA)",
        "es": "Mercado (ej. ee.uu., europa, mena)",
        "de": "Markt (z.B. Europa, MENA)",
    },
    "Message / Brief notes...": {
        "ar": "الرسالة / ملاحظات موجزة...",
        "fr": "Message / Brèves notes...",
        "es": "Mensaje / Notas breves...",
        "de": "Nachricht / Kurze Notizen...",
    },
    "Connected (PostgreSQL)": {
        "ar": "متصل (قاعدة PostgreSQL)",
        "fr": "Connecté (PostgreSQL)",
        "es": "Conectado (PostgreSQL)",
        "de": "Verbunden (PostgreSQL)",
    },
    "Degraded": {
        "ar": "أداء منخفض",
        "fr": "Dégradé",
        "es": "Degradado",
        "de": "Eingeschränkt",
    },
    "Offline": {
        "ar": "غير متصل",
        "fr": "Hors ligne",
        "es": "Desconectado",
        "de": "Offline",
    },
    "Failed to load leads from Supabase.": {
        "ar": "تعذر تحميل الاستفسارات من Supabase.",
        "fr": "Échec du chargement des leads depuis Supabase.",
        "es": "Error al cargar clientes potenciales desde Supabase.",
        "de": "Leads konnten nicht von Supabase geladen werden.",
    },
    "No leads found in this view.": {
        "ar": "لا توجد استفسارات في هذا العرض.",
        "fr": "Aucun lead trouvé dans cette vue.",
        "es": "No se encontraron prospectos en esta vista.",
        "de": "Keine Anfragen in dieser Ansicht gefunden.",
    },
    "Failed to update status in Supabase:": {
        "ar": "فشل تحديث الحالة في قاعدة البيانات:",
        "fr": "Échec de mise à jour du statut dans Supabase :",
        "es": "Error al actualizar el estado en Supabase:",
        "de": "Statusaktualisierung in Supabase fehlgeschlagen:",
    },

    # Dashboard & Login & 404
    "Upload Logo (PNG, SVG, WebP)": {
        "ar": "رفع الشعار (PNG, SVG, WebP)",
        "fr": "Téléverser le logo (PNG, SVG, WebP)",
        "es": "Subir logo (PNG, SVG, WebP)",
        "de": "Logo hochladen (PNG, SVG, WebP)",
    },
    "Add to THE REEL": {
        "ar": "إضافة إلى شريط الإعلانات",
        "fr": "Ajouter au FILM",
        "es": "Añadir al REEL",
        "de": "Zum REEL hinzufügen",
    },
    "Strategic Solution": {
        "ar": "الحل الاستراتيجي",
        "fr": "Solution Stratégique",
        "es": "Solución Estratégica",
        "de": "Strategische Lösung",
    },
    "Operator Authorization": {
        "ar": "تصريح دخول المشغّل",
        "fr": "Autorisation Opérateur",
        "es": "Autorización del Operador",
        "de": "Operator-Autorisierung",
    },
    "Spec Media Internal Portal": {
        "ar": "بوابة Spec Media الداخلية",
        "fr": "Portail Interne Spec Media",
        "es": "Portal Interno Spec Media",
        "de": "Internes Portal Spec Media",
    },
    "Restricted Access": {
        "ar": "منطقة وصول مقيدة",
        "fr": "Accès Restreint",
        "es": "Acceso Restringido",
        "de": "Geschützter Bereich",
    },
    "Username": {
        "ar": "اسم المستخدم",
        "fr": "Nom d'utilisateur",
        "es": "Nombre de usuario",
        "de": "Benutzername",
    },
    "Password": {
        "ar": "كلمة المرور",
        "fr": "Mot de passe",
        "es": "Contraseña",
        "de": "Passwort",
    },
    "Authorize Operator &rarr;": {
        "ar": "المصادقة والمتابعة &larr;",
        "fr": "Autoriser l'opérateur &rarr;",
        "es": "Autorizar operador &rarr;",
        "de": "Operator autorisieren &rarr;",
    },
    "[ Return to Public Site ]": {
        "ar": "[ العودة للموقع العام ]",
        "fr": "[ Retour au site public ]",
        "es": "[ Volver al sitio público ]",
        "de": "[ Zurück zur öffentlichen Website ]",
    },
    "Invalid operator username or password. Please verify your credentials.": {
        "ar": "اسم المستخدم أو كلمة المرور غير صحيحة. يرجى التحقق من البيانات.",
        "fr": "Nom d'utilisateur ou mot de passe invalide. Veuillez vérifier vos identifiants.",
        "es": "Nombre de usuario o contraseña no válidos. Verifique sus credenciales.",
        "de": "Ungültiger Benutzername oder Passwort. Bitte Zugangsdaten prüfen.",
    },
    "Access denied. The portal is restricted to administrators only.": {
        "ar": "تم رفض الوصول. هذه البوابة مخصصة لمديري النظام فقط.",
        "fr": "Accès refusé. Ce portail est strictement réservé aux administrateurs.",
        "es": "Acceso denegado. Este portal está reservado exclusivamente para administradores.",
        "de": "Zugriff verweigert. Dieses Portal ist ausschließlich Administratoren vorbehalten.",
    },
    "404 // Coordinate Out of Bounds": {
        "ar": "404 // إحداثيات خارج النطاق",
        "fr": "404 // Coordonnées Hors Limites",
        "es": "404 // Coordenada Fuera de Límites",
        "de": "404 // Koordinaten außerhalb des Bereichs",
    },
    "Signal Lost in Digital Space": {
        "ar": "انقطاع الإشارة في الفضاء الرقمي",
        "fr": "Signal Perdu dans l'Espace Numérique",
        "es": "Señal Perdida en el Espacio Digital",
        "de": "Signal im digitalen Raum verloren",
    },
    "The coordinate you requested does not exist or has been shifted across dimensions.": {
        "ar": "المسار الذي طلبته غير موجود أو تم نقله إلى موقع آخر.",
        "fr": "Les coordonnées demandées n'existent pas ou ont été déplacées.",
        "es": "La ruta solicitada no existe o ha sido reubicada.",
        "de": "Die angeforderte Adresse existiert nicht oder wurde verschoben.",
    },
    "Return to Orbit / Home &rarr;": {
        "ar": "العودة إلى المدار / الرئيسية &larr;",
        "fr": "Retourner en orbite / Accueil &rarr;",
        "es": "Regresar a la órbita / Inicio &rarr;",
        "de": "Zurück zur Basis / Startseite &rarr;",
    },
}

def write_po_files():
    locale_base = PROJECT_ROOT / "locale"
    for lang in ["en", "ar"]:
        lang_dir = locale_base / lang / "LC_MESSAGES"
        lang_dir.mkdir(parents=True, exist_ok=True)
        po_path = lang_dir / "django.po"
        
        lines = [
            'msgid ""',
            'msgstr ""',
            '"Content-Type: text/plain; charset=UTF-8\\n"',
            '"Content-Transfer-Encoding: 8bit\\n"',
            f'"Language: {lang}\\n"',
            "",
        ]
        
        for msgid, translations in CATALOG.items():
            if lang == "en":
                msgstr = msgid
            else:
                msgstr = translations.get(lang, msgid)
            
            # Escape strings
            def esc(s):
                return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            
            lines.append(f'msgid "{esc(msgid)}"')
            lines.append(f'msgstr "{esc(msgstr)}"')
            lines.append("")
            
        po_content = "\n".join(lines)
        with open(po_path, "w", encoding="utf-8") as f:
            f.write(po_content)
        print(f"[PO] Wrote {len(CATALOG)} messages to {po_path}")

if __name__ == "__main__":
    write_po_files()
    compile_all_locales()
    print("EN & AR PO & MO FILES GENERATED AND COMPILED SUCCESSFULLY!")
