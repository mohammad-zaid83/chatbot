import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { CohereClientV2 } from 'cohere-ai';

const app = express();
const cohere = new CohereClientV2({ token: process.env.COHERE_API_KEY });

app.use(express.json());
app.use(
  cors({
    origin: [process.env.FRONTEND_ORIGIN, 'http://localhost:3000', 'http://localhost:5173'],
    methods: ['POST'],
  })
);

// POST /chat  -> { message: "user text", history?: [{role, content}...] }
app.post('/chat', async (req, res) => {
  const { message, history = [] } = req.body || {};
  if (!message || typeof message !== 'string') {
    return res.status(400).json({ error: 'message (string) required' });
  }

  try {
    const resp = await cohere.chat({
      model: 'command-a-03-2025',   // recent chat model
      messages: [
        { role: 'system', content: 'Respond briefly and helpfully.' },
        ...history,                  // optional chat history from frontend
        { role: 'user', content: message }
      ],
    });

    const text = resp?.message?.content?.[0]?.text ?? '';
    return res.json({ reply: text });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: 'cohere_error', detail: e?.message });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`API running on :${PORT}`));
