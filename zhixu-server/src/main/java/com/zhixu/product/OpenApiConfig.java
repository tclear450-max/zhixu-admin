package com.zhixu.product;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI zhixuOpenApi() {
        return new OpenAPI().info(new Info().title("知序人事 · ZHIXU API")
                .version("1.0.0").description("连接组织、流程与知识的企业人事工作空间"));
    }
}
