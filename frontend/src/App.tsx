import { Route, Routes } from "react-router-dom";
import Nav from "./components/Nav";
import Dashboard from "./pages/Dashboard";
import ManifestoChat from "./pages/ManifestoChat";
import PromiseCompare from "./pages/PromiseCompare";
import Scorecard from "./pages/Scorecard";

export default function App() {
  return (
    <div className="min-h-screen">
      <Nav />
      <main className="pt-28 pb-16 px-4 sm:px-6 max-w-6xl mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/manifestos" element={<ManifestoChat />} />
          <Route path="/compare" element={<PromiseCompare />} />
          <Route path="/scorecard" element={<Scorecard />} />
        </Routes>
      </main>
    </div>
  );
}
