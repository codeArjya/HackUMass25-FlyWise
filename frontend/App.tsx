import React, { useState, useCallback } from 'react';
import { Header } from './components/Header';
import { SearchForm } from './components/SearchForm';
import { ForecastChart } from './components/ForecastChart';
import { DecisionCard } from './components/DecisionCard';
import { FeatureImportanceChart } from './components/FeatureImportanceChart';
import { Loader } from './components/Loader';
import { ErrorMessage } from './components/ErrorMessage';
import { getFlightPrediction } from './services/flightApi';
import type { SearchParams, PredictionResult } from './types';

const App: React.FC = () => {
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = useCallback(async (params: SearchParams) => {
    setIsLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Fetch prediction data
      const predictionData = await getFlightPrediction(params);
      setPrediction(predictionData);

    } catch (err) {
      console.error(err);
      setError('Failed to fetch flight predictions. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans">
      <Header />
      <main className="container mx-auto p-4 md:p-8">
        <div className="max-w-4xl mx-auto bg-slate-800/50 rounded-2xl shadow-2xl shadow-cyan-500/10 p-6 md:p-8 backdrop-blur-sm border border-slate-700">
          <p className="text-center text-slate-400 mb-6">
            Enter your travel details to get a price forecast and a "Buy or Wait" recommendation.
          </p>
          <SearchForm onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {isLoading && <Loader />}
        {error && <ErrorMessage message={error} />}

        {prediction && !isLoading && (
          <div className="mt-12 space-y-8">
            <DecisionCard recommendation={prediction.recommendation} isLoading={false} />

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
              <div className="lg:col-span-3 bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
                <h2 className="text-xl font-bold mb-4 text-cyan-400">Price Forecast</h2>
                <ForecastChart data={prediction.forecast} />
              </div>
              <div className="lg:col-span-2 bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
                <h2 className="text-xl font-bold mb-4 text-amber-400">Decision Factors</h2>
                <FeatureImportanceChart data={prediction.featureImportances} />
              </div>
            </div>
          </div>
        )}

        {!prediction && !isLoading && !error && (
          <div className="text-center mt-12 p-8 bg-slate-800/30 rounded-2xl max-w-2xl mx-auto border border-dashed border-slate-700">
            <h2 className="text-2xl font-bold text-slate-300">Welcome to FlyWise</h2>
            <p className="text-slate-400 mt-2">Your co-pilot for finding the best airfare deals.</p>
            <p className="text-slate-500 mt-4">Start by entering your route and dates above.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
