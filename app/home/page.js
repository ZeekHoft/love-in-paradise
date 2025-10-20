'use client';

import { useState, useEffect } from 'react';

export default function FactCheckerPage() {
  const [claim, setClaim] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentProcess, setCurrentProcess] = useState('');
  const [result, setResult] = useState(null);
  const [justificationBuffer, setJustificationBuffer] = useState('');
  const [error, setError] = useState(null);
  const [useLLM, setUseLLM] = useState(false);

  const checkFact = async (claimText) => {
    // Reset state
    setLoading(true);
    setProgress(0);
    setCurrentProcess('');
    setResult(null);
    setJustificationBuffer('');
    setError(null);

    try {
      const response = await fetch('/api/home', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/x-ndjson',
        },
        body: JSON.stringify({ name: claimText, useLLM })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          // Process any remaining data
          if (buffer.trim()) {
            try {
              const parsed = JSON.parse(buffer);
              handleLine(parsed);
            } catch (e) {
              console.error('Final parse error:', e);
            }
          }
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const parsed = JSON.parse(line);
            handleLine(parsed);
          } catch (e) {
            console.error('Parse error:', e, line);
          }
        }
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err.message || 'An error occurred while checking the fact');
    } finally {
      setLoading(false);
    }
  };

  const handleLine = (data) => {
    // Update progress
    if (data.progress !== undefined) setProgress(data.progress);

    // Update current process
    if (data.currentProcess) setCurrentProcess(data.currentProcess);

    // Accumulate justification
    if (data.justification) {
      setJustificationBuffer(prev => prev + data.justification + '\n');
    }

    // Merge sources and headlines incrementally
    setResult(prev => ({
      ...prev,
      ...data,
      justification: justificationBuffer + (data.justification || ''),
      sources: [...(prev?.sources || []), ...(data.sources || [])],
      headlines: { ...(prev?.headlines || {}), ...(data.headlines || {}) },
    }));

    // Handle errors
    if (data.currentProcess === 'Error') {
      setError(data.justification || 'An error occurred');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (claim.trim()) checkFact(claim);
  };

  const handleTryAgain = () => {
    setClaim('');
    setLoading(false);
    setProgress(0);
    setCurrentProcess('');
    setResult(null);
    setJustificationBuffer('');
    setError(null);
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Fact Checker</h1>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-2 items-center">
          <input
            type="text"
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim to fact-check..."
            className="flex-1 px-4 py-2 border rounded"
            disabled={loading}
          />

          {/* LLM Toggle */}
          <div className="flex items-center gap-2">
            <span className="text-gray-700 text-sm">Use LLM</span>
            <button
              type="button"
              onClick={() => setUseLLM(!useLLM)}
              className={`w-12 h-6 flex items-center rounded-full p-1 transition ${useLLM ? 'bg-green-500' : 'bg-gray-300'}`}
            >
              <div className={`bg-white w-4 h-4 rounded-full transform transition ${useLLM ? 'translate-x-6' : ''}`} />
            </button>
          </div>

          <button
            type="submit"
            disabled={loading || !claim.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
          >
            {loading ? 'Checking...' : 'Check'}
          </button>
        </div>
      </form>

      {/* Progress Bar */}
      {loading && (
        <div className="mb-6">
          <div className="mb-2 text-sm text-gray-600">{currentProcess || 'Processing...'}</div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${(progress * 100).toFixed(0)}%` }}
            />
          </div>
          <div className="mt-1 text-xs text-gray-500">{(progress * 100).toFixed(0)}%</div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          {result.verdict && (
            <div className="mb-4">
              <h2 className="text-xl font-semibold mb-2">Verdict</h2>
              <span className={`inline-block px-4 py-2 rounded-full text-white font-semibold ${
                result.verdict === 'TRUE' ? 'bg-green-600' :
                result.verdict === 'FALSE' ? 'bg-red-600' :
                result.verdict === 'LIKELY TRUE' ? 'bg-green-400' :
                result.verdict === 'LIKELY FALSE' ? 'bg-red-400' :
                'bg-gray-500'
              }`}>
                {result.verdict}
              </span>
            </div>
          )}

          {result.confidence !== undefined && (
            <div className="mb-4">
              <h3 className="text-lg font-semibold mb-1">Confidence</h3>
              <p className="text-gray-700">{result.confidence.toFixed(1)}%</p>
            </div>
          )}

          {justificationBuffer && (
            <div className="mb-4">
              <h3 className="text-lg font-semibold mb-2">Justification</h3>
              <pre className="text-gray-700 whitespace-pre-wrap">{justificationBuffer}</pre>
            </div>
          )}

          {result.sources && result.sources.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Sources</h3>
              <ul className="space-y-2">
                {result.sources.map((url, index) => (
                  <li key={index}>
                    <a
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {result.headlines?.[url] || url}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {result && (
        <button
          onClick={handleTryAgain}
          className="px-6 py-2 bg-gray-700 text-white rounded hover:bg-gray-800 transition"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
