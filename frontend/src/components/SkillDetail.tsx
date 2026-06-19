import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import remarkGfm from "remark-gfm";
import { downloadUrl, Skill } from "../api/client";

interface Props {
  skill: Skill;
}

export function SkillDetail({ skill }: Props) {
  return (
    <div className="skill-detail">
      <div className="detail-header">
        <Link to="/" className="back-link">
          ← Voltar
        </Link>
        <div className="detail-actions">
          <a
            href={downloadUrl(skill.slug)}
            className="btn-download btn-download-lg"
            download
          >
            Baixar .zip
          </a>
        </div>
      </div>

      <div className="detail-meta">
        <h1 className="detail-title">{skill.name}</h1>
        <div className="detail-attrs">
          {skill.author && <span className="detail-attr">Por {skill.author}</span>}
          {skill.version && <span className="detail-attr">v{skill.version}</span>}
        </div>
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

      {skill.content && (
        <div className="markdown-body">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {skill.content}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}
