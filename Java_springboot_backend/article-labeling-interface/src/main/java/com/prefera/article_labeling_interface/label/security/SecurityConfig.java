package com.prefera.article_labeling_interface.label.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf
                        .ignoringRequestMatchers("/like", "/dislike"))  // Disable CSRF for specific endpoints
                .authorizeHttpRequests(authorizeRequests -> authorizeRequests
                        .requestMatchers("/", "/manual_label", "/like", "/dislike").permitAll()  // Allow access to these URLs
                        .anyRequest().authenticated());  // Require authentication for all other requests

        return http.build();  // Build and return the security filter chain
    }
}