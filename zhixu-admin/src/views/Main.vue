<template>
  <el-container class="zx-shell" :class="{ 'zx-nav-collapsed': isCollapsed }">
    <el-aside width="auto" class="zx-aside">
      <!-- 引入侧边栏 -->
      <Aside/>
    </el-aside>
    <div v-if="!isCollapsed" class="zx-nav-backdrop" @click="collapseNavigation" />
    <el-container class="zx-content">
      <el-header height="72px">
        <!-- 引入顶栏 -->
        <Header/>
      </el-header>
      <!-- 引入标签栏 -->
      <Tag/>
      <el-main class="zx-main">
        <section class="zx-page-heading">
          <div><div class="zx-breadcrumb">知序工作空间 <span>/</span> {{ page.group }}</div><h1>{{ page.title }}</h1><p>{{ page.description }}</p></div>
          <span class="zx-page-mark"><i :class="'el-icon-' + page.icon" /></span>
        </section>
        <router-view/>
        <footer class="zx-page-footer"><span>ZHIXU · 让人事有序，让知识流动</span><a href="/guide.html" target="_blank" rel="noopener">使用指南 <i class="el-icon-top-right" /></a></footer>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>

import Aside from '../components/Aside.vue'
import Header from '../components/Header.vue'
import Tag from '../components/Tag.vue'
import { mapGetters } from 'vuex'

const pages = {
  home: ['工作总览', '工作台', '组织动态、工作流程与制度知识，在这里一目了然。', 'data-analysis'],
  chat: ['制度问答', '知识工作台', '从组织知识中寻找答案，让每一次决策都有据可循。', 'chat-dot-round'],
  staff: ['员工档案', '组织管理', '连接每一位同事，管理员工信息、任职状态与角色。', 'user'],
  department: ['部门与组织', '组织管理', '清晰的组织结构，让协作和职责更有序。', 'office-building'],
  docs: ['知识文档', '组织管理', '把分散的制度与文档，沉淀为可检索的组织知识。', 'document'],
  role: ['角色管理', '权限管理', '按职责配置访问权限，让每个人拥有合适的工作空间。', 'key'],
  menu: ['菜单权限', '权限管理', '管理功能入口与访问范围。', 's-grid'],
  attendance: ['考勤记录', '考勤管理', '查看出勤、异常与审批记录，掌握团队的工作节奏。', 'date'],
  leave: ['假期配置', '考勤管理', '统一管理团队的假期规则与可用额度。', 'sunny'],
  overtime: ['加班与调休', '考勤管理', '让额外投入有记录，让休息安排有依据。', 'time'],
  salary: ['薪资明细', '薪酬管理', '集中查看薪资与扣款明细，让每一项金额清晰可查。', 'wallet'],
  insurance: ['五险一金', '薪酬管理', '管理员工的社会保险与公积金配置。', 'umbrella'],
  city: ['参保城市', '薪酬管理', '集中维护各城市的参保基数与缴费比例。', 'location-outline']
}

export default {
  name: 'Main',
  components: {
    Aside,
    Header,
    Tag
  },
  computed: {
    ...mapGetters(['isCollapsed', 'menuList']),
    page () {
      const key = this.$route.path.split('/').filter(Boolean).pop() || 'home'
      const [title, group, description, icon] = pages[key] || ['工作空间', '知序人事', '连接组织、流程与知识。', 's-grid']
      return { title, group, description, icon }
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler () {
        for (const menu of this.menuList) {
          const candidates = menu.children.length ? menu.children.map(item => ({ item, path: '/' + menu.code + '/' + item.code })) : [{ item: menu, path: '/' + menu.code }]
          const found = candidates.find(candidate => candidate.path === this.$route.path)
          if (found) { this.$store.commit('tag/ADD_TAG', found.item); break }
        }
      }
    }
  },
  mounted () {
    if (window.innerWidth <= 780 && !this.isCollapsed) this.collapseNavigation()
  },
  methods: {
    collapseNavigation () { this.$store.commit('menu/COLLAPSE_MENU') }
  }
}
</script>
