import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8080/api/recommendation")
      .then(res => setArticles([res.data]))  // wrap in array to reuse same rendering code
      .catch(err => console.error("Error:", err));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>🔥 Recommended Articles</h1>
      {articles.length === 0 ? (
        <p>No articles available.</p>
      ) : (
        articles.map((article, i) => (
          <div key={i} style={{
            marginBottom: "1rem",
            border: "1px solid #ddd",
            borderRadius: "6px",
            padding: "1rem"
          }}>
            <p><strong>Score:</strong> {article.score.toFixed(2)}</p>
            <p><strong>URL:</strong> <a href={article.url} target="_blank" rel="noreferrer">{article.url}</a></p>
            <p><strong>Excerpt:</strong> {article.data?.slice(0, 120)}...</p>
          </div>
        ))
      )}
    </div>
  );
}

export default App;