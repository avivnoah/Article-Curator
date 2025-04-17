package com.prefera.article_labeling_interface.label.controlllers;
import com.prefera.article_labeling_interface.label.UnlabeledArticle;
import com.prefera.article_labeling_interface.label.repositories.UnlabeledArticleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.Comparator;
import java.util.List;

@RestController
@RequestMapping("/api")
public class RecommendationController {

    @Autowired
    private UnlabeledArticleRepository unlabeledArticleRepository;
    /*
    @GetMapping("/recommendation")
    public UnlabeledArticle getTopScoredArticle() {
        UnlabeledArticle top = unlabeledArticleRepository.findTopByOrderByScoreDesc();
        if (top == null) {
            System.out.println("⚠️ No article found.");
        } else {
            System.out.println("✅ Top article: " + top.getUrl() + " | Score: " + top.getScore());
        }
        return top;
    }
    */
    /*
    @GetMapping("/recommendations")
    public List<UnlabeledArticle> getTopScoredArticles(
            @RequestParam(defaultValue = "0") int offset,
            @RequestParam(defaultValue = "10") int limit) {

        List<UnlabeledArticle> sortedArticles = unlabeledArticleRepository.findAll().stream()
                .filter(article -> article.getScore() > 0.0f)
                .sorted(Comparator.comparing(UnlabeledArticle::getScore).reversed())
                .skip(offset)
                .limit(limit)
                .toList();
        System.out.println("Returned articles: " + sortedArticles.size());
        return sortedArticles;
    }
     */
    @GetMapping("/recommendations")
    public Page<UnlabeledArticle> getTopScoredArticles(Pageable pageable) {
        return unlabeledArticleRepository.findByScoreGreaterThanOrderByScoreDesc(0.0f, pageable);
    }

}