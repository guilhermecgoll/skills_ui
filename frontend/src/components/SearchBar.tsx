import { useEffect, useState } from "react";

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export function SearchBar({ value, onChange }: Props) {
  const [local, setLocal] = useState(value);

  useEffect(() => {
    const id = setTimeout(() => onChange(local), 400);
    return () => clearTimeout(id);
  }, [local, onChange]);

  useEffect(() => {
    setLocal(value);
  }, [value]);

  return (
    <div className="search-wrapper">
      <input
        type="search"
        className="search-input"
        placeholder="Buscar skills por nome, descrição ou conteúdo…"
        value={local}
        onChange={(e) => setLocal(e.target.value)}
        autoFocus
      />
    </div>
  );
}
