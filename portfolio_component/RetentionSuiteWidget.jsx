import React, { useState, useRef, useEffect } from 'react';

/**
 * E-Commerce Customer Retention & Churn Diagnostic Suite
 * Production React + Tailwind CSS Portfolio Integration Component
 */
export default function RetentionSuiteWidget() {
  const [activeBiSource, setActiveBiSource] = useState('tableau'); // 'tableau' | 'powerbi'
  const [isLoading, setIsLoading] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const containerRef = useRef(null);

  // Embed URLs (replace with verified public links)
  const reportUrls = {
    tableau: "https://public.tableau.com/views/Superstore_24/Overview?:showVizHome=no&:embed=true",
    powerbi: "https://app.powerbi.com/view?r=eyJrIjoi..."
  };

  const handleFullscreenToggle = () => {
    if (!document.fullscreenElement && containerRef.current) {
      if (containerRef.current.requestFullscreen) {
        containerRef.current.requestFullscreen();
      }
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    const handleFsChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFsChange);
    return () => document.removeEventListener('fullscreenchange', handleFsChange);
  }, []);

  return (
    <section className="w-full max-w-7xl mx-auto px-4 py-8 font-sans text-slate-100 bg-slate-950 rounded-2xl border border-slate-800 shadow-2xl my-8">
      
      {/* ----------------------------------------------------------------- */}
      {/* 1. PROJECT HEADER & BADGES */}
      {/* ----------------------------------------------------------------- */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wider text-blue-400 bg-blue-950/80 border border-blue-800/60 rounded-full">
              Enterprise Portfolio Case Study
            </span>
            <span className="px-2.5 py-0.5 text-xs font-medium text-emerald-400 bg-emerald-950/80 border border-emerald-800/60 rounded-full flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              Live Diagnostic Model
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
            E-Commerce Customer Retention & Churn Diagnostic Suite
          </h2>
          <p className="text-sm md:text-base text-slate-400 mt-1 max-w-3xl">
            Longitudinal cohort analysis, promotional elasticity diagnostics, and predictive churn modeling across <strong>96,211 transactions</strong> and <strong>93,104 customers</strong>.
          </p>
        </div>

        {/* Action CTAs */}
        <div className="flex items-center gap-3">
          <a
            href="./case_study_summary.md"
            download="Retention_Churn_Diagnostic_Case_Study.md"
            className="px-4 py-2 text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-lg transition-colors flex items-center gap-2 shadow-sm"
          >
            <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            Case Study (PDF)
          </a>
          <a
            href="https://share.streamlit.io"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors flex items-center gap-2 shadow-md shadow-blue-900/30"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
            Launch Python App
          </a>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* 2. EXECUTIVE METRIC SUMMARY CARDS */}
      {/* ----------------------------------------------------------------- */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 my-6">
        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">Active Retention</span>
          <div className="text-2xl font-bold text-sky-400 mt-1">19.4%</div>
          <p className="text-xs text-slate-500 mt-0.5">18,073 Active Retained Customers</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">Recovery Opportunity</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1">$1.33M</div>
          <p className="text-xs text-emerald-500/80 mt-0.5 font-medium">+12.8% Churn Attrition Target</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">Average Customer LTV</span>
          <div className="text-2xl font-bold text-purple-400 mt-1">$138.35</div>
          <p className="text-xs text-slate-500 mt-0.5">3.8x Value Multiplier on 2nd Order</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">Predictive Churn AUC</span>
          <div className="text-2xl font-bold text-amber-400 mt-1">0.976</div>
          <p className="text-xs text-slate-500 mt-0.5">Supervised Random Forest Classifier</p>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* 3. EMBEDDED DASHBOARD VIEWER (1200x800 Fixed Aspect Ratio) */}
      {/* ----------------------------------------------------------------- */}
      <div className="my-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-3">
          <div className="flex items-center gap-2">
            <h3 className="text-base font-semibold text-slate-200">
              Interactive Executive BI Dashboard
            </h3>
            <span className="text-xs text-slate-500">(Fixed 1200x800 Embedded Container)</span>
          </div>

          <div className="flex items-center gap-2">
            {/* Source Switcher */}
            <div className="inline-flex rounded-lg bg-slate-900 p-0.5 border border-slate-800">
              <button
                onClick={() => { setActiveBiSource('tableau'); setIsLoading(true); }}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
                  activeBiSource === 'tableau'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Tableau Public
              </button>
              <button
                onClick={() => { setActiveBiSource('powerbi'); setIsLoading(true); }}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
                  activeBiSource === 'powerbi'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Power BI
              </button>
            </div>

            {/* Fullscreen Button */}
            <button
              onClick={handleFullscreenToggle}
              className="p-1.5 text-slate-400 hover:text-white bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-lg transition-colors"
              title="Toggle Fullscreen"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/>
              </svg>
            </button>
          </div>
        </div>

        {/* 1200x800 Aspect-Ratio Container */}
        <div
          ref={containerRef}
          className={`relative w-full rounded-xl overflow-hidden bg-slate-900 border border-slate-800 shadow-inner ${
            isFullscreen ? 'fixed inset-0 z-50 rounded-none w-screen h-screen' : 'aspect-[1200/800] max-w-[1200px] mx-auto'
          }`}
        >
          {/* Loading Spinner */}
          {isLoading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/85 backdrop-blur-sm z-20">
              <div className="w-10 h-10 border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin"></div>
              <p className="text-xs font-medium text-slate-300 mt-3">Loading {activeBiSource === 'tableau' ? 'Tableau Public' : 'Power BI'} Engine...</p>
            </div>
          )}

          {/* Iframe */}
          <iframe
            key={activeBiSource}
            title="E-Commerce Retention Dashboard"
            src={reportUrls[activeBiSource]}
            className="w-full h-full border-0 absolute inset-0 z-10"
            allowFullScreen
            loading="lazy"
            onLoad={() => setIsLoading(false)}
          />
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* 4. PYTHON INTERACTIVE APP ("CHAT WITH DATA") PROMO CARD */}
      {/* ----------------------------------------------------------------- */}
      <div className="my-8 p-6 bg-gradient-to-r from-slate-900 via-slate-900/90 to-blue-950/30 rounded-xl border border-blue-900/40 relative overflow-hidden">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 relative z-10">
          <div className="max-w-2xl">
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-full bg-blue-400"></span>
              <span className="text-xs font-semibold uppercase tracking-wider text-blue-400">
                Interactive Conversational Analytics
              </span>
            </div>
            <h4 className="text-xl font-bold text-white">
              "Chat with your Retention Data" Streamlit Interface
            </h4>
            <p className="text-sm text-slate-300 mt-1">
              Ask questions in plain English like <em>"Plot discount sensitivity curves"</em> or <em>"Show top churn drivers"</em>. 
              The engine automatically runs SQL/Pandas analytics and renders dynamic Plotly heatmaps and elasticity curves.
            </p>
            <div className="flex flex-wrap gap-2 mt-4">
              <span className="px-2.5 py-1 text-xs bg-slate-800 text-slate-300 rounded-md border border-slate-700">Python 3.11</span>
              <span className="px-2.5 py-1 text-xs bg-slate-800 text-slate-300 rounded-md border border-slate-700">Streamlit</span>
              <span className="px-2.5 py-1 text-xs bg-slate-800 text-slate-300 rounded-md border border-slate-700">Plotly</span>
              <span className="px-2.5 py-1 text-xs bg-slate-800 text-slate-300 rounded-md border border-slate-700">LangChain / NLP Router</span>
              <span className="px-2.5 py-1 text-xs bg-slate-800 text-slate-300 rounded-md border border-slate-700">Random Forest (0.976 AUC)</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
            <a
              href="https://share.streamlit.io"
              target="_blank"
              rel="noopener noreferrer"
              className="px-5 py-3 text-xs font-bold uppercase tracking-wider text-center bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all shadow-lg shadow-blue-900/40 flex items-center justify-center gap-2"
            >
              Open Live Streamlit App
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
              </svg>
            </a>
          </div>
        </div>
      </div>

    </section>
  );
}
