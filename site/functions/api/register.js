// Cloudflare Pages Function. Env vars are set in the Pages dashboard.
import { handleSubmission, readBody } from '../../shared/submit.js';

export async function onRequestPost({ request, env }) {
  try {
    const body = await readBody(request);
    const { status, json } = await handleSubmission(body, env);
    return new Response(JSON.stringify(json), {
      status,
      headers: { 'content-type': 'application/json' },
    });
  } catch {
    return new Response(JSON.stringify({ ok: false, error: 'bad_request' }), {
      status: 400,
      headers: { 'content-type': 'application/json' },
    });
  }
}
