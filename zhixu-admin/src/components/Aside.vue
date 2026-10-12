<template>
  <el-menu
    :default-active="$route.path"
    class="el-menu-vertical-demo"
    :collapse="isCollapsed"
    background-color="#102e38"
    text-color="#b4c9ce"
    active-text-color="#b9eadb"
  >
    <div class="zx-brand">
      <img
        src="/zhixu.svg"
        alt=""
        class="zx-brand-icon"
      />
      <span v-if="!isCollapsed" class="zx-brand-text">知序人事<small>ZHIXU WORKSPACE</small></span>
    </div>
    <div v-if="!isCollapsed" class="zx-nav-label">工作空间</div>
    <el-menu-item
      v-for="item in noChildren"
      :key="item.id"
      :index="'/' + item.code"
      @click="clickMenu(item,'/' + item.code)"
    >
      <i :class="'el-icon-' + item.icon"></i>
      <span slot="title"> {{ item.name }}</span>
    </el-menu-item>
    <el-submenu v-for="item in hasChildren" :key="item.id" :index="'/' + item.code">
      <template slot="title">
        <i :class="'el-icon-' + item.icon"></i>
        <span>{{ item.name }}</span>
      </template>
      <el-menu-item
        v-for="subItem in item.children"
        @click="clickMenu(subItem,'/'+item.code + '/' + subItem.code)"
        :key="subItem.id"
        :index="'/' + item.code + '/' + subItem.code"
      >
        <i :class="'el-icon-' + subItem.icon"></i>
        <span>{{ subItem.name }}</span>
      </el-menu-item>
    </el-submenu>
  </el-menu>
</template>

<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 232px;
  min-height: 400px;
}

.el-menu {
  height: 100%;
  border: none; /* 无边框 */

  h3 {
    color: #fff;
    text-align: center; /* 字体居中 */
    line-height: 48px; /* 行高 */
  }
}
</style>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Aside',
  methods: {
    clickMenu (menu, path) {
      // 使用编程式，路由导航
      this.$router.push({
        path: path // 点击菜单，进行跳转
      })
      this.$store.commit('tag/ADD_TAG', menu)
      if (window.innerWidth <= 780 && !this.isCollapsed) this.$store.commit('menu/COLLAPSE_MENU')
    }
  },
  computed: {
    ...mapGetters(['menuList', 'isCollapsed']),
    noChildren () {
      return this.menuList.filter(item => item.children.length === 0).sort((a, b) => (a.code === 'home' ? -1 : b.code === 'home' ? 1 : 0))
    },
    hasChildren () {
      return this.menuList.filter(item => item.children.length > 0) // 有子菜单
    }
  }
}
</script>
