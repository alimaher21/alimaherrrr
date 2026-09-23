// Homepage content, both languages. Figures are taken from the current site's own pages
// (fact sheet and marketing campaign) — not invented.
// TODO: ask the client to confirm the visitor and VIP ticket figures before launch.

// heroPhoto: drop in a path like '/img/hero.webp' once the client supplies event
// photography and it fades in behind the hero. There is no usable photograph anywhere
// on their current site — the largest image is a partner's logo.
export const home = {
  en: {
    heroPhoto: '/img/d6bd877a-1af8-4c65-84d5-8e08141db0d3.jpg',
    eyebrow: '16–18 November 2026 · Jeddah Center for Exhibitions and Events',
    h1: 'Print 2 Pack 2026',
    h1sub: 'Jeddah, Saudi Arabia',
    lede: 'The inaugural trade fair for the paper, printing, packaging and plastic industries in the Kingdom — bringing the world’s leading technology makers to Jeddah.',
    countdownLabels: { days: 'Days', hours: 'Hours', minutes: 'Min', seconds: 'Sec' },
    facts: [
      { n: '3', label: 'Days' },
      { n: '8,000', label: 'Square metres' },
      { n: '30,000', label: 'Visitor tickets' },
      { n: '10,000', label: 'VIP tickets' },
    ],
    aboutTitle: 'The first of its kind in the Kingdom',
    about: [
      'We are excited to introduce the first-ever PRINT 2 PACK event in Saudi Arabia, showcasing the latest technologies and innovations in the printing, packaging and plastics industry.',
      'It aims to meet the growing industrial needs of Saudi Arabia and the entire GCC region, and is designed for entrepreneurs, service providers, buyers and trade visitors from the Kingdom and around the world.',
    ],
    aboutLink: { label: 'More about the show', href: '/about/' },
    sectorsTitle: 'What is on show',
    sectors: [
      { t: 'Printing', d: 'Sheetfed and web systems, inkjet, print origination, plates and plate making.' },
      { t: 'Finishing', d: 'Print finishing and binding equipment, converting and post-press.' },
      { t: 'Packaging', d: 'Packaging machinery, materials and design for every sector.' },
      { t: 'Paper & Tissue', d: 'Paper, paperboard, tissue and hygienic products.' },
      { t: 'Plastics', d: 'Plastics processing, films and flexible packaging.' },
      { t: 'Materials', d: 'Inks, coatings, substrates and consumables.' },
    ],
    visitorsTitle: 'Who comes to buy',
    visitors: [
      'Food and beverage manufacturers',
      'Food processing and frozen food',
      'Bakers and confectioners',
      'Fruit and vegetable plants',
      'Pasta manufacturers',
      'Retailers and distributors',
    ],
    ctaTitle: 'Take part in the first edition',
    ctaText: 'Stand space is booking now for November 2026.',
  },

  ar: {
    heroPhoto: '/img/d6bd877a-1af8-4c65-84d5-8e08141db0d3.jpg',
    eyebrow: '١٦–١٨ نوفمبر ٢٠٢٦ · مركز جدة للمعارض والفعاليات',
    h1: 'برينت تو باك ٢٠٢٦',
    h1sub: 'جدة، المملكة العربية السعودية',
    lede: 'أول معرض تجاري متخصص في صناعات الورق والطباعة والتغليف والبلاستيك في المملكة، يجمع أبرز صنّاع التقنية في العالم في مدينة جدة.',
    countdownLabels: { days: 'يوم', hours: 'ساعة', minutes: 'دقيقة', seconds: 'ثانية' },
    facts: [
      { n: '٣', label: 'أيام' },
      { n: '٨٬٠٠٠', label: 'متر مربع' },
      { n: '٣٠٬٠٠٠', label: 'تذكرة زائر' },
      { n: '١٠٬٠٠٠', label: 'تذكرة كبار الزوار' },
    ],
    aboutTitle: 'الأول من نوعه في المملكة',
    about: [
      'يسعدنا أن نقدّم النسخة الأولى من معرض برينت تو باك في المملكة العربية السعودية، الذي يعرض أحدث التقنيات والابتكارات في صناعات الطباعة والتغليف والبلاستيك.',
      'يهدف المعرض إلى تلبية الاحتياجات الصناعية المتنامية في المملكة ومنطقة الخليج، وهو موجّه لرواد الأعمال ومزوّدي الخدمات والمشترين وزوار التجارة من المملكة ومن مختلف أنحاء العالم.',
    ],
    aboutLink: { label: 'المزيد عن المعرض', href: '/ar/about/' },
    sectorsTitle: 'ماذا يُعرض',
    sectors: [
      { t: 'الطباعة', d: 'أنظمة الطباعة الورقية واللفّية، الطباعة النفاثة، تجهيز الطباعة والألواح.' },
      { t: 'التشطيب', d: 'معدات التشطيب والتجليد والتحويل وما بعد الطباعة.' },
      { t: 'التغليف', d: 'ماكينات ومواد وتصاميم التغليف لمختلف القطاعات.' },
      { t: 'الورق والمناديل', d: 'الورق والكرتون والمناديل والمنتجات الصحية.' },
      { t: 'البلاستيك', d: 'معالجة البلاستيك والأغشية والتغليف المرن.' },
      { t: 'المواد', d: 'الأحبار والطلاءات والخامات والمستهلكات.' },
    ],
    visitorsTitle: 'من يأتي للشراء',
    visitors: [
      'مصنّعو الأغذية والمشروبات',
      'تصنيع الأغذية والأغذية المجمّدة',
      'المخابز والحلويات',
      'مصانع الفواكه والخضروات',
      'مصنّعو المعكرونة',
      'تجار التجزئة والموزّعون',
    ],
    ctaTitle: 'شارك في النسخة الأولى',
    ctaText: 'حجز الأجنحة مفتوح الآن لدورة نوفمبر ٢٠٢٦.',
  },
};
