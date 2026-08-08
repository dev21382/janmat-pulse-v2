export type Topic = {
  id: string;
  label: string;
  query: string;
  hue: string;
};

export type FeedItem = {
  source: "reddit" | "news" | "gdelt";
  title: string;
  url: string;
  created_utc: number;
  score: number | null;
  sentiment: number;
};

export type ForecastPoint = { day: string; predicted_sentiment: number };
export type HistoryPoint = { day: string; mean_sentiment: number; item_count: number };

export type ForecastResponse = {
  topic_id: string;
  method: "lstm" | "naive_trend" | "insufficient_data";
  points_used?: number;
  history: HistoryPoint[];
  forecast: ForecastPoint[];
};

export type RagSource = {
  party_id: string;
  party_name: string;
  title: string;
  chunk_index: number;
  excerpt: string;
  relevance: number;
};

export type RagResponse = {
  answer: string;
  method: string;
  sources: RagSource[];
};

export type RagStatus = {
  index_built: boolean;
  generative_available: boolean;
  taxonomy_llm_available: boolean;
  sentiment_ml_available: boolean;
  parties: { party_id: string; party_name: string; title: string; url: string; hue: string; ingested: boolean }[];
};

export type ScoreBand = { min: number; max: number; label: string };
export type ScoringLegend = { bands: ScoreBand[]; confidence_thresholds: { high: number; medium: number } };
export type ScoringSummary = {
  topic_id: string;
  score_100: number;
  band: string;
  item_count: number;
  confidence: "High" | "Medium" | "Low";
  window_days: number;
  positive_share: number | null;
  neutral_share: number | null;
  negative_share: number | null;
};

export type TaxonomyCategory = { category: string; counts_by_party: Record<string, number> };
export type PromiseAtom = {
  id: number;
  party_id: string;
  party_name: string;
  hue: string;
  page: number;
  number: string;
  text: string;
  taxonomy_category: string;
  taxonomy_method: "llm" | "keyword";
  matched_keywords: string[];
  quantified: boolean;
};
export type ComparisonParty = {
  party_id: string;
  party_name: string;
  hue: string;
  promises: PromiseAtom[];
  quantified_count: number;
  directional_count: number;
};
export type ComparisonResponse = { category: string; parties: ComparisonParty[] };

export type ScorecardEntry = {
  id: string;
  party_id: string;
  scheme_name: string;
  promise_summary: string;
  taxonomy_category: string;
  target_value: number | null;
  target_unit: string | null;
  achieved_value: number | null;
  achieved_unit: string | null;
  delivery_index: number | null;
  allocation_ratio: number | null;
  utilization_rate: number | null;
  narrative_metric?: string;
  status: string;
  status_note: string;
  sources: { label: string; url: string }[];
  last_updated: string;
};
export type ScorecardRollup = {
  taxonomy_category: string;
  entry_count: number;
  avg_delivery_index: number | null;
  status_breakdown: Record<string, number>;
  entries: ScorecardEntry[];
};

export type SearchItem = {
  source: "reddit" | "news";
  title: string;
  url: string;
  created_utc: number;
  score: number | null;
  sentiment: number;
  sentiment_method: "hf_roberta" | "vader";
  bucket: "positive" | "neutral" | "negative";
  reach_percentile: number;
  reach_basis: "engagement" | "recency";
};
export type SearchResponse = {
  query: string;
  expanded_query: string;
  reddit_ok: boolean;
  news_ok: boolean;
  item_count: number;
  score_100: number;
  band: string;
  confidence: "High" | "Medium" | "Low";
  evidence: { positive: SearchItem[]; neutral: SearchItem[]; negative: SearchItem[] };
  items: SearchItem[];
  cache_hit?: boolean;
};

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

export const api = {
  topics: () => fetch("/api/topics").then((r) => json<Topic[]>(r)),
  feed: (topicId: string) => fetch(`/api/feed/${topicId}`).then((r) => json<{ topic_id: string; items: FeedItem[] }>(r)),
  forecast: (topicId: string) => fetch(`/api/forecast/${topicId}`).then((r) => json<ForecastResponse>(r)),
  ragStatus: () => fetch("/api/rag/status").then((r) => json<RagStatus>(r)),
  ragQuery: (question: string) =>
    fetch("/api/rag/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    }).then((r) => json<RagResponse>(r)),
  scoringLegend: () => fetch("/api/scoring/legend").then((r) => json<ScoringLegend>(r)),
  scoringSummary: (topicId: string) =>
    fetch(`/api/scoring/summary/${topicId}`).then((r) => json<ScoringSummary>(r)),
  taxonomy: () => fetch("/api/manifesto/taxonomy").then((r) => json<{ categories: TaxonomyCategory[] }>(r)),
  compareCategory: (category: string) =>
    fetch(`/api/manifesto/compare/${encodeURIComponent(category)}`).then((r) => json<ComparisonResponse>(r)),
  scorecardRollup: () =>
    fetch("/api/scorecard/rollup").then((r) => json<{ rollups: ScorecardRollup[]; status_options: string[] }>(r)),
  search: (q: string) => fetch(`/api/search?q=${encodeURIComponent(q)}`).then((r) => json<SearchResponse>(r)),
};
