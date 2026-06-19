import { useCallback, useEffect, useState } from "react";
import { fetchSyncStatus, SyncStatus as SyncStatusType, triggerSync } from "../api/client";

function timeAgo(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60) return "agora mesmo";
  if (diff < 3600) return `há ${Math.floor(diff / 60)}min`;
  if (diff < 86400) return `há ${Math.floor(diff / 3600)}h`;
  return `há ${Math.floor(diff / 86400)}d`;
}

export function SyncStatus() {
  const [status, setStatus] = useState<SyncStatusType | null>(null);
  const [syncing, setSyncing] = useState(false);

  const loadStatus = useCallback(async () => {
    try {
      setStatus(await fetchSyncStatus());
    } catch {
      // silent
    }
  }, []);

  useEffect(() => {
    loadStatus();
    const id = setInterval(loadStatus, 30_000);
    return () => clearInterval(id);
  }, [loadStatus]);

  const handleSync = async () => {
    setSyncing(true);
    try {
      await triggerSync();
      await loadStatus();
    } finally {
      setSyncing(false);
    }
  };

  if (!status) return null;

  return (
    <div className="sync-status">
      <span className="sync-info">
        {status.skill_count} skill{status.skill_count !== 1 ? "s" : ""}
        {status.last_sync && (
          <span className="sync-time"> · {timeAgo(status.last_sync)}</span>
        )}
      </span>
      <button
        className="btn-sync"
        onClick={handleSync}
        disabled={syncing}
        title="Forçar sincronização com o repositório"
      >
        {syncing ? "Sincronizando…" : "Sincronizar"}
      </button>
    </div>
  );
}
