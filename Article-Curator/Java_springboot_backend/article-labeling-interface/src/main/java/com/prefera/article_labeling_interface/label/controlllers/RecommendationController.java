package com.prefera.article_labeling_interface.label.controlllers;
import com.prefera.article_labeling_interface.label.UnlabeledArticle;
import com.prefera.article_labeling_interface.label.repositories.UnlabeledArticleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class RecommendationController {

    @Autowired
    private UnlabeledArticleRepository unlabeledArticleRepository;

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
}