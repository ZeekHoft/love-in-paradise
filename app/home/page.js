'use client';
import React, { useEffect, useState } from 'react';

function Home() {
  // Same
  const [loading, setLoading] = useState(false);
  const [useLLM, setUseLLM] = useState(false);
  const [placeholder, setPlaceholder] = useState('');
  const [showVerdict, setShowVerdict] = useState(false);
  const [isVerdictTrue, setIsVerdictTrue] = useState(false);

  // Added
  const [claim, setClaim] = useState('');
  const [progress, setProgress] = useState(0);
  const [currentProcess, setCurrentProcess] = useState('');
  const [result, setResult] = useState(null);
  const [justificationBuffer, setJustificationBuffer] = useState('');
  const [error, setError] = useState(null);

  const rotatingPhrases = [
    'Government to distribute ₱10,000 cash aid to all residents next week, claims viral post.',
    'New law allegedly bans students from using cellphones inside classrooms starting next month.',
    'Post claims Cebu Pacific offering free domestic flights to celebrate anniversary.',
    'Viral TikTok video says NLEX toll fees will double by December.',
    'Rumor spreads that 13th month pay will be released early due to inflation.',
    "Facebook post claims NAIA will be renamed 'Manila International Spaceport' under new project.",
    'Circulating message warns of total lockdown due to rising dengue cases.',
    'Unverified post says public schools to switch to four-day class schedule permanently.',
    'Claim: Government to replace jeepneys with AI-driven buses by 2026.',
    'Message chain alleges that voting age will be lowered to 15 starting next elections.',
    "Fake memo says MRT operations will be suspended for three months for 'AI system upgrade.'",
    'Viral article claims electricity bills will be cut in half after new DOE policy.',
    'Tweet claims rice will be sold at ₱15 per kilo starting next week.',
    'Shared post alleges free internet for all barangays starting this month.',
    'Message circulating online says DOH confirmed new COVID-23 variant in Quezon City.',
  ];

  useEffect(() => {
    let phraseIndex = 0;
    let charIndex = 0;
    let currentPhrase = rotatingPhrases[phraseIndex];
    let typingForward = true;

    const typeSpeed = 30;
    const pauseTime = 2000;
    let timeoutId;

    // Typewriter Effect
    const type = () => {
      if (typingForward) {
        setPlaceholder(currentPhrase.slice(0, charIndex + 1));
        charIndex++;

        if (charIndex === currentPhrase.length) {
          typingForward = false;
          timeoutId = setTimeout(type, pauseTime);
          return;
        }
      } else {
        setPlaceholder(currentPhrase.slice(0, charIndex - 1));
        charIndex--;

        if (charIndex === 0) {
          typingForward = true;
          phraseIndex = (phraseIndex + 1) % rotatingPhrases.length;
          currentPhrase = rotatingPhrases[phraseIndex];
        }
      }
      timeoutId = setTimeout(type, typeSpeed);
    };

    type();

    return () => {
      clearTimeout(timeoutId);
    };
  }, []);

  const checkFact = (claimText) => {
    // Reset state
    setLoading(true);

    setProgress(0);
    setCurrentProcess('');
    setResult(null);
    setJustificationBuffer('');
    setError(null);

    async function readStream(url = '', data = {}) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/x-ndjson',
          },
          body: JSON.stringify(data),
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
            setShowVerdict(true);
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
          buffer = lines.pop() || ''; // save incomplete line for next chunk

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
        setResult({ justification: 'An error occurred. Please try again.' });
        setError(err.message || 'An error occurred while checking the fact');
      } finally {
        setLoading(false);
      }
    }

    readStream('http://localhost:8080/api/home', {
      name: claimText,
      useLLM: useLLM,
    });
  };

  const handleLine = (data) => {
    // Update progress
    if (data.progress !== undefined) setProgress(data.progress);

    // Update current process
    if (data.currentProcess) setCurrentProcess(data.currentProcess);

    // Accumulate justification
    if (data.justification) {
      setJustificationBuffer((prev) => prev + data.justification + '\n');
    }

    // Merge sources and headlines incrementally
    setResult((prev) => ({
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
    setShowVerdict(false);

    setClaim('');
    setLoading(false);
    setProgress(0);
    setCurrentProcess('');
    setResult(null);
    setJustificationBuffer('');
    setError(null);
  };

  return (
    <div className='min-h-screen flex flex-col items-center justify-center relative dotanim'>
      {loading && (
        <div className='flex flex-col items-center justify-center absolute inset-0 transition-opacity duration-500 opacity-100'>
          <div className='bigtext2 transition-all'>
            <p>{currentProcess ?? 'Processing'}</p>
          </div>
          {/* Progress Bar */}
          <div className='w-1/2 mb-24 bg-gray-700 rounded-full h-2.5'>
            <div
              className='dot h-2.5 rounded-full transition-all duration-300'
              style={{ width: `${(progress * 100).toFixed(0)}%` }}
            />
          </div>
          {/* <div className='mt-1 pb-24 text-xs text-gray-300'>
            {(progress * 100).toFixed(0)}%
          </div> */}
          <div className='inset-0 flex items-center justify-center bg-transparent z-10'>
            <div className='flex space-x-2'>
              <div className='w-4 h-4 rounded-full dot dot-animation dot-animation-1'></div>
              <div className='w-4 h-4 rounded-full dot dot-animation dot-animation-2'></div>
              <div className='w-4 h-4 rounded-full dot dot-animation dot-animation-3'></div>
            </div>
          </div>
        </div>
      )}

      {!showVerdict ? (
        <div
          className={`flex flex-col items-center w-full transition-opacity duration-500 ${
            loading ? 'opacity-0 pointer-events-none' : 'opacity-100'
          }`}
        >
          <div className='bigtext'>
            <p>Hello.</p>
          </div>

          <div className='bigtext2'>
            <p>You got news to check?</p>
          </div>

          {/* 👇 LLM Toggle */}
          <div className='flex items-center space-x-2 mt-4'>
            <label className='text-gray-300 text-sm'>Use LLM</label>
            <button
              onClick={() => setUseLLM(!useLLM)}
              className={`w-12 h-6 flex items-center rounded-full p-1 transition ${
                useLLM ? 'bg-green-500' : 'bg-gray-500'
              }`}
            >
              <div
                className={`bg-white w-4 h-4 rounded-full transform transition ${
                  useLLM ? 'translate-x-6' : ''
                }`}
              />
            </button>
          </div>

          <div className='relative w-full max-w-2xl'>
            <textarea
              className='w-full h-32 text-base p-3 pr-20 rounded-xl mt-3 resize focus:outline-none focus:ring-0 focus:border-gray-300'
              placeholder={placeholder}
              name='news'
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
            />

            {claim.trim() !== '' && (
              <button className='submit_btn' onClick={handleSubmit}>
                Submit
              </button>
            )}
          </div>

          <div className='disclaimer'>
            <p>
              Deception Detector may display inaccurate information. Please
              supplement the responses with your own due diligence.
            </p>
          </div>
        </div>
      ) : (
        <div className='flex flex-col items-center justify-center absolute inset-0 transition-opacity duration-500 opacity-100'>
          <div className='verdicttext'>
            <p>Verdict:</p>
          </div>
          <div className='max-w-2xl text-center mb-6 px-4'>
            <p className='text-lg text-gray-400 italic'>“{claim}”</p>
          </div>
          <div className='bigtext'>
            <p>{result.verdict ?? 'No Verdict'}</p>
          </div>
          {result.confidence && (
            <div className='mt-2 text-center text-gray-400 text-lg'>
              Confidence Level:{' '}
              <span className='font-semibold text-white'>
                {Number(result.confidence).toFixed(1)}%
              </span>
            </div>
          )}

          {result.sources && result.sources.length > 0 && (
            <div className='flex flex-col md:flex-row gap-6 mt-6 max-w-6xl w-full'>
              {/* Articles Section */}
              <div className='flex-1'>
                <p className='articles-title font-semibold mb-2'>
                  Relevant Articles:
                </p>
                <div className='articles-grid grid gap-3'>
                  {result.sources.map((url, index) => (
                    <a
                      key={index}
                      href={url}
                      target='_blank'
                      rel='noopener noreferrer'
                      className='article-box p-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition'
                    >
                      <p className='article-headline'>
                        {result.headlines?.[url] || url}
                      </p>
                    </a>
                  ))}
                </div>
              </div>

              {/* Justification Section */}
              {justificationBuffer && (
                <div className='flex-1 bg-gray-[#303030] p-4 rounded-lg text-gray-200 max-h-[400px] overflow-y-auto'>
                  <p className='justification-title sticky font-semibold mb-2'>
                    Justification:
                  </p>
                  <pre className='justification-box whitespace-pre-wrap'>
                    {result.justification}
                  </pre>
                </div>
              )}
            </div>
          )}

          <button
            onClick={handleTryAgain}
            className='mt-4 px-4 py-2 rounded-md text-base bg-[#303030] border-[#303030] text-white hover:bg-white hover:text-black transition'
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}

export default Home;
