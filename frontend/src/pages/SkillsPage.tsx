import { useState } from "react";
import { SearchBar } from "../components/SearchBar";
import { SkillGrid } from "../components/SkillGrid";

export function SkillsPage() {
  const [query, setQuery] = useState("");

  return (
    <div className="page-skills">
      <SearchBar value={query} onChange={setQuery} />
      <SkillGrid query={query} />
    </div>
  );
}
