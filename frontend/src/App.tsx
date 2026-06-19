import { Route, Routes } from "react-router-dom";
import { Header } from "./components/Header";
import { SkillDetailPage } from "./pages/SkillDetailPage";
import { SkillsPage } from "./pages/SkillsPage";

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<SkillsPage />} />
          <Route path="/skills/:slug" element={<SkillDetailPage />} />
        </Routes>
      </main>
    </div>
  );
}
