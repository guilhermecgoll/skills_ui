import { Link } from "react-router-dom";
import { SyncStatus } from "./SyncStatus";

export function Header() {
  return (
    <header className="header">
      <Link to="/" className="logo">
        Skills
      </Link>
      <SyncStatus />
    </header>
  );
}
