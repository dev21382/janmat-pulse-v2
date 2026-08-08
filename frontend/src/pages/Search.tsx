import { useState } from "react";
import { api, SearchItem, SearchResponse } from "../lib/api";

const BUCKET_META: Record<string, { label: string; color: string }> = {
  positive: { label: "Positive", color: "#79cf9a" },
  neutral: { label: "Neutral / Mixed", color: "#9397ab" },
  negative: { label: "Negative", color: "#e0768f" },
};

const EXAMPLE_QUERIES = ["GST", "farmer protests", "Agnipath scheme", "caste census"];

function timeAgo(unix: number) {
  const diff = Date.now() / 1000 - unix;
  if (diff < 3600) return `${Math.max(1, Math.round(diff / 60))}m ago`;
  if (diff < 86400) return `${Math.round(diff / 3600)}h ago`;
  return `${Math.round(diff / 86400)}d ago`;
}

function EvidenceCard({ item }: { item: SearchItem }) {
  return (
    <a
      href={item.url}
      target="_blank"
      rel="noreferrer"
      className="block rounded-lg border border-white/10 p-3 hover:border-white/25 transition-colors"
    >
      <p className="text-xs text-[#dfe2ee] line-clamp-3">{item.title}</p>
      <div className="mt-2 flex items-center justify-between text-[10px] font-mono text-[#75798c]">
        <span>
          {item.source} · {timeAgo(item.created_utc)}
        </span>
        <span title={item.reach_basis === "engagement" ? "Ranked by real engagement (upvotes)" : "No engagement metric available for this source — ranked by recency instead"}>
          reach {Math.round(item.reach_percentile * 100)}% ({item.reach_basis})
        </span>
      </div>
    </a>
  );
}

export default function Search() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runSearch(q: string) {
    if (!q.trim() || loading) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.search(q);
      setResult(res);
    } catch (e) {
      setError("Search failed — try again in a moment.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <header className="space-y-3">
        <p className="text-[11px] font-mono uppercase tracking-[0.08em] text-[#e0768f]">
          Open search · Reddit + Google News, live
        </p>
        <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">Search Any Topic</h1>
        <p className="text-sm text-[#9ea3bb] max-w-2xl">
          Not limited to the curated dashboard topics — search any keyword or issue. Queries are expanded
          with common synonyms, transliterations, and hashtags (e.g. "GST" also matches "जीएसटी") before
          fanning out live to Reddit and Google News, each capped at an 8-second budget so a slow source
          never blocks the response. GDELT isn't used here — it self-throttles and stays a
          background-ingestion-only source (see the Dashboard). Results are cached for 15 minutes per
          query to avoid re-hitting rate-limited sources.
        </p>
      </header>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          runSearch(query);
        }}
        className="flex gap-2"
      >
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a topic, e.g. 'Agnipath scheme'…"
          className="flex-1 bg-white/5 rounded-lg px-4 py-3 text-sm outline-none focus:ring-1 focus:ring-white/20 placeholder:text-[#75798c] glass"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-5 py-3 rounded-lg bg-[#e0768f] text-[#0f1120] text-sm font-medium disabled:opacity-50"
        >
          {loading ? "Searching…" : "Search"}
        </button>
      </form>

      {!result && !loading && (
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => {
                setQuery(q);
                runSearch(q);
              }}
              className="text-xs px-3 py-1.5 rounded-full border border-white/10 text-[#cfd3e5] hover:border-white/25"
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {error && <div className="text-sm text-[#e0768f]">{error}</div>}

      {result && (
        <div className="space-y-6">
          <div className="glass rounded-xl p-4 flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-[10px] font-mono uppercase tracking-wide text-[#75798c]">
                "{result.query}" {result.expanded_query !== result.query && "· query expanded"} ·{" "}
                {result.item_count} items
                {result.cache_hit ? " · cached" : ""}
              </p>
              <p className="text-2xl font-semibold" style={{ color: result.score_100 >= 0 ? "#79cf9a" : "#e0768f" }}>
                {result.score_100 > 0 ? "+" : ""}
                {result.score_100}
              </p>
              <p className="text-sm text-[#cfd3e5]">{result.band}</p>
            </div>
            <div className="flex gap-2 text-[11px] font-mono">
              <span className={`px-2.5 py-1 rounded-full border ${result.reddit_ok ? "border-[#79cf9a55] text-[#79cf9a]" : "border-white/10 text-[#75798c]"}`}>
                Reddit {result.reddit_ok ? "●" : "unavailable"}
              </span>
              <span className={`px-2.5 py-1 rounded-full border ${result.news_ok ? "border-[#79cf9a55] text-[#79cf9a]" : "border-white/10 text-[#75798c]"}`}>
                News {result.news_ok ? "●" : "unavailable"}
              </span>
              <span className="px-2.5 py-1 rounded-full border border-white/10 text-[#9397ab]">
                {result.confidence} confidence
              </span>
            </div>
          </div>

          <section>
            <h2 className="text-sm font-medium text-[#dfe2ee] mb-3">
              Evidence panel — top 2 by reach per bucket
            </h2>
            <div className="grid gap-4 sm:grid-cols-3">
              {(["positive", "neutral", "negative"] as const).map((bucket) => (
                <div key={bucket} className="glass rounded-xl p-3 space-y-2">
                  <p className="text-xs font-mono uppercase" style={{ color: BUCKET_META[bucket].color }}>
                    {BUCKET_META[bucket].label}
                  </p>
                  {result.evidence[bucket].length === 0 && (
                    <p className="text-xs text-[#75798c] py-4 text-center">No items in this bucket.</p>
                  )}
                  {result.evidence[bucket].map((item, i) => (
                    <EvidenceCard key={i} item={item} />
                  ))}
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="text-sm font-medium text-[#dfe2ee] mb-2">All results</h2>
            <ul className="glass rounded-2xl divide-y divide-white/5 p-2">
              {result.items.map((item, i) => (
                <li key={i} className="p-3 flex items-start gap-3">
                  <span
                    className="mt-1.5 w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: BUCKET_META[item.bucket].color }}
                  />
                  <div className="min-w-0 flex-1">
                    <a href={item.url} target="_blank" rel="noreferrer" className="text-sm text-[#dfe2ee] hover:text-white">
                      {item.title}
                    </a>
                    <p className="text-[11px] font-mono uppercase text-[#75798c] mt-1">
                      {item.source} · {timeAgo(item.created_utc)}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </section>
        </div>
      )}
    </div>
  );
}
