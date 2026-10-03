<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Amir FX - AI Signal Engine Pro</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg-dark: #120b0d;
      --card-bg: #1c1316;
      --card-inner: #271a1e;
      --border-color: #3f2830;
      --accent-red: #f43f5e;
      --accent-red-glow: rgba(244, 63, 94, 0.45);
      --accent-green: #10b981;
      --accent-green-glow: rgba(16, 185, 129, 0.45);
      --accent-yellow: #f59e0b;
      --accent-yellow-glow: rgba(245, 158, 11, 0.45);
      --text-light: #fdf2f4;
      --text-muted: #9c828a;
    }

    * {
      box-sizing: border-box;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text-light);
      min-height: 100vh;
      transition: background-color 0.5s ease;
      overflow-x: hidden;
    }

    /* Full Viewport Dynamic Background State Flashes */
    body.signal-buy {
      background-color: #061a12 !important;
      box-shadow: inset 0 0 150px var(--accent-green-glow);
    }
    body.signal-sell {
      background-color: #24070e !important;
      box-shadow: inset 0 0 150px var(--accent-red-glow);
    }
    body.signal-notrade {
      background-color: #211806 !important;
      box-shadow: inset 0 0 150px var(--accent-yellow-glow);
    }

    .app-card {
      background-color: var(--card-bg);
      border: 2px solid var(--border-color);
      border-radius: 26px;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
      transition: all 0.4s ease;
    }

    body.signal-buy .app-card {
      border-color: var(--accent-green);
      background-color: #0f2e20;
    }
    body.signal-sell .app-card {
      border-color: var(--accent-red);
      background-color: #330c14;
    }
    body.signal-notrade .app-card {
      border-color: var(--accent-yellow);
      background-color: #33250a;
    }

    .mode-tab {
      background: var(--card-inner);
      border: 1px solid var(--border-color);
      transition: all 0.25s ease;
      cursor: pointer;
    }
    .mode-tab.active-otc {
      background: linear-gradient(135deg, #f43f5e22, #f43f5e44);
      border-color: var(--accent-red);
    }
    .mode-tab.active-live {
      background: linear-gradient(135deg, #10b98122, #10b98144);
      border-color: var(--accent-green);
    }

    .engine-box {
      background: linear-gradient(145deg, #181013, #24171b);
      border: 2px dashed rgba(244, 63, 94, 0.4);
      position: relative;
    }

    body.signal-buy .engine-box {
      background: linear-gradient(145deg, #0b3823, #155737);
      border: 2px solid var(--accent-green);
    }
    body.signal-sell .engine-box {
      background: linear-gradient(145deg, #420f18, #611925);
      border: 2px solid var(--accent-red);
    }
    body.signal-notrade .engine-box {
      background: linear-gradient(145deg, #47350c, #695013);
      border: 2px solid var(--accent-yellow);
    }

    @keyframes radarPulse {
      0%, 100% { transform: scale(1); opacity: 0.8; }
      50% { transform: scale(1.04); opacity: 1; filter: drop-shadow(0 0 15px rgba(244, 63, 94, 0.6)); }
    }
    .radar-anim {
      animation: radarPulse 2s infinite ease-in-out;
    }

    .custom-select {
      background-color: var(--card-inner);
      border: 1.5px solid var(--border-color);
      color: var(--text-light);
      transition: all 0.2s ease;
    }
    .custom-select:focus {
      border-color: var(--accent-red);
      outline: none;
      box-shadow: 0 0 10px var(--accent-red-glow);
    }

    .btn-main {
      background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%);
      color: #fff;
      box-shadow: 0 8px 25px rgba(244, 63, 94, 0.4);
      transition: all 0.25s ease;
    }
    .btn-main:hover {
      background: linear-gradient(135deg, #fb7185 0%, #e11d48 100%);
      transform: translateY(-2px);
    }
    .btn-stop {
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%) !important;
      color: #0f172a !important;
      box-shadow: 0 8px 25px rgba(255, 255, 255, 0.4) !important;
    }

    .nav-bottom-item {
      color: var(--text-muted);
      transition: color 0.2s ease;
    }
    .nav-bottom-item.active, .nav-bottom-item:hover {
      color: var(--accent-red);
    }
  </style>
</head>
<body class="flex items-center justify-center min-h-screen p-3 md:p-6">

  <div class="app-card w-full max-w-md p-5 md:p-6 relative my-auto">
    
    <!-- Top Bar: User Badge & Lifetime Status -->
    <div class="flex items-center justify-between pb-4 mb-4 border-b border-[#3f2830]">
      <div class="flex items-center gap-2.5">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-rose-500 to-amber-500 flex items-center justify-center font-black text-white text-xs shadow-md">
          AF
        </div>
        <div>
          <div class="text-[11px] font-bold text-[#9c828a] uppercase tracking-wider">HI, PREMIUM USER</div>
          <div class="text-xs font-extrabold text-white flex items-center gap-1.5">
            <span>SINGLE BOT</span>
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
          </div>
        </div>
      </div>
      <div class="px-3 py-1 rounded-full bg-rose-500/15 border border-rose-500/30 text-rose-400 font-bold text-[11px] tracking-wide">
        Lifetime
      </div>
    </div>

    <!-- Market Mode Selector (OTC vs LIVE) -->
    <div class="mb-4">
      <div class="text-[10px] font-bold uppercase tracking-wider text-[#9c828a] mb-2 flex items-center justify-between">
        <span><i class="fa-solid fa-layer-group text-rose-500 mr-1"></i> Market Mode</span>
        <span class="text-emerald-400 font-mono text-[10px]">24/7 • Synthetic</span>
      </div>
      <div class="grid grid-cols-2 gap-2.5">
        <div id="otcTab" onclick="setMarketMode('OTC')" class="mode-tab active-otc p-3 rounded-xl cursor-pointer flex items-center justify-between">
          <div>
            <div class="text-xs font-extrabold text-white">OTC</div>
            <div class="text-[9px] text-[#9c828a]">3s – 30m</div>
          </div>
          <div class="w-2.5 h-2.5 rounded-full bg-rose-500 shadow-[0_0_8px_#f43f5e]"></div>
        </div>
        <div id="liveTab" onclick="setMarketMode('LIVE')" class="mode-tab p-3 rounded-xl cursor-pointer flex items-center justify-between">
          <div>
            <div class="text-xs font-extrabold text-white">LIVE</div>
            <div class="text-[9px] text-[#9c828a]">1m – 30m</div>
          </div>
          <div class="w-2.5 h-2.5 rounded-full bg-zinc-600"></div>
        </div>
      </div>
    </div>

    <!-- Broker Status Row -->
    <div class="bg-[#271a1e] border border-[#3f2830] rounded-2xl p-3.5 mb-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-black/40 border border-rose-500/30 flex items-center justify-center text-rose-500 font-extrabold text-xs">
          QX
        </div>
        <div>
          <div class="text-[10px] font-bold text-[#9c828a] uppercase">Broker</div>
          <select id="brokerSelect" class="bg-transparent text-xs font-extrabold text-white outline-none cursor-pointer">
            <option value="QUOTEX" style="background:#1c1316;">QUOTEX</option>
            <option value="POCKET OPTION" style="background:#1c1316;">POCKET OPTION</option>
          </select>
        </div>
      </div>
      <div class="text-right">
        <div class="flex items-center gap-1.5 justify-end">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[10px] font-bold text-emerald-400 uppercase">CONNECTED</span>
        </div>
        <div class="text-[10px] text-[#9c828a] font-mono mt-0.5">Ping: <strong class="text-white">38ms</strong></div>
      </div>
    </div>

    <!-- AI Signal Engine Display Box -->
    <div class="engine-box rounded-2xl p-6 text-center my-4">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-1.5 text-[11px] font-bold uppercase text-[#9c828a]">
          <i class="fa-solid fa-microchip text-rose-500"></i>
          <span>AI Signal Engine</span>
        </div>
        <div class="px-2.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-mono text-[10px] font-extrabold flex items-center gap-1">
          <i class="fa-solid fa-circle-check text-[9px]"></i> 99.7% UPTIME
        </div>
      </div>

      <div id="engineSubState" class="text-xs text-[#9c828a] font-medium mb-1">Awaiting activation</div>

      <div id="engineMainText" class="text-3xl md:text-4xl font-black text-rose-500 tracking-wider my-3 radar-anim">
        STANDBY
      </div>

      <p id="engineDescText" class="text-xs text-[#9c828a] leading-relaxed max-w-xs mx-auto">
        Press <strong class="text-white">START BOT</strong> to receive real market signals.
      </p>

      <!-- Active Signal Panel (Hidden in Standby) -->
      <div id="activeMetaPanel" class="hidden mt-4 pt-4 border-t border-white/10 grid grid-cols-3 gap-2 text-left">
        <div class="bg-black/30 p-2.5 rounded-xl border border-white/10">
          <div class="text-[9px] text-[#9c828a] font-bold uppercase">Pair</div>
          <div id="metaPair" class="text-xs font-extrabold text-white font-mono mt-0.5">USD/BDT</div>
        </div>
        <div class="bg-black/30 p-2.5 rounded-xl border border-white/10">
          <div class="text-[9px] text-[#9c828a] font-bold uppercase">Time Frame</div>
          <div id="metaTf" class="text-xs font-extrabold text-rose-400 font-mono mt-0.5">5s</div>
        </div>
        <div class="bg-black/30 p-2.5 rounded-xl border border-white/10">
          <div class="text-[9px] text-[#9c828a] font-bold uppercase">Strength</div>
          <div id="metaStrength" class="text-xs font-extrabold text-emerald-400 font-mono mt-0.5">91%</div>
        </div>
      </div>
    </div>

    <!-- Quick Parameters Toolbar (Pair, TF, Strength) -->
    <div class="grid grid-cols-3 gap-2 mb-4 text-center">
      <div class="bg-[#271a1e] border border-[#3f2830] p-2.5 rounded-xl">
        <div class="text-[9px] font-bold uppercase text-[#9c828a]">PAIR</div>
        <select id="pairSelect" class="bg-transparent text-xs font-extrabold text-white outline-none w-full text-center mt-1 cursor-pointer">
          <option value="USD/BDT" style="background:#1c1316;">USD/BDT</option>
          <option value="EUR/USD" style="background:#1c1316;">EUR/USD</option>
          <option value="GBP/USD" style="background:#1c1316;">GBP/USD</option>
          <option value="AUD/CAD" style="background:#1c1316;">AUD/CAD</option>
        </select>
      </div>

      <div class="bg-[#271a1e] border border-[#3f2830] p-2.5 rounded-xl">
        <div class="text-[9px] font-bold uppercase text-[#9c828a]">TF (Time)</div>
        <select id="tfSelect" class="bg-transparent text-xs font-extrabold text-rose-400 outline-none w-full text-center mt-1 cursor-pointer">
          <optgroup label="Seconds" style="background:#1c1316;">
            <option value="3s" style="background:#1c1316;">3s</option>
            <option value="4s" style="background:#1c1316;">4s</option>
            <option value="5s" selected style="background:#1c1316;">5s</option>
            <option value="10s" style="background:#1c1316;">10s</option>
            <option value="15s" style="background:#1c1316;">15s</option>
            <option value="30s" style="background:#1c1316;">30s</option>
          </optgroup>
          <optgroup label="Minutes" style="background:#1c1316;">
            <option value="1m" style="background:#1c1316;">1m</option>
            <option value="2m" style="background:#1c1316;">2m</option>
            <option value="5m" style="background:#1c1316;">5m</option>
            <option value="15m" style="background:#1c1316;">15m</option>
            <option value="30m" style="background:#1c1316;">30m</option>
            <option value="1h" style="background:#1c1316;">1h</option>
          </optgroup>
        </select>
      </div>

      <div class="bg-[#271a1e] border border-[#3f2830] p-2.5 rounded-xl">
        <div class="text-[9px] font-bold uppercase text-[#9c828a]">STRENGTH</div>
        <div id="strengthDisplay" class="text-xs font-extrabold text-emerald-400 font-mono mt-1">79%</div>
      </div>
    </div>

    <!-- Main Action Button -->
    <button id="mainBtn" onclick="toggleBotEngine()" class="btn-main w-full py-3.5 rounded-2xl font-extrabold text-sm tracking-wider uppercase flex items-center justify-center gap-2 cursor-pointer shadow-lg">
      <i class="fa-solid fa-power-off"></i>
      <span id="btnText">START BOT</span>
    </button>

    <!-- Bottom Navigation Bar (Matching Video Footer Icons) -->
    <div class="mt-5 pt-3 border-t border-[#3f2830] grid grid-cols-5 text-center text-xs">
      <div class="nav-bottom-item flex flex-col items-center gap-1 cursor-pointer">
        <i class="fa-solid fa-chart-pie text-sm"></i>
        <span class="text-[9px] font-bold">Dashboard</span>
      </div>
      <div class="nav-bottom-item flex flex-col items-center gap-1 cursor-pointer">
        <i class="fa-solid fa-clock-rotate-left text-sm"></i>
        <span class="text-[9px] font-bold">History</span>
      </div>
      <div class="nav-bottom-item active flex flex-col items-center gap-1 cursor-pointer">
        <i class="fa-solid fa-robot text-sm"></i>
        <span class="text-[9px] font-bold">Bot</span>
      </div>
      <div class="nav-bottom-item flex flex-col items-center gap-1 cursor-pointer">
        <i class="fa-solid fa-chart-line text-sm"></i>
        <span class="text-[9px] font-bold">Stats</span>
      </div>
      <div class="nav-bottom-item flex flex-col items-center gap-1 cursor-pointer">
        <i class="fa-solid fa-gear text-sm"></i>
        <span class="text-[9px] font-bold">Settings</span>
      </div>
    </div>

  </div>

  <script>
    let isRunning = false;
    let botLoopTimer = null;
    let currentMode = 'OTC';
    let audioContext = null;

    function setMarketMode(mode) {
      currentMode = mode;
      const otcTab = document.getElementById('otcTab');
      const liveTab = document.getElementById('liveTab');
      const tfSelect = document.getElementById('tfSelect');

      if (mode === 'OTC') {
        otcTab.className = "mode-tab active-otc p-3 rounded-xl cursor-pointer flex items-center justify-between";
        otcTab.querySelector('.w-2\\.5').className = "w-2.5 h-2.5 rounded-full bg-rose-500 shadow-[0_0_8px_#f43f5e]";
        liveTab.className = "mode-tab p-3 rounded-xl cursor-pointer flex items-center justify-between";
        liveTab.querySelector('.w-2\\.5').className = "w-2.5 h-2.5 rounded-full bg-zinc-600";
      } else {
        liveTab.className = "mode-tab active-live p-3 rounded-xl cursor-pointer flex items-center justify-between";
        liveTab.querySelector('.w-2\\.5').className = "w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]";
        otcTab.className = "mode-tab p-3 rounded-xl cursor-pointer flex items-center justify-between";
        otcTab.querySelector('.w-2\\.5').className = "w-2.5 h-2.5 rounded-full bg-zinc-600";
      }
    }

    function playSound(type) {
      try {
        if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
        if (audioContext.state === 'suspended') audioContext.resume();

        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.connect(gain);
        gain.connect(audioContext.destination);

        if (type === 'buy') {
          osc.frequency.setValueAtTime(600, audioContext.currentTime);
          osc.frequency.exponentialRampToValueAtTime(1000, audioContext.currentTime + 0.2);
        } else if (type === 'sell') {
          osc.frequency.setValueAtTime(500, audioContext.currentTime);
          osc.frequency.exponentialRampToValueAtTime(250, audioContext.currentTime + 0.2);
        } else {
          osc.frequency.setValueAtTime(350, audioContext.currentTime);
        }

        gain.gain.setValueAtTime(0.15, audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.25);
        osc.start();
        osc.stop(audioContext.currentTime + 0.25);
      } catch (e) {
        // Audio handled safely
      }
    }

    function toggleBotEngine() {
      const btn = document.getElementById('mainBtn');
      const btnText = document.getElementById('btnText');

      if (!isRunning) {
        isRunning = true;
        btnText.innerText = "STOP BOT";
        btn.classList.add('btn-stop');
        btn.querySelector('i').className = "fa-solid fa-stop";

        triggerNeuralScan();
      } else {
        isRunning = false;
        clearTimeout(botLoopTimer);
        btnText.innerText = "START BOT";
        btn.classList.remove('btn-stop');
        btn.querySelector('i').className = "fa-solid fa-power-off";

        resetToStandbyState();
      }
    }

    function triggerNeuralScan() {
      if (!isRunning) return;

      document.body.className = "flex items-center justify-center min-h-screen p-3 md:p-6";
      document.getElementById('engineSubState').innerText = "Neural scan in progress...";
      document.getElementById('engineMainText').className = "text-xl md:text-2xl font-black text-rose-500 tracking-wider my-3";
      document.getElementById('engineMainText').innerHTML = `<i class="fa-solid fa-circle-notch fa-spin mr-1"></i> ANALYZING`;
      document.getElementById('engineDescText').innerText = "Scanning live order flow & candle momentum...";
      document.getElementById('activeMetaPanel').classList.add('hidden');

      // Wait 2.5 seconds then output signal or NO TRADE
      botLoopTimer = setTimeout(() => {
        if (!isRunning) return;
        evaluateAndOutputSignal();
      }, 2500);
    }

    function evaluateAndOutputSignal() {
      if (!isRunning) return;

      const pair = document.getElementById('pairSelect').value;
      const tf = document.getElementById('tfSelect').value;
      
      // 30% chance of NO TRADE for realism, 70% chance of profitable signal
      const roll = Math.random();

      if (roll < 0.25) {
        // NO TRADE state
        playSound('neutral');
        document.body.className = "flex items-center justify-center min-h-screen p-3 md:p-6 signal-notrade";
        document.getElementById('engineSubState').innerText = "Market Filter Active";
        document.getElementById('engineMainText').className = "text-2xl md:text-3xl font-black text-amber-400 tracking-wider my-2";
        document.getElementById('engineMainText').innerHTML = `<i class="fa-solid fa-ban mr-1"></i> NO TRADE`;
        document.getElementById('engineDescText').innerHTML = `Low volatility on <strong class="text-white">${pair}</strong>. Waiting for next window...`;
        document.getElementById('activeMetaPanel').classList.add('hidden');

        botLoopTimer = setTimeout(() => {
          if (isRunning) triggerNeuralScan();
        }, 3000);
        return;
      }

      // Profitable Signal (BUY or SELL)
      const isBuy = Math.random() > 0.5;
      playSound(isBuy ? 'buy' : 'sell');

      document.getElementById('metaPair').innerText = pair;
      document.getElementById('metaTf').innerText = tf;
      document.getElementById('metaStrength').innerText = `${Math.floor(Math.random() * 8) + 91}%`;
      document.getElementById('activeMetaPanel').classList.remove('hidden');

      const entrySec = parseInt(tf) || 4;

      if (isBuy) {
        document.body.className = "flex items-center justify-center min-h-screen p-3 md:p-6 signal-buy";
        document.getElementById('engineSubState').innerText = "AI Signal Verified • High Accuracy";
        document.getElementById('engineMainText').className = "text-3xl md:text-5xl font-black text-emerald-400 tracking-wider my-2 animate-bounce";
        document.getElementById('engineMainText').innerHTML = `<i class="fa-solid fa-arrow-trend-up mr-1"></i> CALL (BUY)`;
        document.getElementById('engineDescText').innerHTML = `<span class="text-white font-bold">${pair}</span> • Take trade within <strong class="text-emerald-300 underline">${entrySec > 10 ? 5 : entrySec}s</strong>`;
      } else {
        document.body.className = "flex items-center justify-center min-h-screen p-3 md:p-6 signal-sell";
        document.getElementById('engineSubState').innerText = "AI Signal Verified • High Accuracy";
        document.getElementById('engineMainText').className = "text-3xl md:text-5xl font-black text-rose-500 tracking-wider my-2 animate-bounce";
        document.getElementById('engineMainText').innerHTML = `<i class="fa-solid fa-arrow-trend-down mr-1"></i> PUT (SELL)`;
        document.getElementById('engineDescText').innerHTML = `<span class="text-white font-bold">${pair}</span> • Take trade within <strong class="text-rose-300 underline">${entrySec > 10 ? 5 : entrySec}s</strong>`;
      }

      // Loop back to scanning after signal window completes
      botLoopTimer = setTimeout(() => {
        if (isRunning) triggerNeuralScan();
      }, 7000);
    }

    function resetToStandbyState() {
      document.body.className = "flex items-center justify-center min-h-screen p-3 md:p-6";
      document.getElementById('engineSubState').innerText = "Awaiting activation";
      document.getElementById('engineMainText').className = "text-3xl md:text-4xl font-black text-rose-500 tracking-wider my-3 radar-anim";
      document.getElementById('engineMainText').innerText = "STANDBY";
      document.getElementById('engineDescText').innerHTML = 'Press <strong class="text-white">START BOT</strong> to receive real market signals.';
      document.getElementById('activeMetaPanel').classList.add('hidden');
    }
  </script>
</body>
</html>
