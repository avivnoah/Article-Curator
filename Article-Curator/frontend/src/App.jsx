import { Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import RecommendationsPage from "./pages/RecommendationsPage";
import ManualLabelPage from "./pages/ManualLabelPage";
import { useEffect, useState } from "react";
import "./index.css";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  // Toggle dark mode class on root html
  useEffect(() => {
    const root = window.document.documentElement;
    if (darkMode) {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }, [darkMode]);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 transition-colors duration-300 font-sans">
      {/* NavBar */}
      <div className="flex justify-between items-center p-4 bg-white dark:bg-gray-800 shadow">
        {/* Dark mode toggle */}
        <button
          className="bg-gray-200 dark:bg-gray-700 text-sm text-gray-800 dark:text-white px-4 py-2 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>

        {/* Dropdown */}
        <div className="relative group inline-block text-left">
          <div className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 cursor-pointer">
            ☰ Menu
          </div>

          <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 border dark:border-gray-600 rounded shadow-md 
                          opacity-0 invisible scale-95 
                          group-hover:opacity-100 group-hover:visible group-hover:scale-100
                          transition-all duration-200 ease-out z-50">
            <Link to="/" className="block px-4 py-2 hover:bg-indigo-100 dark:hover:bg-gray-600">🏠 Home</Link>
            <Link to="/recommendations" className="block px-4 py-2 hover:bg-indigo-100 dark:hover:bg-gray-600">🔥 Recommendations</Link>
            <Link to="/label" className="block px-4 py-2 hover:bg-indigo-100 dark:hover:bg-gray-600">✍️ Manual Label</Link>
          </div>
        </div>
      </div>

      {/* Routes */}
      <div className="p-6">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/label" element={<ManualLabelPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
