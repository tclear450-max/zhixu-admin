package com.zhixu.filetask.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zhixu.filetask.entity.FileTaskError;
import com.zhixu.filetask.mapper.FileTaskErrorMapper;
import org.springframework.stereotype.Service;

@Service
public class FileTaskErrorService extends ServiceImpl<FileTaskErrorMapper, FileTaskError> {
}
