const API = "/api";

export interface Skill {
  slug: string;
  name: string;
  description: string;
  tags: string[];
  author: string;
  version: string;
  updated_at: string;
  content?: string;
}

export interface SkillsPage {
  items: Skill[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface SyncStatus {
  last_sync: string | null;
  status: string;
  skill_count: number;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, init);
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export function fetchSkills(q?: string, page = 1, limit = 20): Promise<SkillsPage> {
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  params.set("page", String(page));
  params.set("limit", String(limit));
  return request<SkillsPage>(`/skills?${params}`);
}

export function fetchSkill(slug: string): Promise<Skill> {
  return request<Skill>(`/skills/${encodeURIComponent(slug)}`);
}

export function fetchSyncStatus(): Promise<SyncStatus> {
  return request<SyncStatus>("/sync/status");
}

export function triggerSync(): Promise<SyncStatus & { message: string }> {
  return request("/sync/trigger", { method: "POST" });
}

export function downloadUrl(slug: string): string {
  return `${API}/skills/${encodeURIComponent(slug)}/download`;
}
