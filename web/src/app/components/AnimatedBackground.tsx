import React from 'react';

const AnimatedBackground: React.FC = () => (
  <div
    className="fixed inset-0 w-screen h-screen z-0 pointer-events-none select-none"
    aria-hidden="true"
  >
    <svg
      width="100%"
      height="100%"
      viewBox="0 0 1920 1080"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-screen h-screen absolute top-0 left-0"
      preserveAspectRatio="none"
    >
      {/* Wave 1 */}
      <path
        d="M0 700 Q480 600 960 700 T1920 700 V1080 H0 Z"
        fill="url(#wave1)"
        className="animate-wave1"
      />
      {/* Wave 2 */}
      <path
        d="M0 800 Q600 900 1200 800 T1920 800 V1080 H0 Z"
        fill="url(#wave2)"
        className="animate-wave2"
      />
      {/* Wave 3 */}
      <path
        d="M0 900 Q960 1000 1920 900 V1080 H0 Z"
        fill="url(#wave3)"
        className="animate-wave3"
      />
      <defs>
        <linearGradient id="wave1" x1="0" y1="700" x2="1920" y2="1080" gradientUnits="userSpaceOnUse">
          <stop stopColor="#00ffa3" stopOpacity="0.18" />
          <stop offset="1" stopColor="#9945FF" stopOpacity="0.12" />
        </linearGradient>
        <linearGradient id="wave2" x1="0" y1="800" x2="1920" y2="1080" gradientUnits="userSpaceOnUse">
          <stop stopColor="#9945FF" stopOpacity="0.13" />
          <stop offset="1" stopColor="#00ffa3" stopOpacity="0.10" />
        </linearGradient>
        <linearGradient id="wave3" x1="0" y1="900" x2="1920" y2="1080" gradientUnits="userSpaceOnUse">
          <stop stopColor="#00ffa3" stopOpacity="0.10" />
          <stop offset="1" stopColor="#fff" stopOpacity="0.08" />
        </linearGradient>
      </defs>
    </svg>
    <style>{`
      @keyframes wave1 {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-30px); }
      }
      @keyframes wave2 {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(40px); }
      }
      @keyframes wave3 {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
      }
      .animate-wave1 { animation: wave1 10s ease-in-out infinite; }
      .animate-wave2 { animation: wave2 14s ease-in-out infinite; }
      .animate-wave3 { animation: wave3 18s ease-in-out infinite; }
    `}</style>
  </div>
);

export default AnimatedBackground; 