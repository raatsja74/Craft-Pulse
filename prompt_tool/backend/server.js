const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Path to the prompt history file
const DATA_FILE = path.join(__dirname, 'data', 'prompts.json');

/**
 * Read prompts from the JSON file. If the file is missing or invalid,
 * return an empty array instead of throwing an error.
 */
function readPrompts() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch (err) {
    return [];
  }
}

/**
 * Persist prompts back to the JSON file.
 * @param {Array} prompts - Array of prompt objects to persist
 */
function writePrompts(prompts) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(prompts, null, 2));
}

/**
 * Generate an optimized prompt.
 * This is a placeholder that simply annotates the prompt with the
 * requested mode and style. Real implementations could call an AI model
 * to enrich the prompt further.
 */
app.post('/api/generate', (req, res) => {
  const { basePrompt, mode, style } = req.body;
  const optimizedPrompt = `[${mode}] [${style}] ${basePrompt}`;
  res.json({ optimizedPrompt });
});

/**
 * Compare a prompt across multiple models. For the purposes of this
 * demo, we simply echo back stubbed responses. In a production setup,
 * each model would be queried using its respective SDK.
 */
app.post('/api/compare', async (req, res) => {
  const { prompt, models = [] } = req.body;
  const results = {};
  models.forEach((model) => {
    results[model] = `Stub response from ${model} for prompt: ${prompt}`;
  });
  res.json({ results });
});

// Fetch saved prompts
app.get('/api/prompts', (req, res) => {
  res.json(readPrompts());
});

// Save a new prompt to history
app.post('/api/prompts', (req, res) => {
  const { text, tags = [] } = req.body;
  const prompts = readPrompts();
  const entry = {
    id: Date.now(),
    text,
    tags,
    timestamp: new Date().toISOString(),
  };
  prompts.push(entry);
  writePrompts(prompts);
  res.status(201).json(entry);
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
