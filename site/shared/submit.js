// Shared submission handler. Runs unchanged on Cloudflare Pages Functions and on Vercel —
// the two wrappers in functions/api/ and api/ only translate the platform's request shape.
//
// Never trust the browser: everything the client checks is checked again here.

const REQUIRED = {
  register: ['name', 'company', 'email', 'phone', 'country', 'sector'],
  stand: ['company', 'name', 'email', 'phone', 'country', 'sector', 'size', 'scheme'],
};

const LABELS = {
  register: 'Visitor registration',
  stand: 'Stand booking request',
};

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const esc = (s) =>
  String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export async function handleSubmission(body, env) {
  const kind = body.form === 'stand' ? 'stand' : 'register';
  const lang = body.lang === 'ar' ? 'ar' : 'en';

  // Honeypot — a real person never sees this field.
  if (body.website2) {
    return { status: 200, json: { ok: true } };   // look successful; drop it silently
  }

  if (!body.consent) {
    return { status: 400, json: { ok: false, error: 'consent_required' } };
  }

  const missing = REQUIRED[kind].filter((f) => !String(body[f] ?? '').trim());
  if (missing.length) {
    return { status: 400, json: { ok: false, error: 'missing_fields', fields: missing } };
  }
  if (!EMAIL.test(String(body.email).trim())) {
    return { status: 400, json: { ok: false, error: 'bad_email' } };
  }

  const to = env.NOTIFY_EMAIL || 'ksa@nilefairs.com';
  const from = env.FROM_EMAIL;
  const key = env.RESEND_API_KEY;

  // No delivery configured: refuse loudly rather than swallow someone's registration.
  if (!key || !from) {
    return { status: 503, json: { ok: false, error: 'delivery_not_configured' } };
  }

  const rows = Object.entries(body)
    .filter(([k]) => !['website2', 'form', 'consent', 'lang'].includes(k))
    .filter(([, v]) => String(v ?? '').trim())
    .map(([k, v]) => `<tr><th align="left" style="padding:4px 14px 4px 0;color:#5C53C4">${esc(k)}</th><td>${esc(v)}</td></tr>`)
    .join('');

  const send = (payload) =>
    fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

  const notify = await send({
    from,
    to: [to],
    reply_to: String(body.email).trim(),
    subject: `${LABELS[kind]} — ${body.company || body.name}`,
    html: `<h2 style="font-family:sans-serif;color:#241E70">${LABELS[kind]}</h2>
           <table style="font-family:sans-serif;font-size:14px">${rows}</table>`,
  });

  if (!notify.ok) {
    return { status: 502, json: { ok: false, error: 'delivery_failed' } };
  }

  // Confirmation to the person. A failure here must not fail their registration.
  const confirm = lang === 'ar'
    ? { subject: 'تأكيد — برينت تو باك ٢٠٢٦',
        html: `<p style="font-family:sans-serif">شكراً لك. استلمنا بياناتك لمعرض برينت تو باك ٢٠٢٦، جدة، ١٦–١٨ نوفمبر ٢٠٢٦.</p>` }
    : { subject: 'Confirmation — PRINT2PACK 2026',
        html: `<p style="font-family:sans-serif">Thank you. We have your details for PRINT2PACK 2026, Jeddah, 16–18 November 2026.</p>` };

  try {
    await send({ from, to: [String(body.email).trim()], ...confirm });
  } catch { /* the organiser already has it — that is what matters */ }

  return { status: 200, json: { ok: true } };
}

export async function readBody(request) {
  const type = request.headers.get('content-type') || '';
  if (type.includes('application/json')) return await request.json();
  const form = await request.formData();
  return Object.fromEntries(form);
}
