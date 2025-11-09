import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, ComposedChart } from 'recharts';
import type { ForecastDataPoint } from '../types';

interface ForecastChartProps {
  data: ForecastDataPoint[];
}

const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

export const ForecastChart: React.FC<ForecastChartProps> = ({ data }) => {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <ComposedChart
          data={data}
          margin={{
            top: 5,
            right: 20,
            left: -10,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" tickFormatter={formatDate} stroke="#94a3b8" tick={{ fontSize: 12 }} />
          <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} unit="$" />
          <Tooltip 
            contentStyle={{ 
                backgroundColor: '#1e293b', 
                borderColor: '#334155',
                borderRadius: '0.5rem'
            }} 
            labelStyle={{ color: '#cbd5e1' }}
            itemStyle={{ fontWeight: 'bold' }}
           />
          <Legend wrapperStyle={{fontSize: "14px"}} />
          
          {/* FIX: The `stroke` prop for the Area component expects a string, not a boolean. Changed from `false` to `"none"`. */}
          <Area type="monotone" dataKey="confidenceRange" stroke="none" fill="#06b6d4" fillOpacity={0.2} name="Confidence" />
          
          <Line type="monotone" dataKey="price" stroke="#64748b" strokeWidth={2} dot={false} name="Historical Price" />

          <Line type="monotone" dataKey="predictedPrice" stroke="#2dd4bf" strokeWidth={2} strokeDasharray="5 5" name="Predicted Price" />
          
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};