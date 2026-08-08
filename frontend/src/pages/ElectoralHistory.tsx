import { useEffect, useState } from "react";
import { api, ElectoralHistory as ElectoralHistoryType } from "../lib/api";

function SwingBadge({ value, unit }: { value: number | null; unit: string }) {
  if (value === null) return <span className="text-[#75798c]">—</span>;
  const color = value > 0 ? "#79cf9a" : value < 0 ? "#e0768f" : "#9397ab";
  return (
    <span style={{ color }}>
      {value > 0 ? "+" : ""}
      {value}
      {unit}
    </span>
  );
}

export default function ElectoralHistory() {
  const [data, setData] = useState<ElectoralHistoryType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .electoralHistory()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <header className="space-y-3">
        <p className="text-[11px] font-mono uppercase tracking-[0.08em] text-[#8fc7f0]">
          Electoral history · 2019 vs 2024 Lok Sabha
        </p>
        <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">Electoral History</h1>
        <p className="text-sm text-[#9ea3bb] max-w-2xl">
          Real, sourced national results and their swing between the last two Lok Sabha elections —{" "}
          <span className="text-[#e0a455]">this is historical data, not a seat projection.</span> A
          validated forecast needs constituency-level results across 3-4+ elections to backtest
          properly; two years of national totals can't support that, so none is attempted here (see
          ROADMAP.md for what a real projection would need).
        </p>
        {data && (
          <p className="text-xs text-[#75798c] max-w-2xl">
            Sources:{" "}
            <a href={data.sources["2019"]} target="_blank" rel="noreferrer" className="text-[#8fc7f0] hover:underline">
              2019 results
            </a>{" "}
            ·{" "}
            <a href={data.sources["2024"]} target="_blank" rel="noreferrer" className="text-[#8fc7f0] hover:underline">
              2024 results
            </a>
          </p>
        )}
      </header>

      {loading && <div className="text-sm text-[#75798c] py-8 text-center">Loading…</div>}

      {data && (
        <div className="glass rounded-2xl overflow-x-auto">
          <table className="w-full text-sm min-w-[640px]">
            <thead>
              <tr className="text-left text-[10px] font-mono uppercase text-[#75798c] border-b border-white/10">
                <th className="p-3">Party</th>
                <th className="p-3">2019 seats</th>
                <th className="p-3">2019 vote %</th>
                <th className="p-3">2024 seats</th>
                <th className="p-3">2024 vote %</th>
                <th className="p-3">Seat swing</th>
                <th className="p-3">Vote % swing</th>
              </tr>
            </thead>
            <tbody>
              {data.parties.map((p) => (
                <tr key={p.party_id} className="border-b border-white/5 last:border-0">
                  <td className="p-3">
                    <span style={{ color: p.hue }}>{p.party_name}</span>
                    {p.note && (
                      <span className="block text-[10px] text-[#75798c] mt-1 max-w-xs">{p.note}</span>
                    )}
                  </td>
                  <td className="p-3 font-mono">{p["2019"]?.seats ?? "—"}</td>
                  <td className="p-3 font-mono">{p["2019"]?.vote_share_pct ?? "—"}</td>
                  <td className="p-3 font-mono">{p["2024"]?.seats ?? "—"}</td>
                  <td className="p-3 font-mono">{p["2024"]?.vote_share_pct ?? "—"}</td>
                  <td className="p-3 font-mono">
                    <SwingBadge value={p.seat_swing} unit="" />
                  </td>
                  <td className="p-3 font-mono">
                    <SwingBadge value={p.vote_share_swing} unit="pp" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
