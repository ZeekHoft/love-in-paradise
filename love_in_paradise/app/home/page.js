"use client"
import React, { useEffect, useState } from "react";

function Home() {
    const [message, setMessage] = useState("");
    const [news, setNews] = useState("");
    const [placeholder, setPlaceholder] = useState("");
    const [loading, setLoading] = useState(false);
    const [showVerdict, setShowVerdict] = useState(false);
    const [isVerdictTrue, setIsVerdictTrue] = useState(false);

    const rotatingPhrases = [
        "Pigeon named Kevin runs for mayor, promises more breadcrumbs.",
        "Breaking: Dog learns to code, builds better website than you.",
        "Local cat starts podcast, gains 1M followers overnight.",
        "Aliens demand WiFi password before invading.",
        "Scientists baffled: bread now sentient and tweeting."
    ];

    useEffect(() => {
        let phraseIndex = 0;
        let charIndex = 0;
        let currentPhrase = rotatingPhrases[phraseIndex];
        let typingForward = true;

        const typeSpeed = 70;
        const pauseTime = 2000;
        let timeoutId;

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

        const postData = async (url = '', data = {}) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return response.json();
        };

        setTimeout(() => {
            postData("http://localhost:8080/api/home", { name: news })
                .then(data => {
                    setLoading(false);
                    setMessage(data.message);
                    setIsVerdictTrue(true);
                    setShowVerdict(true);
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    setLoading(false);
                    setMessage("An error occurred. Please try again.");
                });
        }, 1500);
    };

    const handleTryAgain = () => {
        setShowVerdict(false);
        setNews("");
        setMessage("");
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center relative">
            <style>
                {`
                @keyframes hop {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-10px);
                    }
                }
                .dot {
                    background: linear-gradient(to right, #ff6e7f, #bfe9ff);
                }
                .dot-animation {
                    animation: hop 0.6s infinite;
                }
                .dot-animation-1 {
                    animation-delay: 0s;
                }
                .dot-animation-2 {
                    animation-delay: 0.1s;
                }
                .dot-animation-3 {
                    animation-delay: 0.2s;
                }
                `}
            </style>

            {loading && (
                <div className="absolute inset-0 flex items-center justify-center bg-transparent z-10">
                    <div className="flex space-x-2">
                        <div className="w-4 h-4 rounded-full dot dot-animation dot-animation-1"></div>
                        <div className="w-4 h-4 rounded-full dot dot-animation dot-animation-2"></div>
                        <div className="w-4 h-4 rounded-full dot dot-animation dot-animation-3"></div>
                    </div>
                </div>
            )}
            
            {!showVerdict ? (
                <div className={`flex flex-col items-center w-full transition-opacity duration-500 ${loading ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}>
                    <div className="bigtext">
                        <p>Hello.</p>
                    </div>

                    <div className="bigtext2">
                        <p>You got news to check?</p>
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
                            <button 
                                className="absolute bottom-3 right-3 px-3 py-1 border rounded text-sm bg-black border border-white-500 text-white hover:bg-white hover:text-black transition"
                                onClick={handleSubmit}
                            >
                                Submit
                            </button>
                        )}
                    </div>

                    <div className="disclaimer">
                        <p>Deception Detector may display inaccurate information. Please supplement the responses with your own due diligence.</p>
                    </div>
                </div>
            ) : (
                <div className="flex flex-col items-center justify-center absolute inset-0 transition-opacity duration-500 opacity-100">
                    <div className="verdicttext">
                        <p>Verdict:</p>
                    </div>
                    <div className="bigtext">
                        <p>True</p>
                    </div>
                    <div className="mt-4 text-center text-lg text-gray-800">
                        {message}
                    </div>
                    <button
                        onClick={handleTryAgain}
                        className="mt-8 px-8 py-3 rounded-full text-lg bg-black border border-white-500 text-white hover:bg-white hover:text-black transition"
                    >
                        Try Again
                    </button>
                </div>
            )}
            
        </div>
    );
}

export default Home;