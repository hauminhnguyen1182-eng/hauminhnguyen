export default {
    async fetch(request, env) {
        if (request.method === 'OPTIONS') {
            return new Response(null, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            });
        }

        if (request.method === 'POST') {
            const { text, lang = 'en' } = await request.json();

            const models = {
                'en': '@cf/meta/m2m100-1.8b',
                'vi': '@cf/meta/m2m100-1.8b'
            };

            const model = models[lang] || models['en'];

            const aiResponse = await env.AI.run(model, { text });

            return new Response(aiResponse, {
                headers: {
                    'Content-Type': 'audio/mpeg',
                    'Access-Control-Allow-Origin': '*'
                }
            });
        }

        return new Response('Use POST with { text, lang }', { status: 400 });
    }
};