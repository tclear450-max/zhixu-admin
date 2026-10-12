package com.zhixu.filetask.spi;

import com.zhixu.filetask.entity.FileTask;

/** 异步任务提交后的初始快照。 */
public record TaskSnapshot(Long taskId, FileTask snapshot) {
}
