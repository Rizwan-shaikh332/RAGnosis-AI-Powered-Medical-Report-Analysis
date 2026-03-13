import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'

const PIPELINE_STEPS = [
    {
        id: 0, icon: '📄', title: 'Document Input', model: 'Upload Layer',
        subtitle: 'PDF / JPG / PNG / JPEG',
        color: '#3b82f6',
        desc: 'Patient uploads a medical report in any format. The system detects file type and routes to the appropriate text extractor.',
        tech: ['pdfplumber', 'pytesseract (OCR)', 'Pillow'],
        detail: 'PDF text is extracted page-by-page using pdfplumber. Scanned images and photos go through pytesseract OCR (Optical Character Recognition) to convert pixels → text.'
    },
    {
        id: 1, icon: '🧹', title: 'Text Preprocessing', model: 'NLP Pipeline',
        subtitle: 'Clean → Tokenize → Chunk',
        color: '#8b5cf6',
        desc: 'Raw text is cleaned, normalized, and chunked into 512-token segments that transformer models can process.',
        tech: ['regex', 'NLTK', 'HuggingFace Tokenizer'],
        detail: 'Medical abbreviations expanded, noise removed, text segmented. Tokenizer converts text to model-readable tokens using BERT WordPiece vocabulary (30,000+ tokens).'
    },
    {
        id: 2, icon: '🧬', title: 'BERT Encoding', model: 'BioBERT',
        subtitle: 'dmis-lab/biobert-base-cased-v1.1',
        color: '#00d4aa',
        desc: 'BioBERT, fine-tuned on PubMed + PMC biomedical text, generates contextual embeddings and extracts medical named entities.',
        tech: ['BioBERT', 'Transformers', 'Medical NER'],
        detail: 'Bidirectional Encoder Representations from Transformers. Each word gets a 768-dim token embedding capturing bi-directional context. Medical entities (diseases, drugs, lab values) are extracted via NER classification heads.'
    },
    {
        id: 3, icon: '🔍', title: 'RAG Retrieval', model: 'FAISS + MiniLM',
        subtitle: 'sentence-transformers/all-MiniLM-L6-v2',
        color: '#f59e0b',
        desc: 'The report query is embedded and FAISS similarity search finds the top-5 most relevant medical knowledge chunks from the 500+ item vector database.',
        tech: ['FAISS', 'sentence-transformers', 'Cosine Similarity'],
        detail: 'Retrieval-Augmented Generation: query is encoded into a 384-dim dense vector, normalized, and matched against pre-indexed medical QA embeddings using inner product (cosine) similarity. Top-K=5 chunks retrieved in <10ms.'
    },
    {
        id: 4, icon: '📝', title: 'BART Summarization', model: 'facebook/bart-large-cnn',
        subtitle: '406M parameter seq2seq model',
        color: '#ec4899',
        desc: 'BART (Bidirectional and Auto-Regressive Transformer) condenses the medical report into a clear, patient-friendly summary.',
        tech: ['BART-Large', 'Beam Search', 'Seq2Seq'],
        detail: 'Encoder-decoder architecture. Report text (max 1024 tokens) → encoder creates rich representation → decoder auto-regressively generates summary via beam search (beam=4, length_penalty=2.0, max_length=300 tokens).'
    },
    {
        id: 5, icon: '🤖', title: 'Groq LLM Chat', model: 'llama3-8b-8192',
        subtitle: 'Groq Inference API · <1s latency',
        color: '#10b981',
        desc: 'Patient questions are answered by Llama3 8B, enriched with RAG context and the patient\'s own report, running at ultra-low latency on Groq\'s LPU hardware.',
        tech: ['Groq API', 'LLaMA 3', 'Function Calling'],
        detail: 'Groq LPU (Language Processing Unit) achieves 500+ tokens/sec — 10-20x faster than GPU inference. System prompt + RAG context + report excerpt = accurate, empathetic medical answers with source grounding.'
    },
    {
        id: 6, icon: '📊', title: 'Output & Visualization', model: 'Frontend Layer',
        subtitle: 'React · Recharts · Real-time',
        color: '#6366f1',
        desc: 'Results are streamed to the patient dashboard: AI summary, health metric cards with status indicators, trend charts, and the interactive chatbot.',
        tech: ['React + Vite', 'Recharts', 'Framer Motion'],
        detail: 'Health metrics extracted via regex patterns from report text. Compared against clinical reference ranges from the blood_report_reference.csv dataset. Bar/line charts visualize trends across multiple reports over time.'
    },
]

export default function SystemAnimation() {
    const [activeStep, setActiveStep] = useState(0)
    const [playing, setPlaying] = useState(true)
    const [showDetail, setShowDetail] = useState(false)

    useEffect(() => {
        if (!playing) return
        const interval = setInterval(() => {
            setActiveStep(prev => (prev + 1) % PIPELINE_STEPS.length)
        }, 2800)
        return () => clearInterval(interval)
    }, [playing])

    const step = PIPELINE_STEPS[activeStep]

    return (
        <div className="page-wrapper" style={{ background: 'var(--bg-primary)', minHeight: '100vh' }}>
            {/* Background grid */}
            <div style={{
                position: 'fixed', inset: 0, pointerEvents: 'none',
                backgroundImage: 'linear-gradient(rgba(0,212,170,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,170,0.03) 1px, transparent 1px)',
                backgroundSize: '60px 60px', zIndex: 0
            }} />

            <div className="container" style={{ position: 'relative', zIndex: 1, paddingTop: 32, paddingBottom: 60 }}>
                {/* Header */}
                <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} style={{ textAlign: 'center', marginBottom: 48 }}>
                    <div className="badge badge-cyan" style={{ margin: '0 auto 16px', display: 'inline-flex' }}>
                        <div className="pulse-dot" /> RAGnosis Architecture
                    </div>
                    <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 900, letterSpacing: '-0.04em', marginBottom: 12 }}>
                        How <span className="gradient-text">RAGnosis</span> Works
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', maxWidth: 580, margin: '0 auto 20px', lineHeight: 1.8 }}>
                        A complete end-to-end AI pipeline — from raw medical report to actionable insights —
                        powered by BERT, BART, FAISS RAG, and Groq LLM.
                    </p>
                    <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
                        <button
                            className={playing ? 'btn-secondary' : 'btn-primary'}
                            id="play-pause-btn"
                            onClick={() => setPlaying(!playing)}
                        >
                            {playing ? '⏸ Pause' : '▶ Play'} Animation
                        </button>
                        <Link to="/register" className="btn-primary">🚀 Try RAGnosis</Link>
                    </div>
                </motion.div>

                {/* Pipeline nodes - linear */}
                <div style={{ overflowX: 'auto', paddingBottom: 16 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 0, minWidth: 900, justifyContent: 'center', marginBottom: 40 }}>
                        {PIPELINE_STEPS.map((s, idx) => (
                            <div key={s.id} style={{ display: 'flex', alignItems: 'center' }}>
                                {/* Node */}
                                <motion.div
                                    whileHover={{ scale: 1.05 }}
                                    onClick={() => { setActiveStep(idx); setPlaying(false) }}
                                    style={{ cursor: 'pointer' }}
                                >
                                    <div className="node-box" style={{
                                        width: 108, padding: '14px 10px',
                                        borderColor: activeStep === idx ? s.color : 'var(--border)',
                                        boxShadow: activeStep === idx ? `0 0 30px ${s.color}44` : 'none',
                                        background: activeStep === idx ? `${s.color}11` : 'var(--bg-card)',
                                    }}>
                                        {activeStep === idx && (
                                            <motion.div
                                                animate={{ scale: [1, 1.3, 1], opacity: [0.6, 1, 0.6] }}
                                                transition={{ duration: 1.5, repeat: Infinity }}
                                                style={{ position: 'absolute', inset: -2, borderRadius: 'inherit', border: `2px solid ${s.color}`, pointerEvents: 'none' }}
                                            />
                                        )}
                                        <div style={{ fontSize: '1.8rem', marginBottom: 6 }}>{s.icon}</div>
                                        <div style={{ fontSize: '0.72rem', fontWeight: 700, lineHeight: 1.3, color: activeStep === idx ? s.color : 'var(--text-primary)' }}>
                                            {s.title}
                                        </div>
                                        <div style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginTop: 3, lineHeight: 1.2 }}>{s.model}</div>
                                    </div>
                                </motion.div>

                                {/* Arrow */}
                                {idx < PIPELINE_STEPS.length - 1 && (
                                    <div style={{ flex: '0 0 28px', textAlign: 'center', position: 'relative' }}>
                                        <motion.div
                                            animate={playing && activeStep === idx ? { x: [-8, 4, -8], opacity: [0.4, 1, 0.4] } : {}}
                                            transition={{ duration: 0.8, repeat: Infinity }}
                                            style={{ color: activeStep === idx ? 'var(--accent-cyan)' : 'var(--text-muted)', fontSize: '1.2rem' }}
                                        >
                                            →
                                        </motion.div>
                                        {/* Moving data packet */}
                                        <AnimatePresence>
                                            {playing && activeStep === idx && (
                                                <motion.div
                                                    initial={{ left: 0, opacity: 1 }}
                                                    animate={{ left: 28, opacity: 0 }}
                                                    exit={{}}
                                                    transition={{ duration: 0.6, repeat: Infinity }}
                                                    style={{
                                                        position: 'absolute', top: '50%', transform: 'translateY(-50%)',
                                                        width: 8, height: 8, borderRadius: '50%',
                                                        background: 'var(--accent-cyan)',
                                                        boxShadow: '0 0 8px var(--accent-cyan)',
                                                    }}
                                                />
                                            )}
                                        </AnimatePresence>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Step counter dots */}
                <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginBottom: 36 }}>
                    {PIPELINE_STEPS.map((s, i) => (
                        <div
                            key={i}
                            onClick={() => { setActiveStep(i); setPlaying(false) }}
                            style={{
                                width: i === activeStep ? 28 : 8, height: 8, borderRadius: 4,
                                background: i === activeStep ? s.color : 'var(--border)',
                                cursor: 'pointer', transition: 'all 0.3s ease'
                            }}
                        />
                    ))}
                </div>

                {/* Active step detail */}
                <AnimatePresence mode="wait">
                    <motion.div
                        key={activeStep}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.35 }}
                        className="card"
                        style={{
                            maxWidth: 860, margin: '0 auto',
                            borderColor: step.color + '44',
                            boxShadow: `0 0 40px ${step.color}1a`
                        }}
                    >
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 20, flexWrap: 'wrap' }}>
                            <div style={{
                                width: 72, height: 72, borderRadius: 20, flexShrink: 0,
                                background: step.color + '22', border: `1px solid ${step.color}44`,
                                display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem'
                            }}>
                                {step.icon}
                            </div>
                            <div style={{ flex: 1 }}>
                                <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap', marginBottom: 4 }}>
                                    <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.75rem', color: step.color, fontWeight: 600 }}>
                                        STEP {activeStep + 1}/{PIPELINE_STEPS.length}
                                    </span>
                                    <div className="badge" style={{ background: step.color + '22', color: step.color, border: `1px solid ${step.color}44` }}>
                                        {step.model}
                                    </div>
                                </div>
                                <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: 8 }}>{step.title}</h2>
                                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: 16 }}>{step.desc}</p>

                                {/* Tech badges */}
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
                                    {step.tech.map(t => (
                                        <span key={t} style={{
                                            background: 'var(--bg-secondary)', padding: '4px 12px', borderRadius: 100,
                                            fontSize: '0.78rem', fontFamily: 'JetBrains Mono, monospace',
                                            color: step.color, border: `1px solid ${step.color}33`
                                        }}>{t}</span>
                                    ))}
                                </div>

                                {/* Toggle deep detail */}
                                <button
                                    className="btn-ghost"
                                    style={{ fontSize: '0.82rem', padding: '6px 14px' }}
                                    onClick={() => setShowDetail(!showDetail)}
                                >
                                    {showDetail ? '▲ Less Detail' : '▼ Technical Deep Dive'}
                                </button>
                                <AnimatePresence>
                                    {showDetail && (
                                        <motion.div
                                            initial={{ opacity: 0, height: 0 }}
                                            animate={{ opacity: 1, height: 'auto' }}
                                            exit={{ opacity: 0, height: 0 }}
                                            style={{ overflow: 'hidden' }}
                                        >
                                            <div style={{
                                                marginTop: 16, padding: 16,
                                                background: 'var(--bg-secondary)', borderRadius: 12,
                                                fontSize: '0.88rem', lineHeight: 1.8,
                                                color: 'var(--text-secondary)',
                                                borderLeft: `3px solid ${step.color}`
                                            }}>
                                                {step.detail}
                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        </div>
                    </motion.div>
                </AnimatePresence>

                {/* Bottom summary cards */}
                <div style={{ marginTop: 56 }}>
                    <h2 style={{ textAlign: 'center', fontWeight: 800, marginBottom: 32, fontSize: '1.6rem' }}>
                        Complete <span className="gradient-text">Tech Stack</span>
                    </h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
                        {[
                            { icon: '⚛️', title: 'Frontend', items: ['React + Vite', 'Framer Motion', 'Recharts', 'React Router'] },
                            { icon: '🐍', title: 'Backend', items: ['Python Flask', 'PyMongo', 'JWT Auth', 'Werkzeug'] },
                            { icon: '🧠', title: 'AI Models', items: ['BERT (BioBERT)', 'BART-Large-CNN', 'MiniLM-L6-v2', 'LLaMA 3 8B'] },
                            { icon: '🔍', title: 'RAG Engine', items: ['FAISS Index', 'sentence-transformers', 'MedQuAD Dataset', 'Cosine Search'] },
                            { icon: '🗄️', title: 'Database', items: ['MongoDB Atlas', 'User Profiles', 'Report Storage', 'Vector Store'] },
                            { icon: '⚡', title: 'Infrastructure', items: ['Groq LPU API', 'pdfplumber', 'pytesseract OCR', 'CUDA/CPU'] },
                        ].map(s => (
                            <motion.div key={s.title}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                className="card"
                            >
                                <div style={{ fontSize: '1.5rem', marginBottom: 10 }}>{s.icon}</div>
                                <h3 style={{ fontWeight: 700, marginBottom: 10, color: 'var(--accent-cyan)' }}>{s.title}</h3>
                                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 6 }}>
                                    {s.items.map(i => (
                                        <li key={i} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: 8 }}>
                                            <span style={{ color: 'var(--accent-cyan)', fontSize: '0.6rem' }}>◆</span> {i}
                                        </li>
                                    ))}
                                </ul>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
