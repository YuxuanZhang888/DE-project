<template>
  <div class="flex items-center justify-center h-screen w-screen">
    <!-- 动态背景层 -->
    <div class="aurora-bg">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div class="w-full h-full flex items-center justify-center p-4 md:p-10">

      <!-- 主窗口：桌面应用比例 -->
      <div class="glass-window w-full max-w-[1200px] h-[90vh] rounded-[32px] flex overflow-hidden shadow-2xl relative">

        <!-- 左侧边栏 (Sidebar) -->
        <aside class="w-80 glass-sidebar flex flex-col hidden md:flex z-10">
          <!-- 侧边栏头部 -->
          <div class="h-20 flex items-center px-6 border-b border-white/20">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-white shadow-lg shadow-blue-500/30">
              <i class="ph-bold ph-chats-circle text-xl"></i>
            </div>
            <div class="ml-3">
              <h2 class="font-bold text-slate-800 tracking-tight">AI Assistant</h2>
              <span class="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Pro Edition</span>
            </div>
          </div>

          <!-- 导航列表 -->
          <div class="flex-1 p-4 space-y-2 overflow-y-auto no-scrollbar">
            <div class="px-4 py-3 rounded-2xl bg-white/50 border border-white/60 shadow-sm flex items-center gap-3 cursor-pointer">
              <div class="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_#22c55e]"></div>
              <span class="font-medium text-slate-800 text-sm">新对话</span>
            </div>
            <!-- 历史记录模拟 -->
            <div v-for="i in 3" :key="i" class="px-4 py-3 rounded-2xl hover:bg-white/30 border border-transparent hover:border-white/40 transition-all cursor-pointer flex items-center gap-3 group">
              <i class="ph ph-chat-text text-slate-500 group-hover:text-blue-600"></i>
              <div class="flex flex-col">
                <span class="text-sm text-slate-600 font-medium">历史会话 {{i}}</span>
                <span class="text-xs text-slate-400 truncate w-32">123.。。</span>
              </div>
            </div>
          </div>

          <!-- 底部用户信息 -->
          <div class="p-5 border-t border-white/20">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-slate-200 overflow-hidden border-2 border-white">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User">
              </div>
              <div class="flex-1">
                <div class="text-sm font-bold text-slate-700">Administrator</div>
                <div class="text-xs text-slate-500">AIchat Active</div>
              </div>
              <button class="w-8 h-8 rounded-full glass-btn flex items-center justify-center text-slate-600">
                <i class="ph-fill ph-gear"></i>
              </button>
            </div>
          </div>
        </aside>

        <!-- 右侧主聊天区 -->
        <main class="flex-1 flex flex-col relative bg-white/20">

          <!-- 顶部栏 -->
          <header class="h-20 flex items-center justify-between px-8 border-b border-white/30 backdrop-blur-md z-20">
            <div class="flex flex-col">
              <h1 class="text-lg font-bold text-slate-800">智能助手</h1>
              <div class="flex items-center gap-2 text-xs text-slate-500">
                <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                <span>在线</span>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button @click="clearChat" class="glass-btn px-4 py-2 rounded-xl text-sm font-medium text-slate-600 flex items-center gap-2" title="清空">
                <i class="ph ph-trash"></i>
                <span class="hidden sm:inline">清空</span>
              </button>
            </div>
          </header>

          <!-- 消息区域 -->
          <div ref="msgContainer" class="flex-1 overflow-y-auto p-6 md:p-10 space-y-6 no-scrollbar scroll-smooth">

            <!-- 欢迎状态 -->
            <div v-if="messages.length === 0" class="h-full flex flex-col items-center justify-center text-center opacity-60">
              <div class="w-24 h-24 rounded-[30px] bg-gradient-to-tr from-blue-100 to-white shadow-xl flex items-center justify-center mb-6 animate-[float_6s_infinite_ease-in-out]">
                <i class="ph-duotone ph-sparkle text-5xl text-blue-500"></i>
              </div>
              <h2 class="text-2xl font-bold text-slate-800 mb-2">欢迎回来</h2>
              <p class="text-slate-500 max-w-md">我是你的智能助手。你可以问我时间，或者直接开始聊天。</p>
            </div>

            <transition-group name="msg">
              <div v-for="msg in messages" :key="msg.id" class="flex w-full" :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'">

                <!-- 机器人头像 -->
                <div v-if="msg.sender === 'bot'" class="w-9 h-9 rounded-full bg-white/80 shadow-md flex items-center justify-center text-blue-500 mr-3 mt-auto flex-shrink-0">
                  <i class="ph-fill ph-robot text-lg"></i>
                </div>

                <div class="max-w-[80%] md:max-w-[65%] flex flex-col" :class="msg.sender === 'user' ? 'items-end' : 'items-start'">
                  <div class="px-5 py-3.5 rounded-3xl text-[15px] leading-relaxed shadow-sm backdrop-blur-md transition-all duration-300 hover:scale-[1.01]"
                       :class="msg.sender === 'user' ? 'bubble-user rounded-br-sm' : 'bubble-bot rounded-bl-sm'">
                    {{ msg.text }}
                  </div>
                  <span class="text-[10px] text-slate-400 mt-1.5 px-2 font-medium">{{ formatTime(msg.timestamp) }}</span>
                </div>

                <!-- 用户头像 -->
                <div v-if="msg.sender === 'user'" class="w-9 h-9 rounded-full bg-slate-200 overflow-hidden shadow-md ml-3 mt-auto flex-shrink-0 border border-white">
                  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User">
                </div>
              </div>

              <!-- 输入中动画 -->
              <div v-if="isTyping" key="typing" class="flex justify-start w-full">
                <div class="w-9 h-9 rounded-full bg-white/80 shadow-md flex items-center justify-center text-blue-500 mr-3 mt-auto">
                  <i class="ph-fill ph-robot text-lg"></i>
                </div>
                <div class="bubble-bot px-5 py-4 rounded-3xl rounded-bl-sm flex items-center gap-1.5">
                  <div class="w-1.5 h-1.5 bg-slate-500 rounded-full dot"></div>
                  <div class="w-1.5 h-1.5 bg-slate-500 rounded-full dot"></div>
                  <div class="w-1.5 h-1.5 bg-slate-500 rounded-full dot"></div>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- 底部输入区 -->
          <div class="p-6 md:px-10 md:pb-8 pt-2">
            <!-- 快捷指令 -->
            <div class="flex gap-2 mb-4 overflow-x-auto no-scrollbar pb-1">
              <button v-for="action in quickActions" :key="action"
                      @click="sendQuickMessage(action)"
                      :disabled="isTyping"
                      class="glass-btn px-4 py-1.5 rounded-full text-xs font-medium text-slate-600 whitespace-nowrap hover:text-blue-600 disabled:opacity-50">
                {{ action }}
              </button>
            </div>

            <!-- 输入框容器 -->
            <div class="glass-input w-full rounded-[28px] p-2 pl-2 flex items-center gap-2 relative">
              <button class="w-10 h-10 rounded-full hover:bg-black/5 transition-colors flex items-center justify-center text-slate-500">
                <i class="ph ph-plus text-xl"></i>
              </button>

              <input
                  v-model="inputMessage"
                  @keyup.enter="sendMessage"
                  type="text"
                  placeholder="输入消息..."
                  class="flex-1 bg-transparent h-10 outline-none text-slate-800 placeholder-slate-400/80 font-medium px-2"
                  :disabled="isTyping"
              >

              <button
                  @click="sendMessage"
                  :disabled="!inputMessage.trim() || isTyping"
                  class="h-10 px-6 rounded-full bg-blue-600 text-white shadow-lg shadow-blue-500/30 flex items-center justify-center hover:bg-blue-700 active:scale-95 transition-all duration-300 disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed"
              >
                <span v-if="!isTyping" class="font-medium text-sm">发送</span>
                <i v-else class="ph ph-spinner animate-spin"></i>
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue'

export default {
  name: 'App',
  setup() {
    const inputMessage = ref('')
    const messages = ref([])
    const isTyping = ref(false)
    const msgContainer = ref(null)

    const quickActions = [
      '👋 你好',
      '🤖 你是谁',
      '⏰ 现在几点',
      '🎨 切换主题'
    ]

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const scrollToBottom = async () => {
      await nextTick()
      if (msgContainer.value) {
        msgContainer.value.scrollTo({
          top: msgContainer.value.scrollHeight,
          behavior: 'smooth'
        })
      }
    }

    const generateResponse = (text) => {
      const lowerText = text.toLowerCase()
      if (lowerText.includes('你好') || lowerText.includes('hi')) return "你好呀！很高兴见到你，今天想聊点什么？"
      return "这个问题很有趣，让我想想... (智能模型正在思考)"
    }

    const sendMessage = () => {
      const text = inputMessage.value.trim()
      if (!text || isTyping.value) return

      // User Message
      messages.value.push({
        id: Date.now(),
        text: text,
        sender: 'user',
        timestamp: Date.now()
      })

      inputMessage.value = ''
      scrollToBottom()
      isTyping.value = true

      // Simulate AI Delay
      setTimeout(() => {
        const responseText = generateResponse(text)
        messages.value.push({
          id: Date.now() + 1,
          text: responseText,
          sender: 'bot',
          timestamp: Date.now()
        })
        isTyping.value = false
        scrollToBottom()
      }, 1200 + Math.random() * 800)
    }

    const sendQuickMessage = (text) => {
      const cleanText = text.split(' ').pop()
      inputMessage.value = cleanText
      sendMessage()
    }

    const clearChat = () => {
      messages.value = []
    }

    return {
      inputMessage,
      messages,
      isTyping,
      msgContainer,
      quickActions,
      formatTime,
      sendMessage,
      sendQuickMessage,
      clearChat
    }
  }
}
</script>

<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
  overflow: hidden;
  background: #000; /*以此衬托玻璃*/
  margin: 0;
  padding: 0;
}


.aurora-bg {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: -1;
  background: radial-gradient(circle at 50% 100%, #1e1e2e, #000);
  overflow: hidden;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 20s infinite ease-in-out alternate;
}

.orb-1 { width: 800px; height: 800px; background: #3b82f6; top: -200px; left: -200px; animation-duration: 25s; opacity: 0.4; }
.orb-2 { width: 600px; height: 600px; background: #60a5fa; bottom: -100px; right: -100px; animation-duration: 30s; opacity: 0.3; }
.orb-3 { width: 500px; height: 500px; background: #ffffff; top: 40%; left: 30%; animation-duration: 22s; opacity: 0.15; }

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(30px, 20px) scale(1.1); }
}


.glass-window {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(50px) saturate(180%);
  -webkit-backdrop-filter: blur(50px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-top: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow:
      0 50px 100px -20px rgba(0, 0, 0, 0.3),
      inset 0 0 20px rgba(255, 255, 255, 0.5);
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}


.glass-sidebar {
  background: rgba(255, 255, 255, 0.3);
  border-right: 1px solid rgba(255, 255, 255, 0.3);
}


.glass-btn {
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.4);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.glass-btn:hover {
  background: rgba(255, 255, 255, 0.6);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.glass-btn:active {
  transform: scale(0.95);
}

.glass-input {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}
.glass-input:focus {
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}


.msg-enter-active,
.msg-leave-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.msg-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
  filter: blur(10px);
}
.msg-leave-to {
  opacity: 0;
  transform: scale(0.9);
}


.bubble-user {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  box-shadow:
      0 4px 15px rgba(37, 99, 235, 0.4),
      inset 0 2px 4px rgba(255,255,255,0.4),
      inset 0 -2px 4px rgba(0,0,0,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.2);
}


.bubble-bot {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  color: #1e293b;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}


.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }


@keyframes typing {
  0%, 100% { transform: translateY(0); opacity: 0.5; }
  50% { transform: translateY(-4px); opacity: 1; }
}
.dot { animation: typing 1s infinite ease-in-out; }
.dot:nth-child(2) { animation-delay: 0.1s; }
.dot:nth-child(3) { animation-delay: 0.2s; }
</style>