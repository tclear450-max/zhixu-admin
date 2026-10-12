package com.zhixu.salary.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zhixu.salary.entity.SalaryDeduct;
import com.zhixu.salary.enums.DeductEnum;
import com.zhixu.salary.mapper.SalaryDeductMapper;
import com.zhixu.common.dto.Response;
import com.zhixu.common.dto.ResponseDTO;
import com.zhixu.util.EnumUtil;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * <p>
 * 工资扣除表 服务类
 * </p>
 *
 * @since 2022-03-27
 */
@Service
public class SalaryDeductService extends ServiceImpl<SalaryDeductMapper, SalaryDeduct> {


    public ResponseDTO add(SalaryDeduct salaryDeduct) {
        if (save(salaryDeduct)) {
            return Response.success();
        }
        return Response.error();
    }

    public ResponseDTO delete(Integer id) {
        if (removeById(id)) {
            return Response.success();
        }
        return Response.error();
    }

    public ResponseDTO deleteBatch(List<Integer> ids) {
        if (removeBatchByIds(ids)) {
            return Response.success();
        }
        return Response.error();
    }


    public ResponseDTO edit(SalaryDeduct salaryDeduct) {
        if (updateById(salaryDeduct)) {
            return Response.success();
        }
        return Response.error();
    }


    public ResponseDTO query(Integer id) {
        SalaryDeduct salaryDeduct = getById(id);
        if (salaryDeduct != null) {
            return Response.success(salaryDeduct);
        }
        return Response.error();
    }

    public ResponseDTO queryByDeptIdAndTypeNum(Integer deptId, Integer typeNum) {
        QueryWrapper<SalaryDeduct> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("dept_id", deptId).eq("type_num", typeNum);
        SalaryDeduct salaryDeduct = getOne(queryWrapper);
        if (salaryDeduct != null) {
            return Response.success(salaryDeduct);
        }
        return Response.error();
    }


    public ResponseDTO setSalaryDeduct(SalaryDeduct salaryDeduct) {
        QueryWrapper<SalaryDeduct> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("dept_id", salaryDeduct.getDeptId()).eq("type_num", salaryDeduct.getTypeNum());
        if (update(salaryDeduct, queryWrapper) || save(salaryDeduct)) {
            return Response.success();
        }
        return Response.error();
    }

    /**
     * 获取所有罚款类型
     * @return
     */
    public ResponseDTO queryAll() {
        return Response.success(EnumUtil.getEnumList(DeductEnum.class));
    }
}




