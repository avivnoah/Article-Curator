# 🚀 Article Curator – Scalable Roadmap

This roadmap reflects the transition to a production-grade article recommendation system powered by transformers, user handling, and scalable crawling.

---

## ✅ Phase 1: User Infrastructure & Experience (Week 1–2)
- [ ] Create user registration and login system (Spring Security or Firebase)
- [ ] Implement guest mode: prompt-based discovery without saving
- [ ] Store reading history & saved articles in MongoDB
- [ ] UI routing: differentiate guest vs user experience

---

## ✅ Phase 2: Recommendation Engine (Week 2–4)
- [ ] Use Sentence-BERT to embed article paragraphs
- [ ] Average embeddings to represent full article
- [ ] Store vectors + metadata in FAISS or Weaviate
- [ ] Prompt → embedding → vector search (for guests)
- [ ] For users: aggregate user vectors from liked articles
- [ ] Combine prompt and user vector (weighted avg) → search
- [ ] Feedback loop to refine user vectors (on like/dislike)

---

## ✅ Phase 3: Backend Resilience & Zero-Downtime (Week 4–5)
- [ ] Blue-Green Deployment for backend (model/crawler updates)
- [ ] Set up 2 environments: staging & production
- [ ] Add GitHub Actions for CI/CD (build → test → deploy)
- [ ] Automate switch between environments on validation

---

## ✅ Phase 4: Distributed Crawling (Week 5–6)
- [ ] Adapt crawler to skip previously crawled links
- [ ] Create Playwright/Chromium workers running in parallel
- [ ] Deploy as containerized jobs (e.g., with Docker)
- [ ] Auto-embed new articles + insert to vector DB

---

## ✅ Optional: User-defined Crawl Sources
- [ ] Frontend: form for submitting preferred websites
- [ ] Generate or edit site configs dynamically
- [ ] Crawl new sites with fallback selectors