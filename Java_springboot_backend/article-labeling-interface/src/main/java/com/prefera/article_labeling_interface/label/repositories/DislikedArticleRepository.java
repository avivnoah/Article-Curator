package com.prefera.article_labeling_interface.label.repositories;

import com.prefera.article_labeling_interface.label.Article;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface DislikedArticleRepository extends MongoRepository<Article, String> {
    // You can add custom query methods if needed
}