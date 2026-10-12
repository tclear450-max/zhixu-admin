<template>
  <div class="zx-dashboard">
    <section class="zx-home-welcome">
      <div class="zx-welcome-copy"><span class="zx-home-kicker">A LITTLE ORDER, A BETTER WORKDAY</span><h2>每一天，从有序开始。</h2><p>你好，{{ staff.name }}。组织动态、工作流程和制度知识，都在这里。</p><el-button @click="$router.push('/chat')" icon="el-icon-chat-dot-round">打开制度问答 <i class="el-icon-right" /></el-button></div>
      <div class="zx-welcome-art" aria-hidden="true"><span class="zx-art-ring one"/><span class="zx-art-ring two"/><span class="zx-art-center">Z</span><span class="zx-art-note"><i class="el-icon-check" /> 有序协作</span></div>
    </section>
    <section class="zx-stat-grid" aria-label="组织与今日考勤统计">
      <div v-for="(item,index) in countData" :key="index" class="zx-stat-card" :class="{ 'zx-stat-alert': index > 3 && item.value > 0 }"><div class="zx-stat-top"><span>{{ item.name }}</span><i :class="'el-icon-' + item.icon" /></div><strong>{{ item.value }}<small>人</small></strong><span class="zx-stat-hint">{{ index >= 3 ? '今日考勤' : '组织成员' }}</span></div>
    </section>
    <div class="zx-dashboard-grid">
      <section class="zx-dashboard-left">
        <el-card class="zx-profile-card" shadow="never">
          <div class="zx-panel-heading"><h3>我的工作卡片</h3><span>{{ currentDateInfo }}</span></div>
          <div class="zx-profile-main"><img ref="img" src="" alt="头像"/><div><h3>{{ staff.name }}</h3><p>{{ staff.deptName }}</p></div><el-upload :action="uploadApi" :headers="headers" :show-file-list="false" :multiple="false" :on-success="handleUploadSuccess" :limit="1"><el-button icon="el-icon-edit" circle aria-label="修改头像" /></el-upload></div>
          <div class="zx-profile-detail"><span><i class="el-icon-location-outline" /> {{ staff.address || '尚未填写地址' }}</span><span><i class="el-icon-present" /> {{ staff.birthday || '尚未填写生日' }}</span></div>
        </el-card>
        <el-card class="zx-calendar-card" shadow="never">
          <div class="zx-panel-heading"><h3>我的考勤</h3><span>按月查看</span></div>
          <el-calendar v-model="attendanceData.date"><template slot="dateCell" slot-scope="{date, data}"><span>{{ date.getDate() }}</span><el-tag v-if="data.type==='current-month' && attendanceData.list[date.getDate() - 1]" :type="attendanceData.list[date.getDate() - 1].tagType">{{ attendanceData.list[date.getDate() - 1].message }}</el-tag></template></el-calendar>
        </el-card>
      </section>
      <section class="zx-dashboard-right">
        <el-card class="zx-chart-card zx-city-chart" shadow="never"><div class="zx-panel-heading"><div><h3>城市社保缴费比例</h3><p>比较各城市企业缴费标准</p></div><i class="el-icon-data-line" /></div><div ref="city" class="zx-chart-canvas" /></el-card>
        <div class="zx-chart-grid"><el-card class="zx-chart-card" shadow="never"><div class="zx-panel-heading"><h3>年度入职趋势</h3><span>{{ new Date().getFullYear() }}</span></div><div ref="staff" class="zx-chart-canvas" /></el-card><el-card class="zx-chart-card" shadow="never"><div class="zx-panel-heading"><h3>团队分布</h3><i class="el-icon-pie-chart" /></div><div ref="department" class="zx-chart-canvas" /></el-card></div>
        <div class="zx-knowledge-note"><span class="zx-knowledge-icon"><i class="el-icon-reading" /></span><div><h3>把制度变成随手可查的知识</h3><p>{{ product.demo ? '当前使用本地演示制度，回答附带文档来源。' : '根据已上传的组织知识与文档回答问题。' }}</p></div><el-button type="text" @click="$router.push('/chat')">开始提问 <i class="el-icon-right" /></el-button></div>
      </section>
    </div>
  </div>
</template>
<script>
import * as echarts from 'echarts'
import { queryCount, queryCity, queryStaff, queryAttendance, queryDepartment } from '@/api/home'
import { getUploadApi } from '@/api/docs'
import { edit, queryInfo } from '@/api/staff'
import { setAvatar } from '@/utils/avatar'
import { mapGetters } from 'vuex'
import request from '@/utils/request'

export default {
  name: 'Home',
  data () {
    return {
      product: { demo: true, model: '' },
      dayOfWeek: ['星期天', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
      attendanceData: {
        date: '',
        list: []
      },
      countData: [
        {
          name: '员工总数',
          value: 0,
          icon: 'user',
          color: '#409EFF'
        },
        {
          name: '状态正常',
          value: 0,
          icon: 'star-on',
          color: '#67C23A'
        },
        {
          name: '状态异常',
          value: 0,
          icon: 's-goods',
          color: '#F56C6C'
        },
        {
          name: '今日迟到',
          value: 0,
          icon: 'timer',
          color: '#409EFF'
        },
        {
          name: '今日早退',
          value: 0,
          icon: 'watch',
          color: '#67C23A'
        },
        {
          name: '今日旷工',
          value: 0,
          icon: 'lock',
          color: '#F56C6C'
        }
      ],
      staffOption: {
        title: {
          show: false,
          text: new Date().getFullYear() + '年员工入职情况',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}人',
          textStyle: {
            fontWeight: 'bold'
          }
        },
        xAxis: {
          type: 'category',
          data: []
        },
        yAxis: {
          type: 'value',
          name: '人数'
        },
        series: [
          {
            data: [],
            type: 'line'
          },
          {
            data: [],
            type: 'bar'
          }
        ]
      },
      cityOption: {
        title: {
          show: false,
          text: '部分城市社保缴费比例'
        },
        legend: {},
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            return '<a>' + params.name + '</a></a>' + '<br /><a>' + params.seriesName + ': ' + params.data[params.seriesIndex + 1] * 100 + '%</a>'
          },
          textStyle: {
            fontWeight: 'bold'
          }
        },
        dataset: {
          source: []
        },
        xAxis: { type: 'category' },
        yAxis: {
          type: 'value',
          name: '百分比',
          axisLabel: {
            formatter: function (val) {
              return val * 100 + '%'
            }
          }
        },
        series: [{ type: 'line' }, { type: 'line' }, { type: 'line' }, { type: 'line' }]
      },
      departmentOption: {
        title: {
          show: false,
          text: '员工分布情况',
          left: 'center'
        },
        legend: {
          left: 'center',
          top: 'bottom',
          orient: 'horizontal'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}人',
          textStyle: {
            fontWeight: 'bold'
          }
        },
        toolbox: {
          show: false,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        series: [
          {
            name: '团队分布',
            type: 'pie',
            radius: ['38%', '66%'],
            center: ['50%', '55%'],
            label: { // 饼图图形上的文本标签
              normal: {
                show: true,
                position: 'inner', // 标签的位置
                textStyle: {
                  fontWeight: 'bold'
                },
                formatter: '{d}%'
              }
            },
            itemStyle: {
              borderRadius: 3
            },
            data: []
          }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['staff', 'token']),
    headers () {
      return this.token ? { Authorization: 'Bearer ' + this.token } : {}
    },
    uploadApi () {
      return getUploadApi(this.staff.id)
    },
    currentDateInfo () {
      const date = new Date()
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      const currentDate = date.getDate()
      const day = date.getDay()
      return year + '年' + month + '月' + currentDate + '日' + ' ' + this.dayOfWeek[day]
    }
  },
  watch: {
    'attendanceData.date':
      function () {
        this.getStaffAttendance()
      },
    'staff.avatar': // 当头像被修改时，重新获取
      function () {
        setAvatar(this.$refs.img)
      },
    'staff.id':
      function (newVal) {
        if (newVal) {
          setAvatar(this.$refs.img)
        }
      }
  },
  mounted () {
    window.addEventListener('resize', this.resizeCharts)
    this.$nextTick(() => {
      setAvatar(this.$refs.img)
      if (window.ResizeObserver) {
        this.chartObserver = new ResizeObserver(this.resizeCharts)
        ;['city', 'staff', 'department'].forEach(name => this.chartObserver.observe(this.$refs[name]))
      }
    })
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.resizeCharts)
    if (this.chartObserver) this.chartObserver.disconnect()
    Object.values(this.charts || {}).forEach(chart => chart.dispose())
  },
  methods: {
    createChart (element) {
      const chart = echarts.getInstanceByDom(element) || echarts.init(element)
      this.charts = this.charts || []
      if (!this.charts.includes(chart)) this.charts.push(chart)
      chart.setOption({ color: ['#398577', '#8bb18b', '#d4b16d', '#8a9cb3'], textStyle: { fontFamily: 'Microsoft YaHei, sans-serif', color: '#81938b', fontSize: 10 }, grid: { left: 42, right: 16, top: 52, bottom: 35 } })
      return chart
    },
    resizeCharts () { Object.values(this.charts || {}).forEach(chart => chart.resize()) },
    loading () {
      queryInfo(this.staff.id).then(response => {
        if (response.code === 200) {
          this.$store.commit('staff/SET_STAFF', response.data)
          this.$nextTick(() => {
            setAvatar(this.$refs.img)
          })
        } else {
          this.$message.error('获取数据失败！')
        }
      })

      queryStaff().then(response => {
        if (response.code === 200) {
          const quarters = ['一季度', '二季度', '三季度', '四季度']
          this.staffOption.xAxis.data = quarters
          this.staffOption.series.forEach(item => {
            item.data = response.data
          })
          const staffChart = this.createChart(this.$refs.staff)
          staffChart.setOption(this.staffOption)
        } else {
          this.$message.error('获取数据失败！')
        }
      })

      // 获取统计数据
      queryCount().then(response => {
        if (response.code === 200) {
          this.countData[0].value = response.data.totalNum
          this.countData[1].value = response.data.normalNum
          this.countData[2].value = response.data.totalNum - response.data.normalNum
          this.countData[3].value = response.data.lateNum
          this.countData[4].value = response.data.leaveEarlyNum
          this.countData[5].value = response.data.absenteeismNum
        } else {
          this.$message.error('获取数据失败！')
        }
      })

      // 获取城市设社保数据
      queryCity().then(response => {
        if (response.code === 200) {
          const cityData = response.data.map(item => [item.name, item.comPensionRate, item.comMedicalRate, item.comUnemploymentRate, item.comMaternityRate])
          cityData.unshift(['product', '养老保险', '医疗保险', '失业保险', '生育保险'])
          this.cityOption.dataset.source = cityData
          const cityChart = this.createChart(this.$refs.city)
          cityChart.setOption(this.cityOption)
        } else {
          this.$message.error('获取数据失败！')
        }
      })

      // 获取当前月员工的考勤数据
      queryAttendance({ id: this.staff.id }).then(response => {
        if (response.code === 200) {
          this.attendanceData.list = response.data
        } else {
          this.$message.error('获取数据失败！')
        }
      })

      queryDepartment().then(response => {
        if (response.code === 200) {
          this.departmentOption.series[0].data = response.data
          const departmentChart = this.createChart(this.$refs.department)
          departmentChart.setOption(this.departmentOption)
        } else {
          this.$message.error('获取数据失败！')
        }
      })
    },
    // 获取指定月份员工的考勤数据
    getStaffAttendance () {
      const d = this.attendanceData.date
      let month = ''
      if (d.getMonth() < 9) {
        month = d.getFullYear() + '0' + (d.getMonth() + 1)
      } else {
        month = d.getFullYear() + '' + (d.getMonth() + 1)
      }
      queryAttendance({ id: this.staff.id, month: month }).then(response => {
        if (response.code === 200) {
          this.attendanceData.list = response.data
        } else {
          this.$message.error('获取数据失败！')
        }
      })
    },
    handleUploadSuccess (res) {
      if (res.code === 200) {
        // 修改头像
        edit({ id: this.staff.id, avatar: res.data.name }).then(response => {
          if (response.code === 200) {
            this.$message.success('修改头像成功！')
            this.$store.commit('staff/SET_AVATAR', res.data.name)
          } else {
            this.$message.error('修改头像失败！')
          }
        })
      } else {
        this.$message.error(res.message)
      }
    }
  },
  created () {
    this.loading()
    request.get('/product/info').then(response => { if (response.code === 200) this.product = response.data })
  }
}
</script>

<style>
.zx-home-welcome{background:linear-gradient(110deg,#163d47,#245b60);color:#fff;margin-top:20px;border-radius:14px;padding:28px 32px;display:flex;justify-content:space-between;align-items:center}.zx-home-kicker{font-size:9px;color:#98c4c0;letter-spacing:3px}.zx-home-welcome h2{font-size:26px;margin:12px 0;font-weight:500}.zx-home-welcome p{font-size:12px;color:#b4ccce}.zx-home-welcome small{font-size:10px;color:#89b7b1;display:block;margin-top:17px}.zx-home-actions{display:flex;flex-direction:column;gap:16px;align-items:flex-end}.zx-home-actions .el-button{background:#b9eadb;color:#224f48;border-color:#b9eadb;border-radius:8px}.zx-home-actions a{color:#b4ccce;font-size:11px;text-decoration:none}
.el-calendar-table .el-calendar-day {
  height: 54px;
}
</style>
