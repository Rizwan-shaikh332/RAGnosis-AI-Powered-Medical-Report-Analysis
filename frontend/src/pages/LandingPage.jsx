import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

const features = [
    { icon: '🧬', title: 'BERT + BART Analysis', desc: 'Fine-tuned transformer models extract medical entities and generate human-readable summaries from your reports.' },
    { icon: '🔍', title: 'RAG Knowledge Base', desc: 'Retrieval-Augmented Generation from a curated medical knowledge base gives accurate, contextual answers.' },
    { icon: '📊', title: 'Health Metrics Charts', desc: 'Automatic extraction of blood values (hemoglobin, glucose, cholesterol) with trend visualization.' },
    { icon: '🤖', title: 'AI Chatbot', desc: 'Ask any question about your report. Groq-powered LLM answers in simple, patient-friendly language.' },
    { icon: '🔒', title: 'Secure & Private', desc: 'Data encrypted at rest. Only you can access your medical reports via JWT-secured sessions.' },
    { icon: '📄', title: 'Multi-Format Support', desc: 'Upload PDF, JPG, PNG, and JPEG reports. OCR extracts text from scanned images automatically.' },
]

const steps = [
    { num: '01', title: 'Upload Report', desc: 'Drop your medical report in any format — PDF, image, or scan.' },
    { num: '02', title: 'AI Extraction', desc: 'BERT extracts entities; BART generates a patient-friendly summary.' },
    { num: '03', title: 'RAG Retrieval', desc: 'FAISS vector search finds relevant medical context for your specific values.' },
    { num: '04', title: 'Get Insights', desc: 'Read your summary, view health charts, and chat with your AI doctor.' },
]

const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.12 } }
}
const itemVariants = {
    hidden: { opacity: 0, y: 24 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
}

export default function LandingPage() {
    return (
        <div className="page-wrapper" style={{ paddingTop: 72, overflowX: 'hidden' }}>
            {/* Hero */}
            <section style={{ position: 'relative', minHeight: '92vh', display: 'flex', alignItems: 'center', overflow: 'hidden' }}>
                {/* Orbs */}
                <div className="orb orb-cyan" style={{ width: 600, height: 600, top: -200, left: -200 }} />
                <div className="orb orb-purple" style={{ width: 500, height: 500, bottom: -100, right: -100 }} />
                {/* Grid overlay */}
                <div style={{
                    position: 'absolute', inset: 0,
                    backgroundImage: 'linear-gradient(rgba(0,212,170,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,170,0.03) 1px, transparent 1px)',
                    backgroundSize: '60px 60px',
                    pointerEvents: 'none'
                }} />

                <div className="container" style={{ position: 'relative', zIndex: 1, padding: '80px 24px' }}>
                    <motion.div
                        initial={{ opacity: 0, y: 40 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7 }}
                        style={{ maxWidth: 720 }}
                    >
                        <div className="badge badge-cyan" style={{ marginBottom: 24 }}>
                            <div className="pulse-dot" />
                            AI-Powered Medical Analysis
                        </div>
                        <h1 style={{ fontSize: 'clamp(2.5rem, 6vw, 4.5rem)', fontWeight: 900, lineHeight: 1.1, letterSpacing: '-0.04em', marginBottom: 24 }}>
                            Understand Your<br />
                            <span className="gradient-text">Medical Reports</span><br />
                            Instantly
                        </h1>
                        <p style={{ fontSize: '1.15rem', color: 'var(--text-secondary)', maxWidth: 540, marginBottom: 36, lineHeight: 1.8 }}>
                            RAGnosis uses cutting-edge BERT, BART, and RAG technology to transform complex medical reports into clear, actionable insights. Empower yourself with AI-driven health intelligence.
                        </p>
                        <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', alignItems: 'center' }}>
                            <Link to="/register" className="btn-primary" style={{ fontSize: '1rem', padding: '14px 32px' }}>
                                🚀 Start Free Analysis
                            </Link>
                            <Link to="/system" className="btn-secondary" style={{ fontSize: '1rem', padding: '14px 32px' }}>
                                ⚡ See How It Works
                            </Link>
                        </div>
                        <div style={{ display: 'flex', gap: 32, marginTop: 48 }}>
                            {[['10K+', 'Reports Analyzed'], ['98%', 'Accuracy Rate'], ['5s', 'Average Process Time']].map(([val, lab]) => (
                                <div key={lab}>
                                    <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>{val}</div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 2 }}>{lab}</div>
                                </div>
                            ))}
                        </div>
                    </motion.div>

                    {/* Floating report card mockup */}
                    <motion.div
                        animate={{ y: [0, -12, 0] }}
                        transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                        style={{
                            position: 'absolute', right: '5%', top: '50%', transform: 'translateY(-50%)',
                            background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 24,
                            padding: 24, width: 300, display: 'none'
                        }}
                        className="hero-card-desktop"
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
                            <div style={{ width: 32, height: 32, background: 'var(--gradient-cyan)', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.9rem' }}>🩺</div>
                            <div>
                                <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>Blood Report</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>AI Summary Ready</div>
                            </div>
                        </div>
                        {[['Hemoglobin', '13.5 g/dL', 'normal'], ['Glucose', '105 mg/dL', 'high'], ['Cholesterol', '178 mg/dL', 'normal']].map(([n, v, s]) => (
                            <div key={n} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: '0.85rem' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>{n}</span>
                                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                                    <span style={{ fontWeight: 600 }}>{v}</span>
                                    <span className={`badge badge-${s === 'normal' ? 'green' : 'red'}`} style={{ padding: '2px 8px', fontSize: '0.65rem' }}>{s}</span>
                                </div>
                            </div>
                        ))}
                    </motion.div>
                </div>
            </section>

            {/* Features */}
            <section style={{ padding: '80px 0', background: 'var(--bg-secondary)' }}>
                <div className="container">
                    <div style={{ textAlign: 'center', marginBottom: 56 }}>
                        <div className="badge badge-purple" style={{ marginBottom: 16 }}>✨ Features</div>
                        <h2 className="section-title">Everything You Need<br /><span className="gradient-text">In One Place</span></h2>
                    </div>
                    <motion.div
                        variants={containerVariants}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true, amount: 0.2 }}
                        style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}
                    >
                        {features.map((f) => (
                            <motion.div key={f.title} variants={itemVariants} className="card" style={{ cursor: 'default' }}>
                                <div style={{ fontSize: '2rem', marginBottom: 12 }}>{f.icon}</div>
                                <h3 style={{ fontWeight: 700, marginBottom: 8 }}>{f.title}</h3>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>{f.desc}</p>
                            </motion.div>
                        ))}
                    </motion.div>
                </div>
            </section>

            {/* How it works */}
            <section style={{ padding: '80px 0' }}>
                <div className="container">
                    <div style={{ textAlign: 'center', marginBottom: 56 }}>
                        <div className="badge badge-cyan" style={{ marginBottom: 16 }}>🔬 Process</div>
                        <h2 className="section-title">From Report to<br /><span className="gradient-text">Insight in 4 Steps</span></h2>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 24 }}>
                        {steps.map((s, i) => (
                            <motion.div key={s.num}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.15 }}
                                className="card"
                                style={{ textAlign: 'center' }}
                            >
                                <div style={{ fontSize: '2.5rem', fontWeight: 900, color: 'var(--accent-cyan)', opacity: 0.4, marginBottom: 12, fontFamily: 'JetBrains Mono, monospace' }}>{s.num}</div>
                                <h3 style={{ fontWeight: 700, marginBottom: 8 }}>{s.title}</h3>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.7 }}>{s.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section style={{ padding: '80px 0', background: 'var(--bg-secondary)', textAlign: 'center' }}>
                <div className="container">
                    <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                        <h2 className="section-title" style={{ marginBottom: 16 }}>Ready to Understand<br /><span className="gradient-text">Your Health?</span></h2>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: 32, maxWidth: 480, margin: '0 auto 32px' }}>
                            Join RAGnosis today. Upload your first report and get an AI-powered summary in seconds — completely free.
                        </p>
                        <Link to="/register" className="btn-primary" style={{ fontSize: '1.1rem', padding: '16px 40px' }}>
                            🩺 Start My Free Analysis
                        </Link>
                    </motion.div>
                </div>
            </section>

            {/* Footer */}
            <footer style={{ padding: '32px 0', borderTop: '1px solid var(--border)', textAlign: 'center' }}>
                <div className="container">
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                        © 2025 RAGnosis | PICT InC 2025 | Built with ❤️ by the RAGnosis team
                    </p>
                </div>
            </footer>
        </div>
    )
}
