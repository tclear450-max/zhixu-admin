package com.zhixu;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;


@MapperScan({"com.zhixu.*.mapper"})
@SpringBootApplication
@EnableTransactionManagement(proxyTargetClass = true) // CGLIB 代理确保实现类 @Transactional 生效
@EnableScheduling
@EnableAsync
@EnableRetry
public class ZhixuApplication {
    public static void main(String[] args) {
        SpringApplication.run(ZhixuApplication.class, args);
    }
}
