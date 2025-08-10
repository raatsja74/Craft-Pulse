const starterPrompts = [
  'Draft a pitch deck for {product} targeting {audience}',
  'Create a business model canvas for {company}',
  'Identify potential investors for {sector} in {region}',
  'Outline a lean startup plan for {idea}',
  'Analyze the market for {product} in {region}',
  'Generate company name ideas for {theme}',
  'Write a mission statement that {goal}',
  'Brainstorm revenue streams for {business}',
  'Draft an elevator pitch for {idea}'
];

const modes = [
  { value: 'text', label: 'Text' },
  { value: 'code', label: 'Code' },
  { value: 'structuredData', label: 'Structured Data' },
  { value: 'creativeWriting', label: 'Creative Writing' },
  { value: 'marketingCopy', label: 'Marketing Copy' }
];

const styles = [
  { value: 'primer', label: 'Primer' },
  { value: 'reasoningSummary', label: 'Reasoning Summary' },
  { value: 'marketingHook', label: 'Marketing Hook' },
  { value: 'socraticQA', label: 'Socratic Q&A' }
];

const models = [
  { provider: 'openai', modelId: 'gpt-5', label: 'GPT-5' },
  { provider: 'anthropic', modelId: 'claude-latest', label: 'Claude' },
  { provider: 'google', modelId: 'gemini-1.5-pro', label: 'Gemini' }
];

function GenerateTab() {
  const [basePrompt, setBasePrompt] = React.useState('');
  const [mode, setMode] = React.useState(modes[0].value);
  const [style, setStyle] = React.useState(styles[0].value);
  const [optimized, setOptimized] = React.useState('');

  const generate = async () => {
    const resp = await fetch('http://localhost:3001/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ basePrompt, mode, style })
    });
    const data = await resp.json();
    setOptimized(data.optimizedPrompt);
  };

  const savePrompt = async () => {
    await fetch('http://localhost:3001/api/prompts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: optimized, tags: [mode, style] })
    });
    alert('Prompt saved');
  };

  return (
    <div className="container">
      <div className="chips">
        {starterPrompts.map((p) => (
          <span key={p} className="chip" onClick={() => setBasePrompt(p)}>{p}</span>
        ))}
      </div>
      <textarea value={basePrompt} onChange={e => setBasePrompt(e.target.value)} placeholder="Enter your base prompt" />
      <div>
        <select value={mode} onChange={e => setMode(e.target.value)}>
          {modes.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}
        </select>
        <select value={style} onChange={e => setStyle(e.target.value)}>
          {styles.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
        </select>
        <button onClick={generate}>Generate Prompt</button>
      </div>
      {optimized && (
        <div>
          <h3>Optimized Prompt</h3>
          <textarea value={optimized} readOnly></textarea>
          <button onClick={savePrompt}>Save Prompt</button>
        </div>
      )}
    </div>
  );
}

function CompareTab() {
  const [prompt, setPrompt] = React.useState('');
  const [selectedModels, setSelectedModels] = React.useState([]);
  const [results, setResults] = React.useState({});

  const toggleModel = (modelId) => {
    setSelectedModels((prev) =>
      prev.includes(modelId) ? prev.filter(m => m !== modelId) : [...prev, modelId]
    );
  };

  const compare = async () => {
    const resp = await fetch('http://localhost:3001/api/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, models: selectedModels })
    });
    const data = await resp.json();
    setResults(data.results);
  };

  return (
    <div className="container">
      <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Enter prompt to compare" />
      <div>
        {models.map(m => (
          <label key={m.modelId} style={{marginRight:'1rem'}}>
            <input type="checkbox" checked={selectedModels.includes(m.modelId)} onChange={() => toggleModel(m.modelId)} /> {m.label}
          </label>
        ))}
        <button onClick={compare}>Compare Models</button>
      </div>
      <div className="outputs">
        {Object.entries(results).map(([modelId, text]) => {
          const model = models.find(m => m.modelId === modelId);
          return (
            <div key={modelId} className="output">
              <h4>{model ? model.label : modelId}</h4>
              <p>{text}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function App() {
  const [tab, setTab] = React.useState('generate');
  return (
    <div>
      <div className="tabs">
        <div className={`tab ${tab === 'generate' ? 'active' : ''}`} onClick={() => setTab('generate')}>Generate</div>
        <div className={`tab ${tab === 'compare' ? 'active' : ''}`} onClick={() => setTab('compare')}>Compare Models</div>
      </div>
      {tab === 'generate' ? <GenerateTab /> : <CompareTab />}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
