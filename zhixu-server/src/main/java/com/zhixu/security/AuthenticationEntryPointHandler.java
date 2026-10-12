package com.zhixu.security;

import com.alibaba.fastjson.JSON;
import com.zhixu.common.dto.ResponseDTO;
import com.zhixu.common.enums.BusinessStatusEnum;
import com.zhixu.util.WebUtil;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;


@Component
public class AuthenticationEntryPointHandler implements AuthenticationEntryPoint {
    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException authException) {
        String str = JSON.toJSONString(new ResponseDTO(BusinessStatusEnum.UNAUTHORIZED));
        // 给出异常提示信息
        WebUtil.renderString(response, str);
    }
}
