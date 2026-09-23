// One source of truth for every fact that appears on more than one page.
// The old site named the venue two different ways. That cannot happen here.

export const event = {
  name: 'PRINT2PACK',
  edition: '2026',
  startISO: '2026-11-16',
  endISO: '2026-11-18',
  organiser: 'Nile Trade Fairs',
  venue: {
    en: 'Jeddah Center for Exhibitions and Events',
    ar: 'مركز جدة للمعارض والفعاليات',
  },
  address: {
    en: '6345 El-Medina Road, Al Nuzha District, Jeddah, Saudi Arabia',
    ar: '٦٣٤٥ طريق المدينة، حي النزهة، جدة، المملكة العربية السعودية',
  },
  dates: {
    en: '16–18 November 2026',
    ar: '١٦–١٨ نوفمبر ٢٠٢٦',
  },
  // 21.617, 39.156 — Al Nuzha, Jeddah. OpenStreetMap lists this location as
  // "مركز جدة للمنتديات والفعاليات" (Jeddah Forums and Events Center), which matches the
  // name on their venue page rather than the one on their homepage.
  // TODO: have the client confirm the official English name.
  coords: { lat: 21.6169571, lon: 39.1564679 },
  email: 'ksa@nilefairs.com',
  whatsapp: '+966540628088',
};

export const locales = {
  en: { label: 'English', dir: 'ltr', other: 'ar', otherLabel: 'العربية', href: '/' },
  ar: { label: 'العربية', dir: 'rtl', other: 'en', otherLabel: 'English', href: '/ar/' },
};

export const nav = {
  // English navigation. Arabic is added below the object.
  en: [
    { label: 'Home', href: '/' },
    {
      label: 'About', href: '/about/', children: [
        { label: 'About Print2Pack', href: '/about/' },
        { label: 'Why Print2Pack', href: '/why/' },
        { label: 'Fact Sheet', href: '/fact-sheet/' },
        { label: 'Market Background', href: '/market-background/' },
        { label: 'Facts and Figures', href: '/facts-and-figures/' },
        { label: 'Marketing Campaign', href: '/marketing-campaign/' },
        { label: 'The Venue', href: '/venue/' },
        { label: 'The Organiser', href: '/organiser/' },
      ],
    },
    {
      label: 'Exhibitors', href: '/exhibitors/', children: [
        { label: 'Who Exhibits', href: '/exhibitors/' },
        { label: 'Book a Stand', href: '/book-a-stand/' },
        { label: 'Booth Specifications', href: '/booth-specifications/' },
        { label: 'Accommodation', href: '/accommodation/' },
        { label: 'Shipping and Logistics', href: '/logistics/' },
        { label: 'Exhibitor Logos', href: '/exhibitor-logos/' },
        { label: 'Exhibitor List', href: '/exhibitor-list/' },
      ],
    },
    {
      label: 'Visitors', href: '/visitors/', children: [
        { label: 'Who Visits', href: '/visitors/' },
        { label: 'Register to Visit', href: '/register/' },
        { label: 'Accommodation', href: '/accommodation/' },
      ],
    },
    {
      label: 'Downloads', href: '/brochure/', children: [
        { label: 'Brochure', href: '/brochure/' },
        { label: 'Post-Show Report', href: '/post-show-report/' },
      ],
    },
    {
      label: 'Media', href: '/media-partners/', children: [
        { label: 'Media Partners', href: '/media-partners/' },
        { label: 'Gallery', href: '/gallery/' },
      ],
    },
    { label: 'Be Our Partner', href: '/partner/' },
    { label: 'Contact', href: '/contact/' },
  ],
};

// Arabic navigation. Written in Modern Standard Arabic.
// TODO: have a native speaker review before launch.
nav.ar = [
  { label: 'الرئيسية', href: '/ar/' },
  {
    label: 'عن المعرض', href: '/ar/about/', children: [
      { label: 'عن برينت تو باك', href: '/ar/about/' },
      { label: 'لماذا برينت تو باك', href: '/ar/why/' },
      { label: 'معلومات المعرض', href: '/ar/fact-sheet/' },
      { label: 'نبذة عن السوق', href: '/ar/market-background/' },
      { label: 'حقائق وأرقام', href: '/ar/facts-and-figures/' },
      { label: 'الحملة التسويقية', href: '/ar/marketing-campaign/' },
      { label: 'مقر المعرض', href: '/ar/venue/' },
      { label: 'الجهة المنظّمة', href: '/ar/organiser/' },
    ],
  },
  {
    label: 'العارضون', href: '/ar/exhibitors/', children: [
      { label: 'من يعرض', href: '/ar/exhibitors/' },
      { label: 'احجز جناحك', href: '/ar/book-a-stand/' },
      { label: 'مواصفات الأجنحة', href: '/ar/booth-specifications/' },
      { label: 'الإقامة', href: '/ar/accommodation/' },
      { label: 'الشحن والخدمات اللوجستية', href: '/ar/logistics/' },
      { label: 'شعارات العارضين', href: '/ar/exhibitor-logos/' },
      { label: 'قائمة العارضين', href: '/ar/exhibitor-list/' },
    ],
  },
  {
    label: 'الزوار', href: '/ar/visitors/', children: [
      { label: 'من يزور', href: '/ar/visitors/' },
      { label: 'تسجيل الزوار', href: '/ar/register/' },
      { label: 'الإقامة', href: '/ar/accommodation/' },
    ],
  },
  {
    label: 'التحميلات', href: '/ar/brochure/', children: [
      { label: 'الكتيّب', href: '/ar/brochure/' },
      { label: 'تقرير ما بعد المعرض', href: '/ar/post-show-report/' },
    ],
  },
  {
    label: 'المركز الإعلامي', href: '/ar/media-partners/', children: [
      { label: 'الشركاء الإعلاميون', href: '/ar/media-partners/' },
      { label: 'معرض الصور', href: '/ar/gallery/' },
    ],
  },
  { label: 'كن شريكاً', href: '/ar/partner/' },
  { label: 'اتصل بنا', href: '/ar/contact/' },
];

export const cta = {
  en: { stand: 'Book a Stand', visit: 'Register to Visit' },
  ar: { stand: 'احجز جناحك', visit: 'تسجيل الزوار' },
};

// Prefix a slug with the locale. One place, so no page invents its own URL shape.
export const url = (lang, slug = '') =>
  lang === 'ar' ? `/ar/${slug}`.replace(/\/+$/, '/') : `/${slug}`.replace(/\/+$/, '/');
