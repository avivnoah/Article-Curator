package com.prefera.article_labeling_interface.label.repositories;
import com.prefera.article_labeling_interface.label.Article;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ArticleRepository extends MongoRepository<Article, String> {
    // Add custom query methods when needed
}