package com.zhixu.leave.approval;

import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.zhixu.leave.entity.StaffLeave;
import com.zhixu.leave.enums.AuditStatusEnum;
import com.zhixu.common.enums.BusinessStatusEnum;
import com.zhixu.security.ServiceException;
import com.zhixu.leave.approval.ApprovalCandidateResolver;
import com.zhixu.leave.service.StaffLeaveService;
import org.flowable.engine.RuntimeService;
import org.flowable.engine.delegate.DelegateExecution;
import org.flowable.engine.delegate.ExecutionListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;

/**
 * HR 审批执行监听器——流程转译层。
 * <p>
 * 请假状态置为待审 + 装配经理候选人变量，委托 {@link ApprovalCandidateResolver} 解析候选人。
 * </p>
 */
@Component
public class HrApproveListener implements ExecutionListener {

    private final StaffLeaveService staffLeaveService;
    private final ApprovalCandidateResolver candidateResolver;
    private final RuntimeService runtimeService;

    public HrApproveListener(StaffLeaveService staffLeaveService,
                             ApprovalCandidateResolver candidateResolver,
                             RuntimeService runtimeService) {
        this.staffLeaveService = staffLeaveService;
        this.candidateResolver = candidateResolver;
        this.runtimeService = runtimeService;
    }

    @Override
    @Transactional
    public void notify(DelegateExecution execution) {
        UpdateWrapper<StaffLeave> updateWrapper = new UpdateWrapper<>();
        updateWrapper.set("status", AuditStatusEnum.UNAUDITED).eq("id", Integer.valueOf(execution.getProcessInstanceBusinessKey()));
        if (!this.staffLeaveService.update(updateWrapper)) {
            throw new ServiceException(BusinessStatusEnum.ERROR);
        }
        Map<String, Object> variables = new HashMap<>();
        variables.put("manager", candidateResolver.codesOfRole("manager"));
        runtimeService.setVariables(execution.getId(), variables);
    }
}