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

  if (loading) return <p className="text-center p-6 text-gray-500 dark:text-gray-400">Loading article...</p>;

  if (!article) return <p className="text-center p-6 text-gray-500 dark:text-gray-400">No articles available to label.</p>;

  return (
    <div className="flex justify-center items-center min-h-[70vh] px-4">
      <div className="max-w-2xl w-full bg-white dark:bg-gray-900 rounded-lg shadow-md p-6 text-center">
        <h1 className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mb-4">
          ✍️ Manual Labeling
        </h1>
        <p className="mb-2">
          <strong className="text-gray-800 dark:text-gray-200">URL:</strong>{" "}
          <a href={article.url} className="text-indigo-600 dark:text-indigo-300 underline" target="_blank" rel="noreferrer">
            {article.url}
          </a>
        </p>
        <div className="max-h-[70vh] overflow-auto text-gray-700 dark:text-gray-300 whitespace-pre-wrap mb-6">
          <strong>Content:</strong> {article.data}
        </div>

        <div className="flex justify-center gap-4">
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
      </div>
    </div>
  );
}

export default ManualLabelPage;
