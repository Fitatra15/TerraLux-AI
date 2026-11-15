import React, { useState } from 'react';
import { X, Upload, Camera, AlertTriangle, CheckCircle2, ShieldCheck, Cpu } from 'lucide-react';
import { apiClient } from '../api/client';

export default function LeafDiagnoseModal({ parcelId, onClose }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleDiagnose = async () => {
    setLoading(true);
    setError(null);

    const formData = new FormData();
    if (selectedFile) {
      formData.append('file', selectedFile);
    }

    try {
      const res = await apiClient.post(`/parcels/${parcelId}/diagnose`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (err) {
      setError("Échec de l'analyse foliaire. Veuillez vérifier le fichier.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl border border-gray-200 animate-in fade-in zoom-in-95 duration-150">
        
        {/* Header */}
        <div className="bg-forest text-white p-5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-forest-light flex items-center justify-center text-accent">
              <Camera className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-base text-sand">Diagnostic Foliaire Multimodal</h3>
              <p className="text-xs text-sand/80">Vision IA (DINOv2) + Fusion Contexte Climat & Sol</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5">

          {/* Upload Area */}
          <div className="border-2 border-dashed border-gray-300 hover:border-forest rounded-xl p-4 text-center cursor-pointer relative bg-gray-50/50 transition-colors">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
            />
            {preview ? (
              <div className="flex flex-col items-center gap-2">
                <img src={preview} alt="Aperçu feuille" className="h-44 w-auto rounded-lg object-cover shadow-sm border border-gray-200" />
                <p className="text-xs text-gray-500">Cliquez pour remplacer la photo</p>
              </div>
            ) : (
              <div className="py-6 flex flex-col items-center gap-2 text-gray-500">
                <Upload className="w-10 h-10 text-forest/60 mb-1" />
                <p className="text-sm font-semibold text-gray-700">Sélectionnez une photo de feuille malade</p>
                <p className="text-xs text-gray-400">Formats acceptés : JPG, PNG (Mobile ou terrain)</p>
              </div>
            )}
          </div>

          {/* Submit action */}
          <div className="flex justify-end gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-xl text-xs font-semibold text-gray-700 hover:bg-gray-50"
            >
              Fermer
            </button>
            <button
              onClick={handleDiagnose}
              disabled={loading}
              className="px-5 py-2 bg-accent hover:bg-accent-dark disabled:opacity-50 text-white rounded-xl text-xs font-semibold flex items-center gap-2 shadow-sm"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Fusion multimodale en cours...</span>
                </>
              ) : (
                <>
                  <Cpu className="w-4 h-4" />
                  <span>Lancer le diagnostic</span>
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="p-3 bg-red-50 text-red-700 text-xs rounded-xl flex items-center gap-2 border border-red-200">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Result Block: Double Confidence Display */}
          {result && (
            <div className="p-4 bg-emerald-50/60 border border-emerald-200 rounded-xl space-y-4 animate-in fade-in duration-200">
              
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">
                    Diagnostic Final Confirmé
                  </span>
                  <h4 className="font-bold text-gray-900 text-base mt-1">
                    {result.final_diagnosis}
                  </h4>
                </div>
                <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0" />
              </div>

              {/* Double Confidence Bars */}
              <div className="grid grid-cols-2 gap-3 pt-2">
                <div className="bg-white p-3 rounded-lg border border-emerald-100 shadow-xs">
                  <span className="text-[11px] text-gray-500 font-medium block">Confiance Image (ML)</span>
                  <div className="flex items-baseline gap-1 mt-0.5">
                    <span className="text-xl font-bold text-gray-800 font-mono">
                      {Math.round(result.image_confidence * 100)}%
                    </span>
                    <span className="text-[10px] text-gray-400">DINOv2 gelé</span>
                  </div>
                  <div className="w-full bg-gray-100 h-1.5 rounded-full mt-2 overflow-hidden">
                    <div
                      className="bg-accent h-full rounded-full"
                      style={{ width: `${result.image_confidence * 100}%` }}
                    />
                  </div>
                </div>

                <div className="bg-white p-3 rounded-lg border border-emerald-200 shadow-xs">
                  <span className="text-[11px] text-emerald-800 font-semibold flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Confiance Contextuelle</span>
                  </span>
                  <div className="flex items-baseline gap-1 mt-0.5">
                    <span className="text-xl font-bold text-emerald-700 font-mono">
                      {Math.round(result.contextual_confidence * 100)}%
                    </span>
                    <span className="text-[10px] text-emerald-600 font-medium">Climat + Sol</span>
                  </div>
                  <div className="w-full bg-gray-100 h-1.5 rounded-full mt-2 overflow-hidden">
                    <div
                      className="bg-emerald-600 h-full rounded-full"
                      style={{ width: `${result.contextual_confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Plausibility Breakdown */}
              <div className="text-[11px] bg-white/80 p-2.5 rounded-lg border border-emerald-100 flex justify-between text-gray-600">
                <span>Plausibilité climatique : <strong>{Math.round(result.climate_plausibility * 100)}%</strong></span>
                <span>Plausibilité pédologique : <strong>{Math.round(result.soil_plausibility * 100)}%</strong></span>
              </div>

              {/* Justification Text */}
              <p className="text-xs text-gray-700 leading-relaxed bg-white p-3 rounded-lg border border-emerald-100">
                💡 <strong>Explication scientifique :</strong> {result.explanation}
              </p>

              {result.warning && (
                <div className="p-2.5 bg-amber-50 text-amber-800 text-xs rounded-lg flex items-center gap-2 border border-amber-200">
                  <AlertTriangle className="w-4 h-4 shrink-0 text-amber-600" />
                  <span>{result.warning}</span>
                </div>
              )}

            </div>
          )}

        </div>

      </div>
    </div>
  );
}
