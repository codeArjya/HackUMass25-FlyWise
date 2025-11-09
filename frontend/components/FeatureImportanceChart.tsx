
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import type { FeatureImportance } from '../types';

interface FeatureImportanceChartProps {
  data: FeatureImportance[];
}

export const FeatureImportanceChart: React.FC<FeatureImportanceChartProps> = ({ data }) => {
  const sortedData = [...data].sort((a, b) => a.importance - b.importance);

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart layout="vertical" data={sortedData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <XAxis type="number" hide />
          <YAxis 
            dataKey="feature" 
            type="category" 
            axisLine={false} 
            tickLine={false} 
            stroke="#94a3b8" 
            tick={{ fontSize: 12, textAnchor: 'start' }} 
            dx={5} 
          />
          <Tooltip 
            cursor={{ fill: '#334155' }}
            contentStyle={{ 
                backgroundColor: '#1e293b', 
                borderColor: '#334155',
                borderRadius: '0.5rem'
            }} 
            labelStyle={{ color: '#cbd5e1' }}
            formatter={(value: number) => [value.toFixed(2), 'Importance']}
          />
          <Bar dataKey="importance" fill="#f59e0b" background={{ fill: '#33415550', radius: 4}} radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
