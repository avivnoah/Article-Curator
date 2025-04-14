package com.prefera.article_labeling_interface.label;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "articles")  // Collection for original articles
public class Article {
    @Id
    private String id;
    private String url;
    private String data;
    private float score;
    private Integer preference;

    public Article(){

    }
    public Article(String id, String url, String data){
        this.id = id;
        this.url = url;
        this.data = data;
        this.preference = 0;
    }
    public Article(String id, String url, String data, int preference){
        this.id = id;
        this.url = url;
        this.data = data;
        this.preference = preference;
    }
    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public Integer getPreference() { return preference; }
    public void setPreference(Integer preference) { this.preference = preference; }

}