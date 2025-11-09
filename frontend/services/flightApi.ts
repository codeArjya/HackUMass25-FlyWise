import type { SearchParams, PredictionResult } from '../types';

export const getFlightPrediction = async (params: SearchParams): Promise<PredictionResult> => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000';

    const payload = {
        origin: params.origin,
        destination: params.destination,
        depart_date: params.departureDate,  
    };

    const res = await fetch(`${backendUrl}/api/flights/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        throw new Error(`Backend error: ${res.status}`);
    }

    const data = await res.json();
    return {
        decision: data.decision,
        confidence: data.confidence,
        forecast: data.forecast,
        recommendation: data.recommendation,
        featureImportances: data.featureImportances || [],
        priceChangePercentage: Math.round(data.forecast.at(-1).predictedPrice / data.forecast[0].predictedPrice * 100 - 100)
    };
};
