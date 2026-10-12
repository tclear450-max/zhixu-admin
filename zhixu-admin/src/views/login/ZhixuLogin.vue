<template>
  <main class="zx-login">
    <section class="zx-story">
      <div class="zx-wordmark"><span class="zx-symbol">Z</span><span>知序 <small>ZHIXU</small></span></div>
      <div class="zx-story-body">
        <span class="zx-eyebrow">PEOPLE · PROCESS · KNOWLEDGE</span>
        <h1>让人事有序，<br>让知识流动。</h1>
        <p>从员工档案到每一次审批，从日常考勤到制度问答。<br>一个工作空间，连接组织里的每个人。</p>
        <div class="zx-capabilities"><span>01 / 组织与员工</span><span>02 / 考勤与审批</span><span>03 / 知识与问答</span></div>
        <div class="zx-orbit"><span class="zx-orbit-core">知序</span><span class="zx-orbit-label a">组织</span><span class="zx-orbit-label b">流程</span><span class="zx-orbit-label c">知识</span></div>
      </div>
      <div class="zx-story-footer">知序人事 · 让每一步工作，都有章可循</div>
    </section>
    <section class="zx-login-panel">
      <div class="zx-login-form">
        <span class="zx-eyebrow">WELCOME TO ZHIXU</span>
        <h2>欢迎回到知序</h2><p class="zx-muted">登录你的组织工作空间</p>
        <el-form :rules="rules" :model="staff" ref="loginForm" @submit.native.prevent="handleLogin">
          <label>工作账号</label>
          <el-form-item prop="code"><el-input placeholder="请输入账号" prefix-icon="el-icon-user" v-model.trim="staff.code" autocomplete="username" /></el-form-item>
          <label>密码</label>
          <el-form-item prop="password"><el-input placeholder="请输入密码" prefix-icon="el-icon-lock" show-password v-model="staff.password" autocomplete="current-password" /></el-form-item>
          <label>图形验证码</label>
          <div class="zx-code-row">
            <el-form-item prop="validateCode"><el-input placeholder="输入右侧数字" v-model.trim="staff.validateCode" maxlength="4" @keyup.enter.native="handleLogin" /></el-form-item>
            <button type="button" class="zx-code-image" @click="getCode" title="点击刷新验证码"><img ref="img" alt="验证码，点击刷新" /></button>
          </div>
          <el-button class="zx-submit" type="primary" :loading="submitting" @click="handleLogin">进入工作空间 <i class="el-icon-right" /></el-button>
        </el-form>
        <div class="zx-demo-info"><i class="el-icon-info" /><span>本地体验账号 <b>admin</b> · 密码 <b>Zx@123456</b><br>演示数据用于体验；请按图输入验证码。</span></div>
        <a class="zx-guide-link" href="/guide.html">查看使用指南 <i class="el-icon-top-right" /></a>
      </div>
      <footer>ZHIXU PEOPLE WORKSPACE <span>v1.0</span></footer>
    </section>
  </main>
</template>
<script>
import { login } from '@/api/login'
import { setValidateCode } from '@/utils/validateCode'
export default {
  name: 'ZhixuLogin',
  data () {
    return {
      submitting: false,
      staff: { code: 'admin', password: '', validateCode: '' },
      rules: {
        code: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 3, max: 64, message: '密码长度为3到64个字符', trigger: 'blur' }],
        validateCode: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
      }
    }
  },
  mounted () { this.getCode() },
  methods: {
    getCode () { setValidateCode(this.$refs.img) },
    handleLogin () {
      if (this.submitting) return
      this.$refs.loginForm.validate(async valid => {
        if (!valid) return
        this.submitting = true
        try {
          const response = await login(this.staff)
          if (response.code === 200) {
            this.$store.commit('staff/SET_STAFF', response.data)
            this.$store.commit('token/SET_AUTH', true)
            this.$message.success('欢迎回到知序')
            this.$router.push('/home')
          } else { this.$message.error(response.message); this.getCode() }
        } catch (error) { this.getCode() } finally { this.submitting = false }
      })
    }
  }
}
</script>
<style scoped>
.zx-login{min-height:100vh;display:grid;grid-template-columns:1.1fr 1fr;background:#f7f9fc;font-family:Inter,"Microsoft YaHei",sans-serif;color:#142b41}.zx-story{background:#102e38;color:#fff;padding:44px 64px;display:flex;flex-direction:column;position:relative;overflow:hidden}.zx-story:after{content:"";position:absolute;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(49,181,157,.14),transparent 70%);right:-260px;top:180px;pointer-events:none}.zx-wordmark{display:flex;align-items:center;gap:14px;font-size:24px;font-weight:700;letter-spacing:3px}.zx-wordmark small{font-size:11px;color:#99b7bf;margin-left:12px;letter-spacing:4px}.zx-symbol{display:inline-grid;place-items:center;width:40px;height:40px;background:#b9eadb;color:#123c3d;border-radius:12px;font-size:27px;letter-spacing:0}.zx-story-body{margin:auto 0;padding:66px 0 40px;position:relative}.zx-eyebrow{font-size:10px;letter-spacing:3px;color:#769c9b;font-weight:700}.zx-story h1{font-size:clamp(38px,4vw,61px);font-weight:600;line-height:1.4;margin:24px 0}.zx-story p{color:#afc5c9;font-size:14px;line-height:2.1}.zx-capabilities{display:flex;gap:22px;margin-top:28px;color:#8fafb6;font-size:11px}.zx-orbit{margin:45px auto 25px;width:240px;height:160px;position:relative;border:1px solid #355b63;border-radius:50%;transform:rotate(-16deg)}.zx-orbit:before{content:"";position:absolute;inset:-15px 36px;border:1px solid #355b63;border-radius:50%;transform:rotate(66deg)}.zx-orbit-core{position:absolute;left:87px;top:54px;padding:14px;background:#b9eadb;color:#153c3a;border-radius:16px;font-weight:600;transform:rotate(16deg)}.zx-orbit-label{position:absolute;background:#244852;padding:8px 15px;border-radius:20px;font-size:11px;transform:rotate(16deg)}.zx-orbit-label.a{left:-18px;top:35px}.zx-orbit-label.b{right:-18px;top:65px}.zx-orbit-label.c{left:75px;bottom:-10px}.zx-story-footer{font-size:11px;color:#71939c;letter-spacing:1px}.zx-login-panel{display:flex;flex-direction:column;padding:48px 10%;justify-content:center}.zx-login-form{width:100%;max-width:380px;margin:auto}.zx-login-form h2{font-size:30px;margin:15px 0 8px;letter-spacing:1px}.zx-muted{font-size:14px;color:#8c98a6;margin-bottom:38px}.zx-login-form label{font-size:12px;font-weight:600;display:block;margin:19px 0 9px}.zx-login-form /deep/ .el-input__inner{height:46px;border-radius:8px;border-color:#e1e7ed;background:#fff}.zx-login-form /deep/ .el-input__inner:focus{border-color:#278775}.zx-code-row{display:flex;gap:12px}.zx-code-row .el-form-item{flex:1}.zx-code-image{height:46px;width:108px;background:#fff;border:1px solid #e1e7ed;border-radius:8px;cursor:pointer}.zx-code-image img{width:90px;height:30px;object-fit:contain}.zx-submit{width:100%;height:47px;margin-top:10px;border-radius:8px;background:#207c6c;border-color:#207c6c;letter-spacing:1px}.zx-submit:hover{background:#176755;border-color:#176755}.zx-submit i{margin-left:20px}.zx-demo-info{margin-top:26px;padding:14px;background:#edf3f2;border-radius:9px;display:flex;gap:10px;font-size:11px;color:#6b8580;line-height:2}.zx-demo-info b{color:#345e54;font-weight:600}.zx-guide-link{display:block;color:#617b8b;font-size:12px;margin-top:20px;text-decoration:none}.zx-login-panel footer{font-size:9px;color:#9faab6;letter-spacing:2px;padding-top:38px}.zx-login-panel footer span{float:right}@media(max-width:900px){.zx-story{padding:35px}.zx-story h1{font-size:38px}.zx-capabilities{flex-direction:column;gap:12px}.zx-login-panel{padding:40px}}@media(max-width:650px){.zx-login{grid-template-columns:1fr}.zx-story{padding:24px}.zx-story-body{padding:20px 0}.zx-story h1{font-size:30px}.zx-orbit,.zx-capabilities,.zx-story-footer,.zx-story p{display:none}.zx-login-panel{min-height:540px;padding:38px 28px}}
</style>
