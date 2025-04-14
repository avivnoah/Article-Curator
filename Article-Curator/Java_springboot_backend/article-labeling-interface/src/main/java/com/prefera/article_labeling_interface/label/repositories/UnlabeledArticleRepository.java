package com.prefera.article_labeling_interface.label.repositories;
import com.prefera.article_labeling_interface.label.UnlabeledArticle;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface UnlabeledArticleRepository extends MongoRepository<UnlabeledArticle, String> {
    UnlabeledArticle findTopByOrderByScoreDesc();
}