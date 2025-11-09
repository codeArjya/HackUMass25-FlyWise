
export interface SearchParams {
  origin: string;
  destination: string;
  departureDate: string;
  returnDate: string | null;
  isRoundTrip: boolean;
}

export interface ForecastDataPoint {
  date: string;
  price: number;
  predictedPrice?: number;
  confidenceRange?: [number, number];
}

export interface FeatureImportance {
  feature: string;
  importance: number;
}

export interface PredictionResult {
  decision: 'Buy' | 'Wait';
  priceChangePercentage: number;
  confidence: number;
  forecast: ForecastDataPoint[];
  featureImportances: FeatureImportance[];
  recommendation: string;
}
