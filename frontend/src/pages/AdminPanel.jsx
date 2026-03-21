import React from 'react';
import { Shield } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function AdminPanel() {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col h-screen bg-slate-100 font-sans">
      <header className="bg-white border-b border-slate-200 h-16 flex items-center justify-between px-6 flex-shrink-0 z-20 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-1.5 rounded-lg"><Shield className="w-5 h-5 text-white" /></div>
          <span className="text-xl font-bold text-slate-800 tracking-tight">GSInspect <span className="text-indigo-600 font-normal">Admin</span></span>
        </div>
        <button onClick={() => navigate('/dashboard')} className="text-sm font-medium text-slate-600 hover:text-slate-900 border border-slate-300 px-4 py-2 rounded-lg hover:bg-slate-50 transition-colors">
          Return to Dashboard
        </button>
      </header>
      <div className="flex flex-1 items-center justify-center">
        <h2 className="text-2xl font-bold text-slate-400">Admin Panel</h2>
      </div>
    </div>
  );
}
