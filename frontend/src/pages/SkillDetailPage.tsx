import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchSkill, Skill } from "../api/client";
import { SkillDetail } from "../components/SkillDetail";

export function SkillDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [skill, setSkill] = useState<Skill | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    fetchSkill(slug)
      .then((s) => { setSkill(s); setLoading(false); })
      .catch(() => { setError("Skill não encontrada."); setLoading(false); });
  }, [slug]);

  if (loading) return <div className="state-message">Carregando…</div>;
  if (error || !skill) {
    return (
      <div className="state-message">
        <p>{error ?? "Skill não encontrada."}</p>
        <button className="btn-page" onClick={() => navigate("/")}>
          ← Voltar
        </button>
      </div>
    );
  }

  return <SkillDetail skill={skill} />;
}
