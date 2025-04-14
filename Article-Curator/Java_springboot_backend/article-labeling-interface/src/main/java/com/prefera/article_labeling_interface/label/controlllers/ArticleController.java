package com.prefera.article_labeling_interface.label.controlllers;
import com.prefera.article_labeling_interface.label.*;
import com.prefera.article_labeling_interface.label.repositories.ArticleRepository;
import com.prefera.article_labeling_interface.label.services.ArticleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/api")
public class ArticleController {
    @Autowired
    private ArticleRepository articleRepository;  // Original articles repository

    @Autowired
    private ArticleService articleService;

    @PostMapping("/like")
    public ResponseEntity<String> likeArticle(@RequestParam String articleId) {
        articleService.saveArticle(articleId, true);
        return ResponseEntity.ok("Liked");
    }

    @PostMapping("/dislike")
    public ResponseEntity<String> dislikeArticle(@RequestParam String articleId) {
        articleService.saveArticle(articleId, false);
        return ResponseEntity.ok("Disliked");
    }
    @GetMapping({"/manual", "/label", "/label/**", "/manual_label"})
    public Article getNextManualArticle() {
        return articleRepository.findAll().stream()
                .filter(a -> a.getPreference() == null || a.getPreference() == 0)
                .findFirst()
                .orElse(null);
    }
}