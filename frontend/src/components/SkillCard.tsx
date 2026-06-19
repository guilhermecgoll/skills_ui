import { Link } from "react-router-dom";
import { downloadUrl, Skill } from "../api/client";

interface Props {
  skill: Skill;
}

export function SkillCard({ skill }: Props) {
  const handleDownload = (e: React.MouseEvent) => {
    e.preventDefault();
    window.location.href = downloadUrl(skill.slug);
  };

  return (
    <Link to={`/skills/${skill.slug}`} className="skill-card">
      <div className="skill-card-body">
        <h2 className="skill-name">{skill.name}</h2>
        {skill.description && (
          <p className="skill-description">{skill.description}</p>
        )}
        {skill.tags.length > 0 && (
          <div className="tag-list">
            {skill.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
      <div className="skill-card-footer">
        {skill.author && (
          <span className="skill-meta">{skill.author}</span>
        )}
        <button className="btn-download" onClick={handleDownload}>
          Baixar
        </button>
      </div>
    </Link>
  );
}
