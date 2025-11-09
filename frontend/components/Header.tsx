
import React from 'react';

const PlaneIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 -rotate-45 text-cyan-400">
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
    </svg>
);


export const Header: React.FC = () => {
  return (
    <header className="py-6">
      <div className="container mx-auto flex items-center justify-center space-x-3">
        <PlaneIcon />
        <h1 className="text-3xl md:text-4xl font-bold tracking-tighter bg-gradient-to-r from-slate-100 to-cyan-400 text-transparent bg-clip-text">
          FlyWise
        </h1>
      </div>
    </header>
  );
};
