'use client';

import { useState } from 'react';

export default function FactCheckerPage() {
  const [claim, setClaim] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentProcess, setCurrentProcess] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function checkFact(claimText, useLLM = false) {
    // Reset state
    setLoading(true);
    setProgress(0);
    setCurrentProcess('');
    setResult(null);
    setError(null);

    try {
      const response = await fetch('/api/home', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/x-ndjson'
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
          // Process any remaining data in buffer
          if (buffer.trim()) {
            try {
              const parsed = JSON.parse(buffer);
              updateState(parsed);
            } catch (e) {
              console.error('Final parse error:', e);
              setError('Error parsing final response');
            }
          }
          break;
        }

        // Add new data to buffer
        buffer += decoder.decode(value, { stream: true });
        
        // Process complete lines
        const lines = buffer.split('\n');
        
        // Keep the last (possibly incomplete) line in the buffer
        buffer = lines.pop() || '';
        
        // Parse and handle each complete line
        for (const line of lines) {
          if (line.trim()) {
            try {
              const parsed = JSON.parse(line);
              console.log('Progress:', parsed);
              updateState(parsed);
            } catch (e) {
              console.error('Parse error:', e, 'Line:', line);
              setError('Error parsing response');
            }
          }
        }
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err.message || 'An error occurred while checking the fact');
    } finally {
      setLoading(false);
    }
  }

  function updateState(data) {
    // Update progress
    if (data.progress !== undefined) {
      setProgress(data.progress);
    }
    
    // Update current process
    if (data.currentProcess) {
      setCurrentProcess(data.currentProcess);
    }
    
    // If complete or error, set the full result
    if (data.currentProcess === 'Complete' || data.currentProcess === 'Error') {
      setResult(data);
    }
    
    // Handle errors
    if (data.currentProcess === 'Error' && data.justification) {
      setError(data.justification);
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    if (claim.trim()) {
      checkFact(claim);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Fact Checker</h1>
      
      {/* Input Form */}
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-2">
          <input
            type="text"
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim to fact-check..."
            className="flex-1 px-4 py-2 border rounded"
            disabled={loading}
          />
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
          <div className="mb-2 text-sm text-gray-600">
            {currentProcess || 'Processing...'}
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${(progress * 100).toFixed(0)}%` }}
            ></div>
          </div>
          <div className="mt-1 text-xs text-gray-500">
            {(progress * 100).toFixed(0)}%
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results Display */}
      {result && result.verdict && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-2">Verdict</h2>
            <div className={`inline-block px-4 py-2 rounded-full text-white font-semibold ${
              result.verdict === 'TRUE' ? 'bg-green-600' :
              result.verdict === 'FALSE' ? 'bg-red-600' :
              result.verdict === 'LIKELY TRUE' ? 'bg-green-400' :
              result.verdict === 'LIKELY FALSE' ? 'bg-red-400' :
              'bg-gray-500'
            }`}>
              {result.verdict}
            </div>
          </div>

          {result.confidence !== null && result.confidence !== undefined && (
            <div className="mb-4">
              <h3 className="text-lg font-semibold mb-1">Confidence</h3>
              <p className="text-gray-700">{result.confidence.toFixed(1)}%</p>
            </div>
          )}

          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Justification</h3>
            <p className="text-gray-700 whitespace-pre-line">{result.justification}</p>
          </div>

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
                      {result.headlines && result.headlines[url] 
                        ? result.headlines[url]
                        : url}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* No results message */}
      {result && !result.verdict && result.justification && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          <p className="text-gray-700">{result.justification}</p>
        </div>
      )}
    </div>
  );
}