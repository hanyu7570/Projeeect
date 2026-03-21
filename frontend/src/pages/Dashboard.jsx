import React from 'react';

export default function Dashboard() {
  return (
    <div className="flex flex-col gap-4 h-full">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col items-center justify-center flex-1">
        <h2 className="text-xl font-bold text-slate-700">Dashboard Area</h2>
        <p className="text-slate-500 mt-2">Data visualizations and charts will go here.</p>
      </div>
    </div>
  );
}
