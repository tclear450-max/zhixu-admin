package com.zhixu.role.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zhixu.role.entity.RoleMenu;
import com.zhixu.role.entity.StaffRole;
import com.zhixu.common.enums.BusinessStatusEnum;
import com.zhixu.security.ServiceException;
import com.zhixu.role.mapper.RoleMenuMapper;
import com.zhixu.common.dto.Response;
import com.zhixu.common.dto.ResponseDTO;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * <p>
 * 服务类
 * </p>
 *
 * @since 2022-02-28
 */
@Service
public class RoleMenuService extends ServiceImpl<RoleMenuMapper, RoleMenu> {

    /**
     * 为角色设置菜单
     *
     * @param roleId
     * @param menuIds
     * @return
     */
    @Transactional
    public ResponseDTO setMenu(Integer roleId, List<Integer> menuIds) {
        remove(new QueryWrapper<RoleMenu>().eq("role_id", roleId));
        for (Integer menuId : menuIds) {
            save(new RoleMenu().setRoleId(roleId).setMenuId(menuId));
        }
        return Response.success();
    }

    /**
     * 获取角色的菜单
     *
     * @param roleId
     * @return
     */
    public ResponseDTO queryByRoleId(Integer roleId) {
        List<RoleMenu> list = list(new QueryWrapper<RoleMenu>().eq("role_id", roleId));
        return Response.success(list);
    }


}




