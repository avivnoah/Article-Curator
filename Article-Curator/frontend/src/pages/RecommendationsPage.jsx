import { useEffect, useState } from "react";
import axios from "axios";

function RecommendationsPage() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8080/api/recommendation")
      .then(res => setArticles([res.data]))
      .catch(err => console.error("Error:", err));
  }, []);

  return (
    <div className="flex justify-center items-center min-h-[70vh] px-4">
      <div className="max-w-2xl w-full bg-white dark:bg-gray-900 rounded-lg shadow-md p-6 text-center">
        <h1 className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mb-4">
          🔥 Recommended Article
        </h1>
        {articles.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400">No articles available.</p>
        ) : (
          articles.map((article, i) => (
            <div key={i} className="text-left">
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                <strong>Recommendation Score:</strong> {article.score.toFixed(2)}
              </p>
              <p className="mb-2">
                <strong className="text-gray-800 dark:text-gray-200">URL:</strong>{" "}
                <a href={article.url} className="text-indigo-600 dark:text-indigo-300 underline" target="_blank" rel="noreferrer">
                  {article.url}
                </a>
              </p>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>Excerpt:</strong> {article.data?.slice(0, 200)}...
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default RecommendationsPage;
