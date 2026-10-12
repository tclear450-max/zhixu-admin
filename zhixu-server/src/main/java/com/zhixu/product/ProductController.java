package com.zhixu.product;

import com.zhixu.common.dto.Response;
import com.zhixu.common.dto.ResponseDTO;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
public class ProductController {
    private final String model;
    public ProductController(@Value("${spring.ai.openai.chat.options.model}") String model) {
        this.model = model;
    }
    @GetMapping("/product/info")
    public ResponseDTO info() {
        return Response.success(Map.of("name", "知序人事", "brand", "ZHIXU", "version", "1.0.0",
                "demo", model.startsWith("hrm-demo-"), "model", model));
    }
}
