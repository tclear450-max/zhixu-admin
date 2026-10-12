package com.zhixu.staff.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.zhixu.menu.entity.Menu;
import com.zhixu.staff.entity.Staff;
import com.zhixu.security.StaffDetails;
import com.zhixu.common.enums.BusinessStatusEnum;
import com.zhixu.security.ServiceException;
import com.zhixu.menu.mapper.MenuMapper;
import com.zhixu.staff.mapper.StaffMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import jakarta.annotation.Resource;
import java.util.ArrayList;
import java.util.List;

@Service
public class StaffDetailsService implements UserDetailsService {

    @Autowired
    private StaffMapper staffMapper;

    @Autowired
    private MenuMapper menuMapper;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Staff staff = this.staffMapper.selectOne(new QueryWrapper<Staff>().eq("code", username));
        if (staff == null) {
            throw new ServiceException(BusinessStatusEnum.STAFF_NOT_EXIST);
        }
        if (staff.getStatus() == 0){
            throw new ServiceException(BusinessStatusEnum.STAFF_STATUS_ERROR);
        }
        // 查询员工的权限信息
        List<Menu> menuList = this.menuMapper.queryPermission(staff.getId());
        List<GrantedAuthority> list = new ArrayList<>();
        for (Menu menu : menuList) {
            if (menu.getPermission() == null || menu.getPermission().isEmpty()) {
                continue;
            }
            list.add(new SimpleGrantedAuthority(menu.getPermission()));
        }
        return new StaffDetails(username, staff.getPassword(), list,
                true, true, true, true);
    }
}
