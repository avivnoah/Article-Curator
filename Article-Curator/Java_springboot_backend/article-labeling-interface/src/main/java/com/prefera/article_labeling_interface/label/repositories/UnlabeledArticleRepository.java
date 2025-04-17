package com.prefera.article_labeling_interface.label.repositories;
import com.prefera.article_labeling_interface.label.UnlabeledArticle;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface UnlabeledArticleRepository extends MongoRepository<UnlabeledArticle, String> {
    UnlabeledArticle findTopByOrderByScoreDesc();
    Page<UnlabeledArticle> findByScoreGreaterThanOrderByScoreDesc(float minScore, Pageable pageable);
}