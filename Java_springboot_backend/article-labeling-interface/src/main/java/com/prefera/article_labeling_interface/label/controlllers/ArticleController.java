package com.prefera.article_labeling_interface.label.controlllers;

import com.prefera.article_labeling_interface.label.*;
import com.prefera.article_labeling_interface.label.repositories.ArticleRepository;
import com.prefera.article_labeling_interface.label.repositories.DislikedArticleRepository;
import com.prefera.article_labeling_interface.label.repositories.LikedArticleRepository;
import com.prefera.article_labeling_interface.label.repositories.UsedArticleRepository;
import com.prefera.article_labeling_interface.label.services.ArticleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class ArticleController {

    @Autowired
    private ArticleService articleService;

    @Autowired
    private ArticleRepository articleRepository;  // Original articles repository

    @Autowired
    private LikedArticleRepository likedArticleRepository;  // Liked articles repository

    @Autowired
    private DislikedArticleRepository dislikedArticleRepository;  // Disliked articles repository

    @Autowired
    private UsedArticleRepository usedArticleRepository;  // Disliked articles repository

    @GetMapping("/")
    public String index() {
        return "index";  // Render the index.html template
    }

    @GetMapping("/manual_label")
    public String labelArticle(Model model) {
        // Fetch one random article from the database
        List<Article> articles = articleRepository.findAll();
        if (!articles.isEmpty()) {
            Article article = articles.get(0);  // Get the first article
            model.addAttribute("article", article);
            return "manual_label";  // Render the manual_label.html template
        }
        model.addAttribute("message", "No articles available.");
        return "manual_label";  // Handle the case where no articles are available
    }

    @PostMapping("/like")
    public String likeArticle(@RequestParam String articleId) {
        // Retrieve the article to like
        articleService.saveArticle(articleId, true);
        return "redirect:/manual_label";  // Redirect back to label page for the next article
    }

    @PostMapping("/dislike")
    public String dislikeArticle(@RequestParam String articleId) {
        // Retrieve the article to dislike
        articleService.saveArticle(articleId, false);
        return "redirect:/manual_label";  // Redirect back to label page for the next article
    }
}