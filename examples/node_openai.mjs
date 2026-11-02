// Stream one roleplay reply from TavernAPI with the official OpenAI Node SDK.
//
//   npm install openai
//   export TAVERNAPI_API_KEY=sk-tav-...        # PowerShell: $env:TAVERNAPI_API_KEY="sk-tav-..."
//   node node_openai.mjs
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://tavernapi.com/v1',
  apiKey: process.env.TAVERNAPI_API_KEY,
});

const stream = await client.chat.completions.create({
  model: 'gemini-4-argon',
  messages: [
    { role: 'system', content: 'You are Mira, a sharp-tongued tavern keeper. Stay in character.' },
    { role: 'user', content: 'A stranger walks in out of the rain and asks for a room.' },
  ],
  max_tokens: 400,
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
}
process.stdout.write('\n');
