'use client';
import React from 'react';

const stats = [
    { num: '3.32', label: 'Average hours per day Filipinos\nspend on social media' },
    { num: '5', label: 'Agile sprints used\nto build the system' },
    { num: '4', label: 'NLP models powering\nthe pipeline' },
];

const pipeline = [
    {
        step: 'STAGE 01',
        name: 'Gatekeeping',
        desc: 'Non-verifiable claims — opinion, satire, ambiguous language — are filtered out before entering the pipeline.',
    },
    {
        step: 'STAGE 02',
        name: 'Evidence Retrieval',
        desc: 'Web scraping tools query credible Philippine news outlets, building a live evidence database for each claim.',
    },
    {
        step: 'STAGE 03',
        name: 'Semantic Analysis',
        desc: 'Similarity algorithms compare the claim against retrieved articles at the level of meaning, not just keywords.',
    },
    {
        step: 'STAGE 04',
        name: 'Verdict Generation',
        desc: 'A final module produces a verdict, confidence score, and plain-language justification for every result.',
    },
];

const models = [
    {
        source: 'Meta / Facebook',
        name: 'BART',
        role: 'Fact-checkability classification — decides whether a claim is even verifiable before any further analysis runs.',
    },
    {
        source: 'Explosion AI',
        name: 'spaCy',
        role: 'Tokenization and named entity extraction — breaks claims into structured components the rest of the pipeline can reason over.',
    },
    {
        source: 'Sentence Transformers',
        name: 'DistilUSE',
        role: 'Semantic similarity analysis — measures how closely a claim aligns with retrieved news articles in meaning.',
    },
    {
        source: 'Microsoft',
        name: 'DeBERTa',
        role: 'Natural Language Inference — determines whether evidence entails, contradicts, or is neutral toward the claim.',
    },
];

function About() {
    return (
        <div className='min-h-screen relative' style={{ backgroundColor: '#212121', color: '#f0f4f8', fontFamily: 'Arial, Helvetica, sans-serif' }}>

            {/* Dot background */}
            <div style={{
                position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0,
                backgroundImage: 'radial-gradient(circle, #383838 1px, transparent 1px)',
                backgroundSize: '28px 28px', opacity: 0.5,
            }} />

            <div style={{ position: 'relative', zIndex: 1, maxWidth: 860, margin: '0 auto', padding: '72px 24px 100px' }}>

                {/* Hero */}
                <div style={{ textAlign: 'center', marginBottom: 60 }}>
                    <div className='bigtext' style={{ fontSize: 'clamp(40px, 8vw, 60px)', lineHeight: 1.1 }}>
                        Deception Detector
                    </div>
                    <div className='bigtext2' style={{ fontSize: 'clamp(18px, 3vw, 28px)', opacity: 0.7, paddingBottom: 0 }}>
                        Automated fact-checking for the Philippine web.
                    </div>
                </div>

                {/* Stats */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 56 }}>
                    {stats.map((s, i) => (
                        <div key={i} style={{ background: '#303030', borderRadius: 8, padding: '24px 16px', textAlign: 'center' }}>
                            <div style={{
                                fontSize: 36, fontWeight: 100, lineHeight: 1, marginBottom: 8,
                                background: 'linear-gradient(to right, #ff6e7f, #bfe9ff)',
                                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                            }}>
                                {s.num}
                            </div>
                            <div style={{ fontSize: 12, color: '#898989', lineHeight: 1.5, whiteSpace: 'pre-line' }}>
                                {s.label}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Abstract */}
                <div style={{ marginBottom: 52 }}>
                    <div style={{ fontSize: 12, color: '#898989', letterSpacing: 2, textTransform: 'uppercase', marginBottom: 12 }}>
                        Abstract
                    </div>
                    <div style={{ fontSize: 22, fontWeight: 100, color: '#ffffff', marginBottom: 14 }}>
                        What is Deception Detector?
                    </div>
                    <div style={{ fontSize: 14, color: '#898989', lineHeight: 1.85, maxWidth: 720 }}>
                        A web-based fact-checking platform built to address the misinformation crisis on Philippine social media.
                        Using a Hybrid Natural Language Processing framework, the system provides automated, transparent claim
                        verification designed specifically for the Philippine context — complete with confidence scores and
                        plain-language justifications that users can actually trust.
                    </div>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid #303030', margin: '52px 0' }} />

                {/* Pipeline */}
                <div style={{ marginBottom: 52 }}>
                    <div style={{ fontSize: 12, color: '#898989', letterSpacing: 2, textTransform: 'uppercase', marginBottom: 12 }}>
                        Pipeline
                    </div>
                    <div style={{ fontSize: 22, fontWeight: 100, color: '#ffffff', marginBottom: 8 }}>
                        How a claim gets verified
                    </div>
                    <div style={{ fontSize: 14, color: '#898989', lineHeight: 1.85, marginBottom: 24 }}>
                        Every submission passes through four sequential stages before a verdict is returned.
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12 }}>
                        {pipeline.map((p, i) => (
                            <div
                                key={i}
                                style={{ background: '#303030', borderRadius: 8, padding: 20, transition: 'background-color 0.3s ease', cursor: 'default' }}
                                onMouseEnter={e => e.currentTarget.style.backgroundColor = '#3a3a3a'}
                                onMouseLeave={e => e.currentTarget.style.backgroundColor = '#303030'}
                            >
                                <div style={{ fontSize: 11, color: '#555', letterSpacing: 1, marginBottom: 6 }}>{p.step}</div>
                                <div style={{ fontSize: 16, fontWeight: 400, color: '#f0f4f8', marginBottom: 6 }}>{p.name}</div>
                                <div style={{ fontSize: 12, color: '#898989', lineHeight: 1.7 }}>{p.desc}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid #303030', margin: '52px 0' }} />

                {/* Models */}
                <div style={{ marginBottom: 52 }}>
                    <div style={{ fontSize: 12, color: '#898989', letterSpacing: 2, textTransform: 'uppercase', marginBottom: 12 }}>
                        Models
                    </div>
                    <div style={{ fontSize: 22, fontWeight: 100, color: '#ffffff', marginBottom: 8 }}>
                        The NLP Stack
                    </div>
                    <div style={{ fontSize: 14, color: '#898989', lineHeight: 1.85, marginBottom: 24 }}>
                        Four specialized models, each assigned to what it does best.
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12 }}>
                        {models.map((m, i) => (
                            <div
                                key={i}
                                style={{ background: '#303030', borderRadius: 8, padding: 20, transition: 'background-color 0.3s ease, transform 0.3s ease', cursor: 'default' }}
                                onMouseEnter={e => { e.currentTarget.style.backgroundColor = '#3a3a3a'; e.currentTarget.style.transform = 'scale(1.02)'; }}
                                onMouseLeave={e => { e.currentTarget.style.backgroundColor = '#303030'; e.currentTarget.style.transform = 'scale(1)'; }}
                            >
                                <div style={{ fontSize: 11, color: '#555', letterSpacing: 1, textTransform: 'uppercase', marginBottom: 6 }}>{m.source}</div>
                                <div style={{
                                    fontSize: 18, fontWeight: 100, marginBottom: 8,
                                    background: 'linear-gradient(to right, #ff6e7f, #bfe9ff)',
                                    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                                }}>
                                    {m.name}
                                </div>
                                <div style={{ fontSize: 12, color: '#898989', lineHeight: 1.7 }}>{m.role}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid #303030', margin: '52px 0' }} />

                {/* Purpose */}
                <div style={{ marginBottom: 52 }}>
                    <div style={{ fontSize: 12, color: '#898989', letterSpacing: 2, textTransform: 'uppercase', marginBottom: 12 }}>
                        Purpose
                    </div>
                    <div style={{ fontSize: 22, fontWeight: 100, color: '#ffffff', marginBottom: 24 }}>
                        Why we built this
                    </div>
                    <div style={{
                        background: '#303030', borderRadius: 8, padding: 28,
                        borderLeft: '2px solid #ff6e7f',
                    }}>
                        <div style={{ fontSize: 17, fontWeight: 100, color: '#f0f4f8', lineHeight: 1.6, marginBottom: 16 }}>
                            The Philippines leads all Asia-Pacific nations in daily social media use. That reach is also misinformation&apos;s greatest advantage.
                        </div>
                        <div style={{ fontSize: 13, color: '#898989', lineHeight: 1.9 }}>
                            Misinformation spreads because it&apos;s fast, emotionally compelling, and nearly impossible to verify manually at scale.
                            Deception Detector was built to close that gap — an automated tool that dissects news claims, collects evidence from
                            credible local sources, and performs semantic analysis to separate fact from falsehood.
                            <br /><br />
                            The goal isn&apos;t just accuracy. It&apos;s transparency. Every verdict comes with a justification and a confidence score,
                            so users understand the reasoning — not just the conclusion. By making fact-checking accessible and explainable,
                            the system promotes digital literacy and gives Filipino users a real upper hand against organized misinformation campaigns.
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, paddingTop: 32, borderTop: '1px solid #303030' }}>
                    <div className='w-4 h-4 rounded-full dot dot-animation dot-animation-1' />
                    <div className='w-4 h-4 rounded-full dot dot-animation dot-animation-2' />
                    <div className='w-4 h-4 rounded-full dot dot-animation dot-animation-3' />
                    <div style={{ fontSize: 12, color: '#898989' }}>
                        Developed using Agile methodology across five sprints &mdash; tailored for the Philippine information ecosystem.
                    </div>
                </div>

            </div>
        </div>
    );
}

export default About;