package com.prefera.article_labeling_interface.label.services;

import com.prefera.article_labeling_interface.label.Article;

import com.prefera.article_labeling_interface.label.repositories.ArticleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

@Service
public class ArticleService {

    @Autowired
    private MongoTemplate mongoTemplate;  // Use MongoTemplate for custom operations

    @Autowired
    private ArticleRepository articleRepository; // Original articles repository

    public void saveArticle(String articleId, boolean liked) {
        // Fetch the article from the original database
        Article article = articleRepository.findById(articleId)
                .orElseThrow(() -> new RuntimeException("Article not found"));

        if(liked){
            mongoTemplate.save(article, "liked_articles");
        }
        else{
            mongoTemplate.save(article, "disliked_articles");
        }
        mongoTemplate.save(article, "labeled_articles");

        // Save the article to the liked articles collection
        // Remove the article from the original database
        articleRepository.delete(article);
    }

}