'use client';

import React from 'react';
// import Image from 'next/image';
import { Unlock, UserCog, Zap, Rocket, Plus, Settings, MessageCircle, Github } from 'lucide-react';
import Section from './components/Section';
import useParallax from './components/useParallax';
// import Waves from './components/Waves';
const steps = [
  { label: '1', desc: 'Add Telefy to your Telegram group or chat.' },
  { label: '2', desc: 'Configure the personality of your agent.' },
  { label: '3', desc: 'Interact with the agent. No filter, no limits.' },
];

const cards = [
  { title: 'Uncensored Responses', desc: 'Telefy answers any question, no filter, no restrictions.', icon: Unlock },
  { title: 'Custom Personalities', desc: 'Set a unique personality for each group or chat.', icon: UserCog },
  { title: 'Solana Token Utility', desc: 'Use $TELEFY for dedicated agents, custom actions, and more.', icon: Zap },
  { title: 'Dedicated Agents', desc: 'Dedicated agents have real-time, live data with no/very high rate limits. The public agent has live data but is rate limited.', icon: Rocket },
];

const icons = {
  twitter: (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M22.46 5.924c-.793.352-1.645.59-2.54.698a4.48 4.48 0 0 0 1.963-2.475 8.94 8.94 0 0 1-2.828 1.082A4.48 4.48 0 0 0 16.11 4c-2.485 0-4.5 2.015-4.5 4.5 0 .353.04.697.116 1.027C7.728 9.37 4.1 7.6 1.67 4.905a4.48 4.48 0 0 0-.61 2.264c0 1.563.796 2.942 2.008 3.75a4.48 4.48 0 0 1-2.037-.563v.057c0 2.183 1.553 4.006 3.617 4.422a4.48 4.48 0 0 1-2.03.077c.573 1.788 2.236 3.09 4.205 3.125A8.98 8.98 0 0 1 2 19.54a12.68 12.68 0 0 0 6.88 2.017c8.26 0 12.78-6.84 12.78-12.78 0-.195-.004-.39-.013-.583A9.14 9.14 0 0 0 24 4.59a8.94 8.94 0 0 1-2.54.698z" fill="#1DA1F2"/></svg>
  ),
  telegram: (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.036 16.569l-.398 3.77c.57 0 .816-.246 1.113-.543l2.67-2.56 5.537 4.04c1.013.558 1.73.264 1.99-.936l3.61-16.84c.33-1.53-.553-2.13-1.54-1.76L2.36 9.47c-1.48.58-1.46 1.41-.25 1.78l4.6 1.44 10.68-6.74c.5-.32.96-.14.58.2" fill="#229ED9"/></svg>
  ),
  info: (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="10" stroke="#6366F1" strokeWidth="2" fill="none"/><rect x="11" y="10" width="2" height="6" rx="1" fill="#6366F1"/><rect x="11" y="7" width="2" height="2" rx="1" fill="#6366F1"/></svg>
  ),
};

const HomePage = () => {
  const heroBlobParallax = useParallax(0.7);
  const heroHeadlineParallax = useParallax(-0.15);
  const stepsBlobParallax = useParallax(0.5);
  const stepsHeadingParallax = useParallax(-0.12);
  // Parallax for Why Telefy section
  const whyBlobParallax = useParallax(0.2);
  const whyHeadingParallax = useParallax(-0.065);
  // Parallax for Footer section
  const footerBlobParallax = useParallax(0.17);
  const footerHeadingParallax = useParallax(-0.055);
  // Parallax for main content of each section
  const stepsContentParallax = useParallax(0.09);
  const whyContentParallax = useParallax(-0.07);
  const footerContentParallax = useParallax(0.05);
  // Parallax for Build with Telefy section
  const buildBlobParallax = useParallax(0.18);
  const buildHeadingParallax = useParallax(-0.07);
  const buildContentParallax = useParallax(0.06);
  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-x-hidden bg-gray-100">
      {/* <Waves backgroundColor="black" lineColor="#e0e7ff" /> */}
      <div className="fixed inset-0 z-[-1] w-full h-full" /> 
      
      <div className="w-full max-w-6xl md:my-10 rounded-[2.5rem] shadow-2xl backdrop-blur-2xl border border-white/30 p-2 md:p-8 flex flex-col min-h-[96vh] bg-gradient-to-br from-[#e0e7ff] via-[#f1f5f9] to-[#f0fdfa]" style={{background: 'linear-gradient(135deg, #e0e7ff 0%, #f1f5f9 50%, #f0fdfa 100%)'}}>
        {/* Static Navbar */}
      <header className="w-full flex items-center justify-center z-40">
        <nav className="w-full max-w-xl mx-auto rounded-2xl bg-gray-100 backdrop-blur-md border border-white/30 shadow-lg flex items-center justify-between px-4 py-2 md:py-3 transition-all duration-300">
          <div className="flex items-center gap-2">
            <img src="/images/pngs/logo_png_5.png" alt="Telefy Logo" className="w-8 h-8 rounded-full object-contain" />
            <span className="font-bold text-xl md:text-2xl text-gray-800">Telefy</span>
          </div>
          <button className="bg-cyan-400 hover:bg-cyan-500 text-white font-semibold rounded-full px-6 py-2 shadow-md focus:outline-none focus:ring-2 focus:ring-cyan-300 transition ml-4" tabIndex={0} aria-label="Deploy Agent">Deploy Agent</button>
        </nav>
      </header>
        {/* Hero Section */}
        <Section className="relative flex flex-col items-center justify-center text-center py-16 md:py-28">
          {/* Blurred gradient blob */}
          <div
            className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/4 w-[480px] h-[320px] bg-gradient-to-tr from-[#e0e7ff] via-[#a5b4fc] to-[#f0fdfa] opacity-60 blur-3xl rounded-full z-0 pointer-events-none select-none"
            ref={heroBlobParallax.ref}
            style={heroBlobParallax.style}
          />
          <div className="relative z-10 flex flex-col items-center animate-fade-in-up">
            <h1
              className="text-4xl md:text-7xl font-extrabold text-gray-900 mb-6 leading-tight"
              ref={heroHeadlineParallax.ref}
              style={heroHeadlineParallax.style}
            >
              <span className="">Telefy, </span>
              <span className="bg-gradient-to-r from-[#00ffa3] to-[#9945FF] bg-clip-text text-transparent">Uncensored</span>
              <span className=""> Telegram AI Agent</span>
            </h1>
            <p className="max-w-2xl text-base md:text-lg text-gray-700 mb-10">With Telefy, each agent is tailored to understand the unique dynamics of your group, providing personalized and intelligent interactions. No filter, no limits—just pure, honest answers and total control. Dedicated agents, custom personalities.</p>
          </div>
        </Section>
        {/* Steps Section */}
        <Section className="w-full flex flex-col items-center py-8 relative">
          {/* Parallax background blob for steps section */}
          <div
            className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/3 w-[340px] h-[220px] bg-gradient-to-tr from-[#a5b4fc] via-[#e0e7ff] to-[#f0fdfa] opacity-50 blur-2xl rounded-full z-0 pointer-events-none select-none"
            ref={stepsBlobParallax.ref}
            style={stepsBlobParallax.style}
          />
          <h2
            className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-600 bg-clip-text text-transparent drop-shadow-lg mb-2 relative z-10 leading-tight pb-1"
            ref={stepsHeadingParallax.ref}
            style={stepsHeadingParallax.style}
          >
            How Telefy Works
          </h2>
          <p className="text-gray-700 max-w-2xl text-center mb-8 relative z-10">Get started in seconds. Telefy is the first fully uncensored, personality-driven Telegram AI agent. No filter, no limits—just pure, honest answers and total control.</p>
          <div className="relative w-full max-w-md mx-auto flex flex-col items-center z-10" ref={stepsContentParallax.ref} style={stepsContentParallax.style}>
            {steps.map((step, idx) => (
              <div
                key={idx}
                className="relative flex items-start w-full group focus-within:ring-2 focus-within:ring-cyan-400 mb-8 last:mb-0 transition-transform duration-500"
                tabIndex={0}
                aria-label={`Step ${step.label}: ${step.desc}`}
              >
                {/* Timeline Line */}
                {idx !== steps.length - 1 && (
                  <span className="absolute left-6 top-10 w-0.5 h-full bg-cyan-200 z-0" aria-hidden="true" />
                )}
                {/* Icon Circle */}
                <span className="flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-cyan-400 to-purple-400 text-white font-bold text-2xl shadow-lg z-10 mr-4 animate-fade-in-up">
                  {idx === 0 && <Plus size={28} aria-label="Add to Telegram" />}
                  {idx === 1 && <Settings size={28} aria-label="Configure Personality" />}
                  {idx === 2 && <MessageCircle size={28} aria-label="Chat" />}
                </span>
                {/* Step Content */}
                <div className="flex flex-col">
                  <span className="text-lg font-semibold text-gray-900 mb-1">Step {step.label}</span>
                  <span className="text-gray-700 text-base">{step.desc}</span>
                </div>
              </div>
            ))}
          </div>
        </Section>
        {/* Cards Section */}
        <Section className="w-full flex flex-col items-center py-8 relative mt-40">
          {/* Parallax background blob for Why Telefy section */}
          <div
            className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/3 w-[340px] h-[220px] bg-gradient-to-tr from-[#f0fdfa] via-[#a5b4fc] to-[#e0e7ff] opacity-50 blur-2xl rounded-full z-0 pointer-events-none select-none"
            ref={whyBlobParallax.ref}
            style={whyBlobParallax.style}
          />
          <h2
            className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-purple-500 via-cyan-400 to-purple-600 bg-clip-text text-transparent drop-shadow-lg relative z-10 leading-tight pb-1"
            ref={whyHeadingParallax.ref}
            style={whyHeadingParallax.style}
          >
            Uncensored. Custom. Uniquely Yours.
          </h2>
          <p className="text-gray-700 max-w-2xl text-center mb-8 relative z-10">Telefy is more than just an AI bot. It&apos;s your group&apos;s own, fully unlocked agent—customizable, fast, and powered by the $TELEFY token for premium features and speed.</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl animate-fade-in-up relative z-10" ref={whyContentParallax.ref} style={whyContentParallax.style}>
            {cards.map((card, idx) => {
              const Icon = card.icon;
              return (
                <div
                  key={idx}
                  className="flex flex-col items-center bg-white rounded-3xl shadow-lg p-8 min-h-[220px] transition-transform duration-200 hover:scale-105 hover:bg-cyan-50 focus-within:scale-105 focus-within:bg-cyan-50 border border-white/40 group outline-none"
                  tabIndex={0}
                  aria-label={card.title + ': ' + card.desc}
                >
                  <span className="flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-cyan-400 to-purple-400 text-white text-3xl font-bold mb-4 shadow-lg">
                    <Icon size={36} aria-label={card.title + ' icon'} />
                  </span>
                  <span className="text-xl md:text-2xl font-extrabold text-gray-900 mb-2 text-center">{card.title}</span>
                  <span className="text-base text-gray-700 text-center">{card.desc}</span>
                </div>
              );
            })}
          </div>
        </Section>
        {/* Build with Telefy Section */}
        <Section className="w-full flex flex-col items-center py-16 relative mt-40">
          {/* Parallax background blob for build section */}
          <div
            className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/3 w-[340px] h-[220px] bg-gradient-to-tr from-[#e0e7ff] via-[#a5b4fc] to-[#f0fdfa] opacity-50 blur-2xl rounded-full z-0 pointer-events-none select-none"
            ref={buildBlobParallax.ref}
            style={buildBlobParallax.style}
          />
          <h2
            className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-600 bg-clip-text text-transparent drop-shadow-lg relative z-10 leading-tight pb-1"
            ref={buildHeadingParallax.ref}
            style={buildHeadingParallax.style}
          >
            Build with Telefy
          </h2>
          <div className="max-w-2xl text-center mb-8 relative z-10" ref={buildContentParallax.ref} style={buildContentParallax.style}>
            <p className="text-gray-700 text-lg md:text-xl mb-6">Create your own agents, extensions, and integrations. Telefy is open-source and developer-friendly—build anything you can imagine for Telegram.</p>
            <a
              href="https://github.com/telefy/telefy"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-gray-900 hover:bg-gray-800 text-white font-semibold rounded-full px-6 py-3 shadow-lg transition focus:outline-none focus:ring-2 focus:ring-cyan-400 text-lg"
              tabIndex={0}
              aria-label="View Telefy on GitHub"
            >
              <Github size={24} />
              View on GitHub
            </a>
          </div>
        </Section>
        {/* Footer Section */}
        <Section className="w-full flex flex-col items-center py-16 relative mt-40">
          {/* Parallax background blob for footer section */}
          <div
            className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/3 w-[380px] h-[240px] bg-gradient-to-tr from-[#a5b4fc] via-[#e0e7ff] to-[#f0fdfa] opacity-50 blur-2xl rounded-full z-0 pointer-events-none select-none"
            ref={footerBlobParallax.ref}
            style={footerBlobParallax.style}
          />
          <h2
            className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-600 bg-clip-text text-transparent drop-shadow-lg relative z-10 leading-tight pb-1"
            ref={footerHeadingParallax.ref}
            style={footerHeadingParallax.style}
          >
            Ready to unlock your Telegram?
          </h2>
          <p className="text-gray-700 max-w-2xl text-center mb-6 relative z-10">Add Telefy to your group, set your agent&apos;s personality, and experience the first truly uncensored, customizable Telegram AI—powered by Solana.</p>
          <div className="flex flex-col md:flex-row gap-4 w-full max-w-3xl items-center justify-center mb-6 relative z-10" ref={footerContentParallax.ref} style={footerContentParallax.style}>
            <button className="bg-cyan-400 hover:bg-cyan-500 text-white font-semibold rounded-full px-4 py-2 shadow focus:outline-none focus:ring-2 focus:ring-cyan-300 transition mb-2 md:mb-0" tabIndex={0} aria-label="Copy contract address">Copy contract address</button>
            <span className="bg-white/80 rounded-full px-4 py-2 text-gray-700 text-sm font-mono">Contract: coming soon</span>
          </div>
          <div className="flex flex-col md:flex-row gap-6 w-full max-w-4xl items-center justify-center mb-8 relative z-10" ref={footerContentParallax.ref} style={footerContentParallax.style}>
            <div
              className="flex-1 bg-white/90 rounded-2xl shadow-lg p-6 flex flex-col items-center min-w-[180px] max-w-[240px] border border-white/40 relative transition-transform duration-200 hover:scale-105 focus-within:scale-105"
              tabIndex={0}
              aria-label="Follow us on X"
            >
              <div className="text-xl font-semibold text-gray-900 mb-2 text-center">Follow us on <span className="inline-block align-middle text-2xl font-bold">X</span></div>
              <span className="mx-auto">{icons.twitter}</span>
            </div>
            <div
              className="flex-1 bg-white/90 rounded-2xl shadow-lg p-6 flex flex-col items-center min-w-[180px] max-w-[240px] border border-white/40 relative transition-transform duration-200 hover:scale-105 focus-within:scale-105"
              tabIndex={0}
              aria-label="Join our Telegram"
            >
              <div className="text-xl font-semibold text-gray-900 mb-2 text-center">Join our Telegram</div>
              <span className="mx-auto">{icons.telegram}</span>
            </div>
            <div
              className="flex-1 bg-white/90 rounded-2xl shadow-lg p-6 flex flex-col items-center min-w-[180px] max-w-[240px] border border-white/40 relative transition-transform duration-200 hover:scale-105 focus-within:scale-105"
              tabIndex={0}
              aria-label="About / Docs"
            >
              <div className="text-xl font-semibold text-gray-900 mb-2 text-center">About / Docs</div>
              <span className="mx-auto">{icons.info}</span>
            </div>
          </div>
          <div className="w-full flex items-center justify-between px-2 mt-40 relative z-10">
            <div className="flex items-center gap-2">
              <img src="/images/pngs/logo_png_5.png" alt="Telefy Logo" className="w-6 h-6 rounded-full object-contain" />
              <span className="font-bold text-lg text-gray-800">Telefy</span>
            </div>
            <span className="text-gray-400 text-xs">Copyright 2025. Telefy.</span>
          </div>
        </Section>
      </div>
      <style>{`
        @keyframes fade-in-up {
          0% { opacity: 0; transform: translateY(32px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up {
          animation: fade-in-up 1.1s cubic-bezier(.4,0,.2,1) both;
        }
      `}</style>
    </div>
  );
};

export default HomePage;
