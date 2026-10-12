package com.zhixu.role.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zhixu.common.enums.BusinessStatusEnum;
import com.zhixu.common.dto.Response;
import com.zhixu.common.dto.ResponseDTO;
import com.zhixu.role.entity.StaffRole;
import com.zhixu.security.ServiceException;
import com.zhixu.role.mapper.StaffRoleMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * @Date 2022/3/1
 * @Version 1.0
 */

@Service
public class StaffRoleService extends ServiceImpl<StaffRoleMapper, StaffRole> {

    @Transactional
    public ResponseDTO setRole(Integer staffId, List<Integer> roleIds) {
        remove(new QueryWrapper<StaffRole>().eq("staff_id", staffId));
        for (Integer roleId : roleIds) {
            save(new StaffRole().setStaffId(staffId).setRoleId(roleId));
        }
        return Response.success();
    }

    public ResponseDTO queryByStaffId(Integer staffId) {
        List<StaffRole> list = list(new QueryWrapper<StaffRole>().eq("staff_id",staffId));
        return Response.success(list);
    }
}
