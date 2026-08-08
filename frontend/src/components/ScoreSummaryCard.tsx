import { useEffect, useState } from "react";
import { api, ScoringSummary } from "../lib/api";

const CONFIDENCE_COLOR: Record<string, string> = {
  High: "#79cf9a",
  Medium: "#e0a455",
  Low: "#e0768f",
};

export default function ScoreSummaryCard({ topicId, hue }: { topicId: string; hue: string }) {
  const [summary, setSummary] = useState<ScoringSummary | null>(null);

  useEffect(() => {
    setSummary(null);
    api.scoringSummary(topicId).then(setSummary).catch(() => {});
  }, [topicId]);

  if (!summary) return null;

  return (
    <div className="glass rounded-xl p-4 flex items-center justify-between gap-4">
      <div>
        <p className="text-[10px] font-mono uppercase tracking-wide text-[#75798c]">
          Composite score · last {summary.window_days}d
        </p>
        <p className="text-2xl font-semibold" style={{ color: hue }}>
          {summary.score_100 > 0 ? "+" : ""}
          {summary.score_100}
        </p>
        <p className="text-sm text-[#cfd3e5]">{summary.band}</p>
      </div>
      {summary.positive_share !== null && (
        <div className="flex-1 max-w-xs">
          <div className="flex h-2 rounded-full overflow-hidden">
            <div style={{ width: `${(summary.positive_share ?? 0) * 100}%`, background: "#79cf9a" }} />
            <div style={{ width: `${(summary.neutral_share ?? 0) * 100}%`, background: "#9397ab" }} />
            <div style={{ width: `${(summary.negative_share ?? 0) * 100}%`, background: "#e0768f" }} />
          </div>
          <p className="text-[10px] text-[#75798c] mt-1 font-mono">
            {Math.round((summary.positive_share ?? 0) * 100)}% pos ·{" "}
            {Math.round((summary.neutral_share ?? 0) * 100)}% neu ·{" "}
            {Math.round((summary.negative_share ?? 0) * 100)}% neg
          </p>
        </div>
      )}
      <div className="text-right">
        <span
          className="text-[11px] font-mono uppercase px-2.5 py-1 rounded-full border"
          style={{ borderColor: `${CONFIDENCE_COLOR[summary.confidence]}55`, color: CONFIDENCE_COLOR[summary.confidence] }}
        >
          {summary.confidence} confidence
        </span>
        <p className="text-[10px] text-[#75798c] mt-1">{summary.item_count.toLocaleString()} mentions</p>
      </div>
    </div>
  );
}
