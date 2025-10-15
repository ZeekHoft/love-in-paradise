"use client";
import React, { useEffect, useState } from "react";

function Home() {
  const [message, setMessage] = useState({});
  const [news, setNews] = useState("");
  const [placeholder, setPlaceholder] = useState("");
  const [loading, setLoading] = useState(false);
  const [showVerdict, setShowVerdict] = useState(false);
  const [isVerdictTrue, setIsVerdictTrue] = useState(false);
  const [useLLM, setUseLLM] = useState(false);

  const rotatingPhrases = [
    "Government to distribute ₱10,000 cash aid to all residents next week, claims viral post.",
    "New law allegedly bans students from using cellphones inside classrooms starting next month.",
    "Post claims Cebu Pacific offering free domestic flights to celebrate anniversary.",
    "Viral TikTok video says NLEX toll fees will double by December.",
    "Rumor spreads that 13th month pay will be released early due to inflation.",
    "Facebook post claims NAIA will be renamed 'Manila International Spaceport' under new project.",
    "Circulating message warns of total lockdown due to rising dengue cases.",
    "Unverified post says public schools to switch to four-day class schedule permanently.",
    "Claim: Government to replace jeepneys with AI-driven buses by 2026.",
    "Message chain alleges that voting age will be lowered to 15 starting next elections.",
    "Fake memo says MRT operations will be suspended for three months for 'AI system upgrade.'",
    "Viral article claims electricity bills will be cut in half after new DOE policy.",
    "Tweet claims rice will be sold at ₱15 per kilo starting next week.",
    "Shared post alleges free internet for all barangays starting this month.",
    "Message circulating online says DOH confirmed new COVID-23 variant in Quezon City.",
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

  const handleSubmit = () => {
    setLoading(true);

    async function readStream(url = "", data = {}) {
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        const reader = response.body.getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            setLoading(false);
            setIsVerdictTrue(true);
            setShowVerdict(true);
            break;
          }

          const decoder = new TextDecoder("utf-8");
          console.log(decoder.decode(value));
          const latestMessage = JSON.parse(decoder.decode(value));

          if (latestMessage.articles || latestMessage.article_urls) {
            setMessage((prev) => ({
              ...prev,
              articles: latestMessage.articles || latestMessage.article_urls,
            }));
          }

          setMessage((prev) => ({ ...prev, ...latestMessage }));
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
        setMessage({ justification: "An error occurred. Please try again." });
      }
    }

    readStream("http://localhost:8080/api/home", {
      name: news,
      use_llm: useLLM,
    });
  };

  const handleTryAgain = () => {
    setShowVerdict(false);
    setNews("");
    setMessage({});
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative dotanim">
      {loading && (
        <div className="flex flex-col items-center justify-center absolute inset-0 transition-opacity duration-500 opacity-100">
          <div className="bigtext2 transition-all">
            <p>{message.currentProcess ?? "Processing"}</p>
          </div>
          <div className="inset-0 flex items-center justify-center bg-transparent z-10">
            <div className="flex space-x-2">
              <div className="w-4 h-4 rounded-full dot dot-animation dot-animation-1"></div>
              <div className="w-4 h-4 rounded-full dot dot-animation dot-animation-2"></div>
              <div className="w-4 h-4 rounded-full dot dot-animation dot-animation-3"></div>
            </div>
          </div>
        </div>
      )}

      {!showVerdict ? (
        <div
          className={`flex flex-col items-center w-full transition-opacity duration-500 ${
            loading ? "opacity-0 pointer-events-none" : "opacity-100"
          }`}
        >
          <div className="bigtext">
            <p>Hello.</p>
          </div>

          <div className="bigtext2">
            <p>You got news to check?</p>
          </div>

          {/* 👇 LLM toggle */}
          <div className="flex items-center space-x-2 mt-4">
            <label className="text-gray-300 text-sm">Use LLM</label>
            <button
              onClick={() => setUseLLM(!useLLM)}
              className={`w-12 h-6 flex items-center rounded-full p-1 transition ${
                useLLM ? "bg-green-500" : "bg-gray-500"
              }`}
            >
              <div
                className={`bg-white w-4 h-4 rounded-full transform transition ${
                  useLLM ? "translate-x-6" : ""
                }`}
              />
            </button>
          </div>

          <div className="relative w-full max-w-2xl">
            <textarea
              className="w-full h-32 text-base p-3 pr-20 rounded-xl mt-3 resize focus:outline-none focus:ring-0 focus:border-gray-300"
              placeholder={placeholder}
              name="news"
              value={news}
              onChange={(e) => setNews(e.target.value)}
            />

            {news.trim() !== "" && (
              <button className="submit_btn" onClick={handleSubmit}>
                Submit
              </button>
            )}
          </div>

          <div className="disclaimer">
            <p>
              Deception Detector may display inaccurate information. Please
              supplement the responses with your own due diligence.
            </p>
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center absolute inset-0 transition-opacity duration-500 opacity-100">
          <div className="verdicttext">
            <p>Verdict:</p>
          </div>
          <div className="max-w-2xl text-center mb-6 px-4">
            <p className="text-lg text-gray-400 italic">“{news}”</p>
          </div>
          <div className="bigtext">
            <p>{message.verdict ?? "No Verdict"}</p>
          </div>
          {message.confidence && (
            <div className="mt-2 text-center text-gray-400 text-lg">
              Confidence Level:{" "}
              <span className="font-semibold text-white">
                {Number(message.confidence).toFixed(1)}%
              </span>
            </div>
          )}
          {message.article_urls && message.article_urls.length > 0 && (
            <div className="articles-container">
              <p className="articles-title">Relevant Articles:</p>
              <div className="articles-grid">
                {message.article_urls.map((url, index) => (
                  <a
                    key={index}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="article-box"
                  >
                    <p className="article-headline">
                      {message.headlines?.[url] || url}
                    </p>
                  </a>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={handleTryAgain}
            className="mt-4 px-4 py-2 rounded-md text-base bg-[#303030] border-[#303030] text-white hover:bg-white hover:text-black transition"
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}

export default Home;
