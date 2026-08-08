import { useEffect, useState } from "react";
import { api, ScorecardEntry, ScorecardRollup } from "../lib/api";

const STATUS_COLOR: Record<string, string> = {
  Fulfilled: "#79cf9a",
  "Partially Fulfilled": "#a8d98f",
  "In Progress": "#8fc7f0",
  "Not Started": "#9397ab",
  "Goalpost Moved": "#e0a455",
  "Not Proven": "#e0768f",
};

function EntryCard({ entry }: { entry: ScorecardEntry }) {
  const color = STATUS_COLOR[entry.status] ?? "#9397ab";
  return (
    <div className="glass rounded-xl p-4 space-y-2">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-medium text-[#dfe2ee]">{entry.scheme_name}</h3>
          <p className="text-xs text-[#9ea3bb] mt-0.5">{entry.promise_summary}</p>
        </div>
        <span
          className="shrink-0 text-[10px] font-mono uppercase px-2.5 py-1 rounded-full border"
          style={{ borderColor: `${color}55`, color }}
        >
          {entry.status}
        </span>
      </div>

      {entry.delivery_index !== null ? (
        <div>
          <div className="flex justify-between text-[10px] font-mono text-[#75798c] mb-1">
            <span>Delivery Index</span>
            <span>
              {entry.achieved_value?.toLocaleString()} / {entry.target_value?.toLocaleString()}{" "}
              {entry.target_unit}
            </span>
          </div>
          <div className="h-2 rounded-full bg-white/5 overflow-hidden">
            <div
              className="h-full rounded-full"
              style={{ width: `${Math.min((entry.delivery_index ?? 0) * 100, 100)}%`, background: color }}
            />
          </div>
        </div>
      ) : entry.narrative_metric ? (
        <p className="text-xs text-[#cfd3e5] font-mono">{entry.narrative_metric}</p>
      ) : null}

      <p className="text-xs text-[#9397ab]">{entry.status_note}</p>

      <div className="flex flex-wrap gap-x-3 gap-y-1 pt-1">
        {entry.sources.map((s) => (
          <a
            key={s.url}
            href={s.url}
            target="_blank"
            rel="noreferrer"
            className="text-[10px] font-mono text-[#8fc7f0] hover:underline"
          >
            {s.label} ↗
          </a>
        ))}
        <span className="text-[10px] font-mono text-[#75798c] ml-auto">Updated {entry.last_updated}</span>
      </div>
    </div>
  );
}

export default function Scorecard() {
  const [rollups, setRollups] = useState<ScorecardRollup[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .scorecardRollup()
      .then((res) => setRollups(res.rollups))
      .finally(() => setLoading(false));
  }, []);

  const nonEmpty = rollups.filter((r) => r.entry_count > 0);

  return (
    <div className="space-y-6">
      <header className="space-y-3">
        <p className="text-[11px] font-mono uppercase tracking-[0.08em] text-[#b58ae8]">
          Promise-to-performance · seed dataset
        </p>
        <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">Delivery Scorecard</h1>
        <p className="text-sm text-[#9ea3bb] max-w-2xl">
          A small, hand-curated set of real, independently sourced entries demonstrating the scorecard
          methodology — not a live PFMS/CAG/budget-document pipeline. Every number here is cited to a
          government or CAG source; where no verified figure exists, the field is left blank rather than
          estimated, and shown as <span className="text-[#e0768f]">Not Proven</span>. All entries are
          currently BJP/NDA-run schemes, structurally, because a delivery scorecard can only score promises
          a party actually had power to implement — the same rule would apply to any other governing party.
        </p>
      </header>

      {loading && <div className="text-sm text-[#75798c] py-8 text-center">Loading…</div>}

      {!loading &&
        nonEmpty.map((rollup) => (
          <section key={rollup.taxonomy_category} className="space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-[#dfe2ee]">{rollup.taxonomy_category}</h2>
              {rollup.avg_delivery_index !== null && (
                <span className="text-[11px] font-mono text-[#75798c]">
                  avg delivery index {(rollup.avg_delivery_index * 100).toFixed(0)}%
                </span>
              )}
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {rollup.entries.map((entry) => (
                <EntryCard key={entry.id} entry={entry} />
              ))}
            </div>
          </section>
        ))}

      {!loading && nonEmpty.length === 0 && (
        <div className="glass rounded-2xl p-8 text-center text-sm text-[#75798c]">No scorecard entries yet.</div>
      )}
    </div>
  );
}
