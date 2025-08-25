"use client"
import React, { useEffect, useState } from "react";

function Home() {
    const [message, setMessage] = useState("");
    const [news, setNews] = useState("");
    const [placeholder, setPlaceholder] = useState("");

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

        const type = () => {
            if (typingForward) {
                setPlaceholder(currentPhrase.slice(0, charIndex + 1));
                charIndex++;

                if (charIndex === currentPhrase.length) {
                    typingForward = false;
                    setTimeout(type, pauseTime);
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
            setTimeout(type, typeSpeed);
        };

        type();

        return () => {

        };
    }, []);

    const handleSubmit = () => {
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

        postData("http://localhost:8080/api/home", { name: news })
            .then(data => {
                setMessage(data.message);
            });
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center">


            <div className="relative w-full max-w-2xl">
                <textarea 
                    className="w-full h-32 text-base p-3 pr-20 rounded-xl border border-gray-300 mt-3 resize focus:outline-none focus:ring-0 focus:border-gray-300"  
                    placeholder={placeholder}
                    name="news" 
                    value={news}
                    onChange={(e) => setNews(e.target.value)} 
                />

                {news.trim() !== "" && (
                    <button 
                        className="absolute bottom-3 right-3 px-3 py-1 text-sm bg-black text-white rounded hover:bg-gray-800 transition"
                        onClick={handleSubmit}
                    >
                        Submit
                    </button>
                )}
            </div>

            {message && (
                <div className="mt-4 text-center text-lg text-gray-800">
                    {message}
                </div>
            )}
        </div>
    );
}

export default Home;
