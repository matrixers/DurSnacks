const express = require('express');

const app = express();

// Lets the server read JSON request bodies (populates req.body)
app.use(express.json());

// Quick check that the server is up: open http://localhost:8090/ in a browser
app.get('/', (req, res) => {
    res.json({ status: 'ok' });
});

// The Python backend (python -m Backend.server) that finds the passages
const PYTHON_BACKEND = process.env.PYTHON_BACKEND || 'http://127.0.0.1:8000';

// The endpoint the Kivy app calls
// Request:  { "core": "Sad", "secondary": "Lonely", "deeper": "Isolated",
//             "what": "...", "why": "...", "who": "..." }       (what / why / who optional)
// Response: { "sentiment": { emotion, name, deeper },    (same keys as Backend/backend_JSON.JSON)
//             "picture": { imageURL, title, artist, year, link },
//             "quotes":[{ quote, name, years }, ...],   (one per quote box, 3)
//             "no_match": false, "message": "all quotes as one text", "poem": "...", "results": [...] }
//           (passed on unchanged from the Python backend; example in Backend/example_output.json)
app.post('/guidance', async (req, res) => {
    const { core, secondary, deeper, what = '', why = '', who = '' } = req.body || {};

    if (!core || !secondary || !deeper) {
        return res
            .status(400)
            .json({ error: 'core, secondary and deeper are required' });
    }

    // Pass the request on to the Python backend and send its answer back to the app
    try {
        const reply = await fetch(`${PYTHON_BACKEND}/guidance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ core, secondary, deeper, what, why, who }),
            signal: AbortSignal.timeout(110000), // a search takes about 30 seconds
        });
        res.status(reply.status).json(await reply.json());
    } catch (err) {
        console.error('Python backend did not answer:', err.message);
        res.status(502).json({ error: 'The Python backend is not running (python -m Backend.server)' });
    }
});

// Malformed JSON and other errors come back as JSON, not an HTML page
app.use((err, req, res, next) => {
    console.error(err);
    res.status(err.status || 500).json({ error: err.message || 'Server error' });
});

module.exports = app;