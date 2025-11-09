
import React from 'react';

interface DecisionCardProps {
  recommendation: string;
  isLoading: boolean;
}

const LoadingDots: React.FC = () => (
    <div className="flex space-x-1">
        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
    </div>
);

export const DecisionCard: React.FC<DecisionCardProps> = ({ recommendation, isLoading }) => {
  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 text-center border border-slate-700 shadow-lg">
      <h2 className="text-sm font-bold uppercase tracking-widest text-cyan-400 mb-2">AI Recommendation</h2>
      <div className="text-2xl md:text-3xl font-semibold text-slate-100 min-h-[40px] flex items-center justify-center">
        {isLoading ? <LoadingDots /> : recommendation}
      </div>
    </div>
  );
};
