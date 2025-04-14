import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="flex items-center justify-center min-h-[70vh] px-4">
      <div className="max-w-xl text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-indigo-600 dark:text-indigo-400 mb-4">
          Welcome to Article Curator
        </h1>
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6">
          Discover, rate, and label articles using your preferences.
          Start training your smart feed — or browse what you already love!
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link
            to="/label"
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded text-lg font-medium transition"
          >
            ✍️ Start Labeling
          </Link>
          <Link
            to="/recommendations"
            className="bg-white dark:bg-gray-800 dark:text-white border border-indigo-600 hover:bg-indigo-50 dark:hover:bg-gray-700 px-6 py-3 rounded text-lg font-medium transition"
          >
            🔥 See Recommendations
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
