import { useEffect, useState } from "react";
import { api, ScoringLegend } from "../lib/api";

const BAND_COLOR: Record<string, string> = {
  "Strongly Positive": "#79cf9a",
  Positive: "#a8d98f",
  "Neutral / Mixed": "#9397ab",
  Negative: "#e0a08f",
  "Strongly Negative": "#e0768f",
};

export default function ScoreLegend() {
  const [legend, setLegend] = useState<ScoringLegend | null>(null);

  useEffect(() => {
    api.scoringLegend().then(setLegend).catch(() => {});
  }, []);

  if (!legend) return null;

  return (
    <div className="glass rounded-xl px-4 py-3">
      <p className="text-[10px] font-mono uppercase tracking-wide text-[#75798c] mb-2">
        Score legend — always shown, never buried
      </p>
      <div className="flex flex-wrap gap-3 text-xs">
        {legend.bands.map((b) => (
          <span key={b.label} className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full" style={{ background: BAND_COLOR[b.label] }} />
            <span className="text-[#cfd3e5]">{b.label}</span>
            <span className="text-[#75798c] font-mono">
              ({b.min > 0 ? "+" : ""}
              {b.min} to {b.max > 0 ? "+" : ""}
              {b.max})
            </span>
          </span>
        ))}
      </div>
      <p className="text-[10px] text-[#75798c] mt-2">
        Confidence: High ({legend.confidence_thresholds.high.toLocaleString()}+ mentions) · Medium (
        {legend.confidence_thresholds.medium.toLocaleString()}–
        {(legend.confidence_thresholds.high - 1).toLocaleString()}) · Low (below{" "}
        {legend.confidence_thresholds.medium.toLocaleString()}, shown plainly rather than hidden)
      </p>
    </div>
  );
}
