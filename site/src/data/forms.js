// Form definitions, both languages, in one place — same idea as site.js.
// A field is described once and rendered by Form.astro.
//
// Saudi Arabia's PDPL requires explicit consent before collecting personal data, so every
// form ends with a required consent checkbox linking to the privacy notice. That is not
// optional politeness — SDAIA has been enforcing since September 2024.

const countries = [
  'Saudi Arabia', 'Egypt', 'United Arab Emirates', 'Kuwait', 'Qatar', 'Bahrain', 'Oman',
  'Jordan', 'Lebanon', 'Iraq', 'Turkey', 'India', 'China', 'Germany', 'Italy', 'Spain',
  'United Kingdom', 'United States', 'Other',
];

const countriesAr = [
  'المملكة العربية السعودية', 'مصر', 'الإمارات العربية المتحدة', 'الكويت', 'قطر',
  'البحرين', 'عُمان', 'الأردن', 'لبنان', 'العراق', 'تركيا', 'الهند', 'الصين', 'ألمانيا',
  'إيطاليا', 'إسبانيا', 'المملكة المتحدة', 'الولايات المتحدة', 'أخرى',
];

const sectors = {
  en: ['Printing', 'Packaging', 'Paper and tissue', 'Plastics', 'Food and beverage',
       'Converting and finishing', 'Inks and materials', 'Machinery', 'Other'],
  ar: ['الطباعة', 'التغليف', 'الورق والمناديل', 'البلاستيك', 'الأغذية والمشروبات',
       'التحويل والتشطيب', 'الأحبار والمواد', 'الماكينات', 'أخرى'],
};

export const forms = {
  register: {
    endpoint: '/api/register',
    en: {
      intro: 'Registration is free. Fill this in and your badge will be waiting at the door.',
      submit: 'Complete registration',
      sending: 'Sending…',
      successTitle: 'You are registered',
      successBody: 'A confirmation is on its way to your email. Bring it, or just your name, to the registration desk.',
      errorTitle: 'That did not send',
      errorBody: 'Something went wrong at our end. Please email ksa@nilefairs.com and we will register you by hand.',
      fields: [
        { name: 'name',    label: 'Full name',      type: 'text',   required: true,  autocomplete: 'name' },
        { name: 'company', label: 'Company',        type: 'text',   required: true,  autocomplete: 'organization' },
        { name: 'role',    label: 'Job title',      type: 'text',   autocomplete: 'organization-title' },
        { name: 'email',   label: 'Email',          type: 'email',  required: true,  autocomplete: 'email' },
        { name: 'phone',   label: 'Phone',          type: 'tel',    required: true,  autocomplete: 'tel', hint: 'Include the country code' },
        { name: 'country', label: 'Country',        type: 'select', required: true,  options: countries, autocomplete: 'country-name' },
        { name: 'sector',  label: 'Your sector',    type: 'select', required: true,  options: sectors.en },
      ],
    },
    ar: {
      intro: 'التسجيل مجاني. أكمل البيانات وستجد بطاقتك في انتظارك عند المدخل.',
      submit: 'إتمام التسجيل',
      sending: 'جارٍ الإرسال…',
      successTitle: 'تم تسجيلك',
      successBody: 'سيصلك تأكيد على بريدك الإلكتروني. أحضره معك، أو اذكر اسمك عند مكتب التسجيل.',
      errorTitle: 'لم يتم الإرسال',
      errorBody: 'حدث خطأ لدينا. يرجى مراسلتنا على ksa@nilefairs.com وسنقوم بتسجيلك يدوياً.',
      fields: [
        { name: 'name',    label: 'الاسم الكامل',   type: 'text',   required: true,  autocomplete: 'name' },
        { name: 'company', label: 'الشركة',          type: 'text',   required: true,  autocomplete: 'organization' },
        { name: 'role',    label: 'المسمّى الوظيفي', type: 'text',   autocomplete: 'organization-title' },
        { name: 'email',   label: 'البريد الإلكتروني', type: 'email', required: true, autocomplete: 'email' },
        { name: 'phone',   label: 'رقم الهاتف',      type: 'tel',    required: true,  autocomplete: 'tel', hint: 'مع رمز الدولة' },
        { name: 'country', label: 'الدولة',          type: 'select', required: true,  options: countriesAr, autocomplete: 'country-name' },
        { name: 'sector',  label: 'مجال عملك',       type: 'select', required: true,  options: sectors.ar },
      ],
    },
  },

  stand: {
    endpoint: '/api/stand',
    en: {
      intro: 'Tell us what you need and the team will come back to you with availability and a quote.',
      submit: 'Request a stand',
      sending: 'Sending…',
      successTitle: 'Request received',
      successBody: 'The team will contact you within two working days with availability and pricing.',
      errorTitle: 'That did not send',
      errorBody: 'Something went wrong at our end. Please email ksa@nilefairs.com directly and we will pick it up from there.',
      fields: [
        { name: 'company',  label: 'Company name',       type: 'text',   required: true, autocomplete: 'organization' },
        { name: 'name',     label: 'Contact person',     type: 'text',   required: true, autocomplete: 'name' },
        { name: 'role',     label: 'Position',           type: 'text',   autocomplete: 'organization-title' },
        { name: 'email',    label: 'Email',              type: 'email',  required: true, autocomplete: 'email' },
        { name: 'phone',    label: 'Phone',              type: 'tel',    required: true, autocomplete: 'tel', hint: 'Include the country code' },
        { name: 'country',  label: 'Country',            type: 'select', required: true, options: countries, autocomplete: 'country-name' },
        { name: 'website',  label: 'Website',            type: 'url',    autocomplete: 'url' },
        { name: 'sector',   label: 'What you exhibit',   type: 'select', required: true, options: sectors.en },
        { name: 'size',     label: 'Stand size',         type: 'select', required: true,
          options: ['9 m² (3×3)', '12 m² (4×3)', '18 m² (6×3)', '24 m² (6×4)', '36 m² (6×6)', 'Larger — tell us below'] },
        { name: 'scheme',   label: 'Stand type',         type: 'select', required: true,
          options: ['Shell scheme — built for me', 'Space only — I will build'] },
        { name: 'message',  label: 'Anything else',      type: 'textarea', rows: 4 },
      ],
    },
    ar: {
      intro: 'أخبرنا باحتياجاتك وسيتواصل معك الفريق بالتوافر والتسعير.',
      submit: 'اطلب جناحاً',
      sending: 'جارٍ الإرسال…',
      successTitle: 'تم استلام طلبك',
      successBody: 'سيتواصل معك الفريق خلال يومي عمل بالتوافر والأسعار.',
      errorTitle: 'لم يتم الإرسال',
      errorBody: 'حدث خطأ لدينا. يرجى مراسلتنا مباشرة على ksa@nilefairs.com.',
      fields: [
        { name: 'company',  label: 'اسم الشركة',       type: 'text',   required: true, autocomplete: 'organization' },
        { name: 'name',     label: 'الشخص المسؤول',    type: 'text',   required: true, autocomplete: 'name' },
        { name: 'role',     label: 'المنصب',            type: 'text',   autocomplete: 'organization-title' },
        { name: 'email',    label: 'البريد الإلكتروني', type: 'email',  required: true, autocomplete: 'email' },
        { name: 'phone',    label: 'رقم الهاتف',        type: 'tel',    required: true, autocomplete: 'tel', hint: 'مع رمز الدولة' },
        { name: 'country',  label: 'الدولة',            type: 'select', required: true, options: countriesAr, autocomplete: 'country-name' },
        { name: 'website',  label: 'الموقع الإلكتروني', type: 'url',    autocomplete: 'url' },
        { name: 'sector',   label: 'ما الذي تعرضه',     type: 'select', required: true, options: sectors.ar },
        { name: 'size',     label: 'مساحة الجناح',      type: 'select', required: true,
          options: ['٩ م² (٣×٣)', '١٢ م² (٤×٣)', '١٨ م² (٦×٣)', '٢٤ م² (٦×٤)', '٣٦ م² (٦×٦)', 'أكبر — اذكرها أدناه'] },
        { name: 'scheme',   label: 'نوع الجناح',        type: 'select', required: true,
          options: ['جناح مجهّز', 'مساحة فقط — سأقوم بالتجهيز'] },
        { name: 'message',  label: 'ملاحظات إضافية',    type: 'textarea', rows: 4 },
      ],
    },
  },
};

export const consent = {
  en: {
    label: 'I agree that Nile Trade Fairs may store these details and contact me about PRINT2PACK.',
    link: 'How we handle your data',
    required: 'Please tick this to continue.',
  },
  ar: {
    label: 'أوافق على احتفاظ نايل تريد فيرز ببياناتي والتواصل معي بخصوص معرض برينت تو باك.',
    link: 'كيف نتعامل مع بياناتك',
    required: 'يرجى الموافقة للمتابعة.',
  },
};

export const validation = {
  en: { required: 'This is needed.', email: 'That does not look like an email address.',
        phone: 'Please include the country code.', url: 'That does not look like a web address.' },
  ar: { required: 'هذا الحقل مطلوب.', email: 'البريد الإلكتروني غير صحيح.',
        phone: 'يرجى إضافة رمز الدولة.', url: 'الرابط غير صحيح.' },
};
