// Vercel serverless function — same handler, different request shape.
import { handleSubmission } from '../shared/submit.js';

export default async function (req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'method' });
  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const { status, json } = await handleSubmission(body, process.env);
    res.status(status).json(json);
  } catch {
    res.status(400).json({ ok: false, error: 'bad_request' });
  }
}
