package com.prefera.article_labeling_interface.label;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "unlabeled_articles")
public class UnlabeledArticle {
    @Id
    private String id;
    private String url;
    private String data;
    private float score;

    public String getId() { return id; }
    public String getUrl() { return url; }
    public String getData() { return data; }
    public float getScore() { return score; }

    public void setId(String id) { this.id = id; }
    public void setUrl(String url) { this.url = url; }
    public void setData(String data) { this.data = data; }
    public void setScore(float score) { this.score = score; }
}
