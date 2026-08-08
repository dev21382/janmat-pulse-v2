import { useEffect, useState } from "react";
import { api, ComparisonResponse, TaxonomyCategory } from "../lib/api";

export default function PromiseCompare() {
  const [categories, setCategories] = useState<TaxonomyCategory[]>([]);
  const [active, setActive] = useState<string>("");
  const [comparison, setComparison] = useState<ComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.taxonomy().then((res) => {
      setCategories(res.categories);
      if (res.categories.length) setActive(res.categories[0].category);
    });
  }, []);

  useEffect(() => {
    if (!active) return;
    setLoading(true);
    api
      .compareCategory(active)
      .then(setComparison)
      .finally(() => setLoading(false));
  }, [active]);

  return (
    <div className="space-y-6">
      <header className="space-y-3">
        <p className="text-[11px] font-mono uppercase tracking-[0.08em] text-[#e0a455]">
          Manifesto intelligence · cross-party comparison
        </p>
        <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">Promise Comparison</h1>
        <p className="text-sm text-[#9ea3bb] max-w-2xl">
          Every promise-atom is a discrete, page-cited commitment extracted from the manifesto's own
          numbered lists, then tagged to a fixed 10-category taxonomy so parties are compared on identical
          terms regardless of how each document is organised. Tagging uses an LLM classifier (Groq) when
          configured — shown as <span className="text-[#8fc7f0]">AI-tagged</span> — falling back to keyword
          matching per atom otherwise, shown as <span className="text-[#9397ab]">keyword-tagged</span> with
          its matched keywords visible for auditability either way. "Quantified" means the commitment has a
          number, amount, or date attached; "directional" means it doesn't. BJP's and TMC's manifestos are
          written as prose/bullet sections rather than numbered lists, so they contribute few or no
          promise-atoms here — a real property of those documents, not a gap in extraction. Their full text
          is still searchable in Manifesto Chat.
        </p>
      </header>

      <div className="flex flex-wrap gap-2">
        {categories.map((c) => (
          <button
            key={c.category}
            onClick={() => setActive(c.category)}
            className="px-3 py-1.5 rounded-full text-xs border transition-colors"
            style={{
              borderColor: active === c.category ? "#e0a455" : "rgba(242,243,250,0.14)",
              color: active === c.category ? "#e0a455" : "#9397ab",
              background: active === c.category ? "#e0a4551a" : "transparent",
            }}
          >
            {c.category}
            <span className="ml-1.5 text-[10px] font-mono text-[#75798c]">
              {Object.values(c.counts_by_party).reduce((a, b) => a + b, 0)}
            </span>
          </button>
        ))}
      </div>

      {loading && <div className="text-sm text-[#75798c] py-8 text-center">Loading…</div>}

      {!loading && comparison && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {comparison.parties.length === 0 && (
            <div className="col-span-full text-sm text-[#75798c] py-8 text-center glass rounded-2xl">
              No numbered promise-atoms detected for this category in the ingested manifestos.
            </div>
          )}
          {comparison.parties.map((party) => (
            <div key={party.party_id} className="glass rounded-2xl p-4 space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold" style={{ color: party.hue }}>
                  {party.party_name}
                </h2>
                <span className="text-[10px] font-mono text-[#75798c]">
                  {party.quantified_count} quantified · {party.directional_count} directional
                </span>
              </div>
              <ul className="space-y-3 max-h-[520px] overflow-y-auto pr-1">
                {party.promises.map((p) => (
                  <li key={p.id} className="text-xs border-l-2 pl-3" style={{ borderColor: `${party.hue}55` }}>
                    <p className="text-[#dfe2ee]">{p.text}</p>
                    <p className="text-[10px] font-mono text-[#75798c] mt-1">
                      p.{p.page} · #{p.number} ·{" "}
                      <span style={{ color: p.quantified ? "#79cf9a" : "#e0a455" }}>
                        {p.quantified ? "quantified" : "directional"}
                      </span>{" "}
                      ·{" "}
                      <span style={{ color: p.taxonomy_method === "llm" ? "#8fc7f0" : "#9397ab" }}>
                        {p.taxonomy_method === "llm" ? "AI-tagged" : "keyword-tagged"}
                      </span>
                    </p>
                  </li>
                ))}
                {party.promises.length === 0 && (
                  <li className="text-xs text-[#75798c]">No atoms tagged to this category.</li>
                )}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
