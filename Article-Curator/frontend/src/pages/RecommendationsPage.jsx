import { useEffect, useState } from "react";
import axios from "axios";

function RecommendationsPage() {
  const [articles, setArticles] = useState([]);
  const [page, setPage] = useState(0);
  const [lastPage, setLastPage] = useState(false);
  const [totalPages, setTotalPages] = useState(0);
  const size = 1;

  const fetchPage = (page) => {
    axios
      .get(`http://localhost:8080/api/recommendations?page=${page}&size=${size}`)
      .then((res) => {
        setArticles(res.data.content);
        setLastPage(res.data.last);
        setTotalPages(res.data.totalPages);
      })
      .catch((err) => console.error("Error:", err));
  };

  useEffect(() => {
    fetchPage(page);
  }, [page]);

  const next = () => {
    if (!lastPage) setPage((prev) => prev + 1);
  };

  const prev = () => {
    if (page > 0) setPage((prev) => prev - 1);
  };

  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center px-4">
      <h1 className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mb-6">🔥 Recommended Articles</h1>
      {articles.length === 0 ? (
        <p className="text-gray-500">No articles available.</p>
      ) : (
        <div className="bg-white dark:bg-gray-800 p-6 rounded shadow max-w-2xl w-full">
          <p className="mb-2 text-gray-700 dark:text-gray-300">
            <span className="font-semibold">Score:</span> {articles[0].score.toFixed(2)}
          </p>
          <div className="flex gap-2 items-start mb-2">
            <span className="font-semibold text-gray-700 dark:text-gray-300">URL:</span>
            <a
              href={articles[0].url}
              target="_blank"
              rel="noreferrer"
              className="text-blue-500 underline truncate"
              style={{ maxWidth: "80%", display: "inline-block" }}
              title={articles[0].url}
            >
              {articles[0].url}
            </a>
          </div>

          <div className="text-gray-700 dark:text-gray-300 line-clamp-3">
            <span className="font-semibold">Content:</span> {articles[0].data}
          </div>
        </div>
      )}

      <div className="flex gap-4 mt-6">
        <button
          onClick={prev}
          disabled={page === 0}
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded disabled:opacity-50"
        >
          ← Previous
        </button>
        <button
          onClick={next}
          disabled={lastPage}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Next →
        </button>
      </div>

      <p className="text-sm text-gray-500 mt-2">
        Article {page + 1} of {totalPages}
      </p>
    </div>
  );
}

export default RecommendationsPage;
