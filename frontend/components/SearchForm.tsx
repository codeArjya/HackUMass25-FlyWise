
import React, { useState } from 'react';
import type { SearchParams } from '../types';

interface SearchFormProps {
  onSearch: (params: SearchParams) => void;
  isLoading: boolean;
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  const [origin, setOrigin] = useState('JFK');
  const [destination, setDestination] = useState('LAX');
  const [departureDate, setDepartureDate] = useState(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]);
  const [returnDate, setReturnDate] = useState(new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]);
  const [isRoundTrip, setIsRoundTrip] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      origin,
      destination,
      departureDate,
      returnDate: isRoundTrip ? returnDate : null,
      isRoundTrip,
    });
  };

  const commonInputStyles = "w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition";

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="origin" className="block text-sm font-medium text-slate-400 mb-1">Origin</label>
          <input type="text" id="origin" value={origin} onChange={(e) => setOrigin(e.target.value)} className={commonInputStyles} required />
        </div>
        <div>
          <label htmlFor="destination" className="block text-sm font-medium text-slate-400 mb-1">Destination</label>
          <input type="text" id="destination" value={destination} onChange={(e) => setDestination(e.target.value)} className={commonInputStyles} required />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="departure" className="block text-sm font-medium text-slate-400 mb-1">Departure</label>
          <input type="date" id="departure" value={departureDate} min={new Date().toISOString().split('T')[0]} onChange={(e) => setDepartureDate(e.target.value)} className={commonInputStyles} required />
        </div>
        <div>
          <label htmlFor="return" className="block text-sm font-medium text-slate-400 mb-1">Return</label>
          <input type="date" id="return" value={returnDate} min={departureDate} onChange={(e) => setReturnDate(e.target.value)} className={commonInputStyles} disabled={!isRoundTrip} required={isRoundTrip} />
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="flex items-center">
            <input
            id="roundtrip"
            name="roundtrip"
            type="checkbox"
            checked={isRoundTrip}
            onChange={(e) => setIsRoundTrip(e.target.checked)}
            className="h-4 w-4 rounded border-slate-500 bg-slate-700 text-cyan-600 focus:ring-cyan-500"
            />
            <label htmlFor="roundtrip" className="ml-2 block text-sm text-slate-300">
            Round Trip
            </label>
        </div>
        <button type="submit" disabled={isLoading} className="inline-flex items-center justify-center px-6 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-cyan-600 hover:bg-cyan-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 focus:ring-offset-slate-800 disabled:bg-slate-600 disabled:cursor-not-allowed transition">
          {isLoading ? 'Analyzing...' : 'Get Forecast'}
        </button>
      </div>

    </form>
  );
};
