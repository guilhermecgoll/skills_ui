import { useEffect, useState } from "react";
import { fetchSkills, SkillsPage } from "../api/client";
import { SkillCard } from "./SkillCard";

interface Props {
  query: string;
}

export function SkillGrid({ query }: Props) {
  const [data, setData] = useState<SkillsPage | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setPage(1);
  }, [query]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetchSkills(query || undefined, page)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((err: Error) => { if (!cancelled) { setError(err.message); setLoading(false); } });

    return () => { cancelled = true; };
  }, [query, page]);

  if (loading) {
    return <div className="state-message">Carregando…</div>;
  }

  if (error) {
    return <div className="state-message state-error">Erro: {error}</div>;
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="state-message">
        {query ? `Nenhuma skill encontrada para "${query}".` : "Nenhuma skill disponível."}
      </div>
    );
  }

  return (
    <div>
      <p className="results-count">
        {data.total} skill{data.total !== 1 ? "s" : ""} encontrada{data.total !== 1 ? "s" : ""}
        {query && ` para "${query}"`}
      </p>
      <div className="skills-grid">
        {data.items.map((skill) => (
          <SkillCard key={skill.slug} skill={skill} />
        ))}
      </div>
      {data.pages > 1 && (
        <div className="pagination">
          <button
            className="btn-page"
            disabled={page === 1}
            onClick={() => setPage((p) => p - 1)}
          >
            ← Anterior
          </button>
          <span className="page-info">
            {page} / {data.pages}
          </span>
          <button
            className="btn-page"
            disabled={page === data.pages}
            onClick={() => setPage((p) => p + 1)}
          >
            Próxima →
          </button>
        </div>
      )}
    </div>
  );
}
