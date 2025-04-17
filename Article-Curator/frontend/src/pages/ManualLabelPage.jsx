import { useEffect, useState } from "react";
import axios from "axios";

function ManualLabelPage() {
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchNextArticle = () => {
    setLoading(true);
    axios.get("http://localhost:8080/api/manual")
      .then(res => {
        setArticle(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching article:", err);
        setArticle(null);
        setLoading(false);
      });
  };

  const submitFeedback = (liked) => {
    if (!article) return;

    const endpoint = liked ? "/like" : "/dislike";

    axios.post(`http://localhost:8080/api${endpoint}`, null, {
      params: { articleId: article.id }
    })
    .then(() => fetchNextArticle())
    .catch(err => console.error("Error submitting feedback:", err));
  };

  useEffect(() => {
    fetchNextArticle();
  }, []);

  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center px-4">
      <h1 className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mb-6">✍️ Manual Labeling</h1>

      {loading ? (
        <p className="text-gray-500 dark:text-gray-400">Loading article...</p>
      ) : !article ? (
        <p className="text-gray-500 dark:text-gray-400">No articles available to label.</p>
      ) : (
        <>
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow max-w-2xl w-full">
            <p className="mb-2 flex gap-2 items-start text-gray-700 dark:text-gray-300">
              <span className="font-semibold">URL:</span>
              <span className="flex-1 truncate">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-500 underline truncate inline-block max-w-full"
                  title={article.url}
                >
                  {article.url}
                </a>
              </span>
            </p>

            <div className="text-gray-700 dark:text-gray-300 overflow-hidden max-h-48">
              <span className="font-semibold">Content:</span>{" "}
              <span className="line-clamp-10">{article.data}</span>
            </div>
          </div>

          <div className="flex gap-4 mt-6">
            <button
              onClick={() => submitFeedback(true)}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded transition font-medium"
            >
              👍 Like
            </button>
            <button
              onClick={() => submitFeedback(false)}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded transition font-medium"
            >
              👎 Dislike
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ManualLabelPage;
