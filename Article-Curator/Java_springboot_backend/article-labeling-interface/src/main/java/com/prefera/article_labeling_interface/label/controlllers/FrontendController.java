package com.prefera.article_labeling_interface.label.controlllers;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class FrontendController {
    @GetMapping({
            "/",
            "/about",
            "/recommendation",
             // allow nested routes
    })
    public String forwardReactRoutes() {
        return "forward:/index.html";
    }
}
