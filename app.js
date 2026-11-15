const express = require('express');

const app = express();

// Lets the server read JSON request bodies (populates req.body)
app.use(express.json());

// Quick check that the server is up: open http://localhost:8090/ in a browser
app.get('/', (req, res) => {
    res.json({ status: 'ok' });
});

// The endpoint the Kivy app calls
// Request:  { "core": "Mad", "secondary": "Hurt", "deeper": "Distant" }
// Response: { "message": "text to show on the output screen" }
app.post('/guidance', (req, res) => {
    const { core, secondary, deeper } = req.body || {};

    if (!core || !secondary || !deeper) {
        return res
            .status(400)
            .json({ error: 'core, secondary and deeper are required' });
    }

    // TODO: replace with the real logic (database lookup, AI call, etc.)
    // Whatever happens, reply with JSON containing a "message" string.
    const message =
        `You're feeling ${secondary.toLowerCase()}, which sits under ` +
        `feeling ${core.toLowerCase()}. Deeper down it may be ` +
        `${deeper.toLowerCase()}.`;

    res.json({ message });
});

// Malformed JSON and other errors come back as JSON, not an HTML page
app.use((err, req, res, next) => {
    console.error(err);
    res.status(err.status || 500).json({ error: err.message || 'Server error' });
});

module.exports = app;