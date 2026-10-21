import os

print("Building enhanced 3D racing game...")

with open("arivu_base64.txt", "r", encoding="ascii") as f:
    b64_image = f.read().strip()

print(f"Loaded base64 length: {len(b64_image)}")

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Arivu Super Turbo 3D - Grand Prix</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }
    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #080a12;
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      color: #fff;
    }
    #game-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
    }

    /* UI Overlay */
    #ui-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 10;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 16px 22px;
    }

    .interactive {
      pointer-events: auto;
    }

    /* Top Bar */
    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      width: 100%;
    }

    .brand-badge {
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 7px 18px;
      border-radius: 40px;
      border: 1.5px solid rgba(0, 240, 255, 0.6);
      box-shadow: 0 4px 25px rgba(0, 240, 255, 0.35);
      cursor: pointer;
    }
    .brand-avatar {
      width: 46px;
      height: 46px;
      border-radius: 50%;
      border: 2px solid #00f0ff;
      object-fit: cover;
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.8);
    }
    .brand-text h2 {
      font-size: 16px;
      font-weight: 900;
      letter-spacing: 1.2px;
      background: linear-gradient(90deg, #00f0ff, #ff007b);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-transform: uppercase;
    }
    .brand-text p {
      font-size: 11px;
      color: #94a3b8;
      font-weight: 700;
      letter-spacing: 0.6px;
    }

    /* Race Stats */
    .race-stats {
      display: flex;
      gap: 12px;
    }
    .stat-pill {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      padding: 7px 15px;
      text-align: center;
      min-width: 85px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .stat-pill.pos-pill {
      border-color: rgba(255, 215, 0, 0.8);
      box-shadow: 0 0 18px rgba(255, 215, 0, 0.4);
    }
    .stat-label {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #94a3b8;
      font-weight: 800;
    }
    .stat-val {
      font-size: 22px;
      font-weight: 900;
      color: #fff;
      font-family: 'Courier New', Courier, monospace;
    }
    .pos-pill .stat-val {
      color: #ffd700;
      text-shadow: 0 0 12px rgba(255, 215, 0, 0.7);
    }

    /* Top Right Buttons */
    .top-actions {
      display: flex;
      gap: 10px;
    }
    .icon-btn {
      background: rgba(15, 23, 42, 0.85);
      border: 1.5px solid rgba(0, 240, 255, 0.5);
      color: #fff;
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .icon-btn:hover {
      background: rgba(0, 240, 255, 0.35);
      transform: scale(1.06);
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
    }

    /* Toast Notifications */
    .toast-container {
      position: absolute;
      top: 90px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      pointer-events: none;
    }
    .toast-msg {
      background: rgba(10, 14, 26, 0.92);
      border-left: 5px solid #00f0ff;
      padding: 10px 24px;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 900;
      letter-spacing: 1px;
      color: #fff;
      text-transform: uppercase;
      animation: toastPop 2.2s forwards;
      box-shadow: 0 8px 30px rgba(0, 240, 255, 0.45);
    }
    .toast-msg.gold {
      border-color: #ffd700;
      color: #ffd700;
      box-shadow: 0 8px 30px rgba(255, 215, 0, 0.5);
    }
    .toast-msg.boost {
      border-color: #ff007b;
      color: #ff007b;
      box-shadow: 0 8px 30px rgba(255, 0, 123, 0.5);
    }
    @keyframes toastPop {
      0% { opacity: 0; transform: translateY(-15px) scale(0.92); }
      15% { opacity: 1; transform: translateY(0) scale(1.05); }
      25% { transform: scale(1); }
      80% { opacity: 1; transform: translateY(0); }
      100% { opacity: 0; transform: translateY(-20px) scale(0.92); }
    }

    /* Drift Notification */
    .drift-alert {
      position: absolute;
      bottom: 210px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 28px;
      font-weight: 900;
      color: #ffd700;
      text-shadow: 0 0 20px rgba(255, 215, 0, 0.9);
      letter-spacing: 2px;
      font-style: italic;
      display: none;
      pointer-events: none;
    }

    /* Bottom Section */
    .bottom-bar {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      width: 100%;
    }

    /* Radar / Minimap */
    .radar-box {
      width: 145px;
      height: 145px;
      background: rgba(10, 15, 30, 0.9);
      border: 1.5px solid rgba(0, 240, 255, 0.5);
      border-radius: 18px;
      padding: 6px;
      position: relative;
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(12px);
    }
    #radar-canvas {
      width: 100%;
      height: 100%;
      display: block;
    }
    .radar-title {
      position: absolute;
      top: 6px;
      left: 10px;
      font-size: 9px;
      color: #00f0ff;
      font-weight: 900;
      letter-spacing: 1px;
    }

    /* Dashboard */
    .dashboard-cluster {
      display: flex;
      align-items: flex-end;
      gap: 20px;
      background: rgba(15, 23, 42, 0.9);
      border: 1.5px solid rgba(0, 240, 255, 0.4);
      border-radius: 22px;
      padding: 14px 24px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(14px);
    }

    /* Speedometer */
    .speedo-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }
    .speedo-dial {
      width: 130px;
      height: 75px;
      position: relative;
      overflow: hidden;
    }
    .speedo-svg {
      width: 130px;
      height: 130px;
      transform: rotate(-90deg);
    }
    .speedo-bg {
      fill: none;
      stroke: rgba(255, 255, 255, 0.12);
      stroke-width: 10;
      stroke-dasharray: 235;
      stroke-dashoffset: 78;
    }
    .speedo-fill {
      fill: none;
      stroke: url(#speedoGradient);
      stroke-width: 10;
      stroke-dasharray: 235;
      stroke-dashoffset: 235;
      transition: stroke-dashoffset 0.08s ease-out;
      stroke-linecap: round;
    }
    .speed-number {
      position: absolute;
      bottom: 2px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 34px;
      font-weight: 900;
      font-family: 'Courier New', Courier, monospace;
      color: #fff;
      text-shadow: 0 0 15px rgba(0, 240, 255, 0.85);
      line-height: 1;
    }
    .speed-unit {
      font-size: 11px;
      color: #94a3b8;
      font-weight: 800;
      letter-spacing: 1.2px;
      margin-top: 2px;
    }

    /* Gear & RPM */
    .gear-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 0 8px;
      border-left: 1px solid rgba(255, 255, 255, 0.15);
      border-right: 1px solid rgba(255, 255, 255, 0.15);
    }
    .gear-label {
      font-size: 10px;
      color: #64748b;
      font-weight: 800;
    }
    .gear-num {
      font-size: 32px;
      font-weight: 900;
      color: #00f0ff;
      text-shadow: 0 0 12px rgba(0, 240, 255, 0.7);
      line-height: 1;
      margin: 2px 0;
    }
    .rpm-bar-wrap {
      width: 52px;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
    }
    .rpm-bar-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #00f0ff, #ffd700, #ff0055);
      transition: width 0.08s;
    }

    /* Nitro Meter */
    .nitro-wrap {
      display: flex;
      flex-direction: column;
      gap: 5px;
      min-width: 105px;
    }
    .nitro-label {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 800;
      color: #00f0ff;
      letter-spacing: 1px;
    }
    .nitro-track {
      width: 100%;
      height: 16px;
      background: rgba(0, 0, 0, 0.7);
      border: 1px solid rgba(0, 240, 255, 0.6);
      border-radius: 8px;
      overflow: hidden;
      padding: 2px;
    }
    .nitro-fill {
      height: 100%;
      width: 100%;
      border-radius: 5px;
      background: linear-gradient(90deg, #00f0ff, #ff007b);
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.9);
      transition: width 0.1s linear;
    }
    .nitro-hint {
      font-size: 9px;
      color: #94a3b8;
      text-align: right;
    }

    /* Controls Bar */
    .controls-hint {
      display: flex;
      gap: 14px;
      background: rgba(0, 0, 0, 0.6);
      padding: 7px 16px;
      border-radius: 20px;
      font-size: 11px;
      color: #cbd5e1;
      letter-spacing: 0.5px;
    }
    .controls-hint kbd {
      background: rgba(255, 255, 255, 0.2);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: inherit;
      color: #00f0ff;
      font-weight: 800;
    }

    /* Touch Controls */
    #touch-controls {
      display: none;
      position: absolute;
      bottom: 20px;
      left: 0;
      width: 100%;
      height: 160px;
      pointer-events: none;
      z-index: 12;
      justify-content: space-between;
      padding: 0 20px;
    }
    .touch-cluster {
      display: flex;
      gap: 14px;
      pointer-events: auto;
    }
    .touch-btn {
      width: 66px;
      height: 66px;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.85);
      border: 2px solid rgba(0, 240, 255, 0.6);
      color: #fff;
      font-size: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
      touch-action: none;
    }
    .touch-btn:active {
      background: rgba(0, 240, 255, 0.4);
      transform: scale(0.95);
    }
    .touch-btn.nitro-touch {
      border-color: #ff007b;
      color: #ff007b;
      box-shadow: 0 0 18px rgba(255, 0, 123, 0.6);
    }
    .touch-btn.gas-touch {
      border-color: #10b981;
      color: #10b981;
    }
    .touch-btn.brake-touch {
      border-color: #ef4444;
      color: #ef4444;
    }

    /* Modals */
    .modal-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at center, rgba(15, 23, 42, 0.88) 0%, rgba(5, 7, 15, 0.98) 100%);
      backdrop-filter: blur(10px);
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .modal-card {
      background: rgba(17, 24, 39, 0.95);
      border: 2px solid rgba(0, 240, 255, 0.6);
      border-radius: 26px;
      padding: 36px 44px;
      max-width: 580px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 70px rgba(0, 240, 255, 0.35), inset 0 0 25px rgba(0, 240, 255, 0.12);
      display: flex;
      flex-direction: column;
      align-items: center;
      animation: modalFadeIn 0.35s ease-out;
    }
    @keyframes modalFadeIn {
      from { opacity: 0; transform: scale(0.92); }
      to { opacity: 1; transform: scale(1); }
    }
    .hero-photo-wrap {
      position: relative;
      margin-bottom: 20px;
    }
    .hero-photo {
      width: 125px;
      height: 125px;
      border-radius: 50%;
      border: 4px solid #00f0ff;
      object-fit: cover;
      box-shadow: 0 0 35px rgba(0, 240, 255, 0.8);
    }
    .hero-crown {
      position: absolute;
      top: -16px;
      right: 4px;
      font-size: 34px;
      transform: rotate(20deg);
      filter: drop-shadow(0 0 10px #ffd700);
    }
    .modal-title {
      font-size: 34px;
      font-weight: 900;
      letter-spacing: 2px;
      background: linear-gradient(90deg, #00f0ff, #ff007b, #ffd700);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 8px;
      text-transform: uppercase;
    }
    .modal-subtitle {
      font-size: 14px;
      color: #94a3b8;
      margin-bottom: 24px;
      line-height: 1.6;
    }
    .mode-select {
      display: flex;
      gap: 14px;
      width: 100%;
      margin-bottom: 24px;
    }
    .mode-btn {
      flex: 1;
      background: rgba(30, 41, 59, 0.85);
      border: 2px solid rgba(255, 255, 255, 0.15);
      border-radius: 14px;
      padding: 14px 10px;
      color: #fff;
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
    }
    .mode-btn:hover, .mode-btn.active {
      border-color: #00f0ff;
      background: rgba(0, 240, 255, 0.18);
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
    }
    .mode-btn h3 {
      font-size: 15px;
      font-weight: 900;
      margin-bottom: 4px;
    }
    .mode-btn p {
      font-size: 11px;
      color: #94a3b8;
    }
    .cta-btn {
      background: linear-gradient(90deg, #00f0ff, #0084ff);
      color: #080a12;
      font-weight: 900;
      font-size: 18px;
      letter-spacing: 1.2px;
      padding: 15px 36px;
      border-radius: 35px;
      border: none;
      cursor: pointer;
      box-shadow: 0 0 30px rgba(0, 240, 255, 0.7);
      transition: all 0.2s;
      text-transform: uppercase;
      width: 100%;
    }
    .cta-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 40px rgba(0, 240, 255, 0.95);
      background: linear-gradient(90deg, #38f8ff, #1d96ff);
    }

    /* Finish Stats */
    .finish-stats {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      width: 100%;
      margin-bottom: 24px;
    }
    .stat-card {
      background: rgba(30, 41, 59, 0.7);
      border-radius: 12px;
      padding: 10px;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .stat-card-title {
      font-size: 11px;
      color: #94a3b8;
      text-transform: uppercase;
      font-weight: 700;
    }
    .stat-card-value {
      font-size: 20px;
      font-weight: 900;
      color: #00f0ff;
      margin-top: 2px;
    }

    #speed-lines {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 5;
      opacity: 0;
      transition: opacity 0.2s;
    }

    @media (max-width: 768px) {
      .brand-text h2 { font-size: 13px; }
      .brand-text p { display: none; }
      .brand-avatar { width: 36px; height: 36px; }
      .stat-pill { min-width: 65px; padding: 6px 10px; }
      .stat-val { font-size: 16px; }
      .controls-hint { display: none; }
      #touch-controls { display: flex; }
      .radar-box { width: 115px; height: 115px; }
      .dashboard-cluster { padding: 10px 14px; gap: 12px; }
      .speedo-dial { width: 100px; height: 58px; }
      .speedo-svg { width: 100px; height: 100px; }
      .speed-number { font-size: 26px; }
      .gear-num { font-size: 24px; }
      .modal-card { padding: 24px 20px; }
    }
  </style>
</head>
<body>
  <!-- 3D Canvas -->
  <canvas id="game-canvas"></canvas>
  <canvas id="speed-lines"></canvas>

  <!-- HUD -->
  <div id="ui-container">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="brand-badge interactive" title="Arivu - Ready to Race & Ready to Work!">
        <img id="ui-arivu-avatar" class="brand-avatar" alt="Arivu">
        <div class="brand-text">
          <h2>ARIVU GRAND PRIX</h2>
          <p>#OPENTOWORK RACING TEAM</p>
        </div>
      </div>

      <div class="race-stats">
        <div class="stat-pill pos-pill">
          <div class="stat-label">Position</div>
          <div class="stat-val" id="hud-pos">1ST</div>
        </div>
        <div class="stat-pill" id="hud-lap-container">
          <div class="stat-label">Lap</div>
          <div class="stat-val" id="hud-lap">1/3</div>
        </div>
        <div class="stat-pill">
          <div class="stat-label">Time</div>
          <div class="stat-val" id="hud-time">00:00.0</div>
        </div>
        <div class="stat-pill">
          <div class="stat-label">Score</div>
          <div class="stat-val" id="hud-score" style="color:#00f0ff">0</div>
        </div>
      </div>

      <div class="top-actions interactive">
        <button class="icon-btn" id="btn-cam" title="Change Camera View (C)">📷</button>
        <button class="icon-btn" id="btn-audio" title="Mute/Unmute Audio (M)">🔊</button>
        <button class="icon-btn" id="btn-pause" title="Pause Game (P/ESC)">⏸️</button>
      </div>
    </div>

    <!-- Center Alerts -->
    <div class="toast-container" id="toast-box"></div>
    <div class="drift-alert" id="drift-alert">DRIFT +0</div>

    <!-- Bottom Bar -->
    <div class="bottom-bar">
      <!-- Radar -->
      <div class="radar-box">
        <div class="radar-title">TRACK RADAR</div>
        <canvas id="radar-canvas" width="145" height="145"></canvas>
      </div>

      <!-- Hint -->
      <div class="controls-hint">
        <span><kbd>W</kbd>/<kbd>↑</kbd> Accel</span>
        <span><kbd>S</kbd>/<kbd>↓</kbd> Brake</span>
        <span><kbd>A</kbd><kbd>D</kbd> Steer</span>
        <span><kbd>SPACE</kbd> Nitro</span>
        <span><kbd>SHIFT</kbd> Drift</span>
        <span><kbd>C</kbd> Camera</span>
      </div>

      <!-- Dashboard Cluster -->
      <div class="dashboard-cluster">
        <div class="speedo-wrap">
          <div class="speedo-dial">
            <svg class="speedo-svg" viewBox="0 0 100 100">
              <defs>
                <linearGradient id="speedoGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#00f0ff"/>
                  <stop offset="60%" stop-color="#ffd700"/>
                  <stop offset="100%" stop-color="#ff0055"/>
                </linearGradient>
              </defs>
              <circle class="speedo-bg" cx="50" cy="50" r="37.5" />
              <circle class="speedo-fill" id="speedo-fill-ring" cx="50" cy="50" r="37.5" />
            </svg>
            <div class="speed-number" id="hud-speed">0</div>
          </div>
          <div class="speed-unit">KM/H</div>
        </div>

        <div class="gear-wrap">
          <div class="gear-label">GEAR</div>
          <div class="gear-num" id="hud-gear">1</div>
          <div class="rpm-bar-wrap">
            <div class="rpm-bar-fill" id="hud-rpm"></div>
          </div>
        </div>

        <div class="nitro-wrap">
          <div class="nitro-label">
            <span>NITRO BOOST</span>
            <span id="hud-nitro-val">100%</span>
          </div>
          <div class="nitro-track">
            <div class="nitro-fill" id="hud-nitro-fill"></div>
          </div>
          <div class="nitro-hint">PRESS [SPACE]</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Touch Controls -->
  <div id="touch-controls">
    <div class="touch-cluster">
      <div class="touch-btn" id="touch-left">◀</div>
      <div class="touch-btn" id="touch-right">▶</div>
    </div>
    <div class="touch-cluster">
      <div class="touch-btn nitro-touch" id="touch-nitro">⚡</div>
      <div class="touch-btn brake-touch" id="touch-brake">▼</div>
      <div class="touch-btn gas-touch" id="touch-gas">▲</div>
    </div>
  </div>

  <!-- Title Modal -->
  <div class="modal-overlay" id="title-modal">
    <div class="modal-card">
      <div class="hero-photo-wrap">
        <img id="hero-img-start" class="hero-photo" alt="Arivu">
        <div class="hero-crown">⚡</div>
      </div>
      <h1 class="modal-title">ARIVU RACING 3D</h1>
      <p class="modal-subtitle">
        Accelerate to career heights! Race as <strong>Arivu</strong>, overtake rival racers, collect Job Offer Letters, and drift through high-speed cyber turns to victory!
      </p>

      <div class="mode-select">
        <div class="mode-btn active" id="mode-gp" onclick="setGameMode('gp')">
          <h3>🏎️ CAREER GP</h3>
          <p>3 Fast Laps vs 4 AI Rivals</p>
        </div>
        <div class="mode-btn" id="mode-endless" onclick="setGameMode('endless')">
          <h3>⚡ ENDLESS HIGHWAY</h3>
          <p>Endless score chase & traffic</p>
        </div>
      </div>

      <button class="cta-btn" id="btn-start-game">START ENGINE & RACE</button>
    </div>
  </div>

  <!-- Pause Modal -->
  <div class="modal-overlay" id="pause-modal" style="display:none;">
    <div class="modal-card">
      <h1 class="modal-title">GAME PAUSED</h1>
      <p class="modal-subtitle">Take a breather, tune your tires, and get back to the track!</p>
      <div style="display:flex; flex-direction:column; gap:12px; width:100%;">
        <button class="cta-btn" id="btn-resume">RESUME RACE</button>
        <button class="mode-btn" id="btn-restart" style="width:100%;">RESTART RACE</button>
      </div>
    </div>
  </div>

  <!-- Victory Modal -->
  <div class="modal-overlay" id="finish-modal" style="display:none;">
    <div class="modal-card">
      <div class="hero-photo-wrap">
        <img id="hero-img-finish" class="hero-photo" alt="Arivu">
        <div class="hero-crown">🏆</div>
      </div>
      <h1 class="modal-title" id="finish-title">VICTORY PODIUM!</h1>
      <p class="modal-subtitle" id="finish-msg">
        Arivu crossed the checkered flag in 1st Place! #OPENTOWORK Offer letters signed!
      </p>

      <div class="finish-stats">
        <div class="stat-card">
          <div class="stat-card-title">Final Position</div>
          <div class="stat-card-value" id="res-pos">1st Place</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-title">Total Time</div>
          <div class="stat-card-value" id="res-time">02:14.3</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-title">Top Speed</div>
          <div class="stat-card-value" id="res-speed">294 KM/H</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-title">Total Score</div>
          <div class="stat-card-value" id="res-score">4,850 PTS</div>
        </div>
      </div>

      <div style="display:flex; gap:14px; width:100%;">
        <button class="cta-btn" id="btn-play-again" style="flex:1;">RACE AGAIN</button>
      </div>
    </div>
  </div>

  <!-- Three.js -->
  <script src="three.min.js"></script>
  <script>
    if (typeof THREE === 'undefined') {
      document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\/script>');
    }
  </script>

  <!-- Game Code -->
  <script>
    const ARIVU_BASE64 = "data:image/jpeg;base64,__ARIVU_IMAGE_BASE64__";
    document.getElementById('ui-arivu-avatar').src = ARIVU_BASE64;
    document.getElementById('hero-img-start').src = ARIVU_BASE64;
    document.getElementById('hero-img-finish').src = ARIVU_BASE64;

    /* =========================================================================
       AUDIO SYSTEM (Pure Web Audio API - Synthesizer Engine & SFX)
       ========================================================================= */
    class SoundEngine {
      constructor() {
        this.ctx = null;
        this.masterGain = null;
        this.engineOsc1 = null;
        this.engineOsc2 = null;
        this.engineFilter = null;
        this.engineGain = null;
        this.nitroGain = null;
        this.driftGain = null;
        this.bgmGain = null;
        this.enabled = true;
        this.bgmStep = 0;
        this.bgmTimer = null;
      }

      init() {
        if (this.ctx) {
          if (this.ctx.state === 'suspended') this.ctx.resume();
          return;
        }
        try {
          const AudioCtx = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioCtx();

          this.masterGain = this.ctx.createGain();
          this.masterGain.gain.setValueAtTime(0.75, this.ctx.currentTime);
          this.masterGain.connect(this.ctx.destination);

          // Engine Sound: Dual Sawtooth / Triangle
          this.engineGain = this.ctx.createGain();
          this.engineGain.gain.setValueAtTime(0.08, this.ctx.currentTime);

          this.engineFilter = this.ctx.createBiquadFilter();
          this.engineFilter.type = 'lowpass';
          this.engineFilter.frequency.setValueAtTime(350, this.ctx.currentTime);

          this.engineOsc1 = this.ctx.createOscillator();
          this.engineOsc1.type = 'sawtooth';
          this.engineOsc1.frequency.setValueAtTime(75, this.ctx.currentTime);

          this.engineOsc2 = this.ctx.createOscillator();
          this.engineOsc2.type = 'triangle';
          this.engineOsc2.frequency.setValueAtTime(37.5, this.ctx.currentTime);

          this.engineOsc1.connect(this.engineFilter);
          this.engineOsc2.connect(this.engineFilter);
          this.engineFilter.connect(this.engineGain);
          this.engineGain.connect(this.masterGain);

          this.engineOsc1.start();
          this.engineOsc2.start();

          this.setupNitroSound();
          this.setupDriftSound();
          this.startSynthBGM();
        } catch (e) {
          console.warn("Audio init deferred:", e);
        }
      }

      setupNitroSound() {
        const bufferSize = this.ctx.sampleRate * 2;
        const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          output[i] = Math.random() * 2 - 1;
        }

        const whiteNoise = this.ctx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(1400, this.ctx.currentTime);
        filter.Q.setValueAtTime(1.8, this.ctx.currentTime);

        this.nitroGain = this.ctx.createGain();
        this.nitroGain.gain.setValueAtTime(0.001, this.ctx.currentTime);

        whiteNoise.connect(filter);
        filter.connect(this.nitroGain);
        this.nitroGain.connect(this.masterGain);
        whiteNoise.start();
      }

      setupDriftSound() {
        const bufferSize = this.ctx.sampleRate * 2;
        const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          output[i] = Math.random() * 2 - 1;
        }

        const whiteNoise = this.ctx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(850, this.ctx.currentTime);
        filter.Q.setValueAtTime(3.5, this.ctx.currentTime);

        this.driftGain = this.ctx.createGain();
        this.driftGain.gain.setValueAtTime(0.001, this.ctx.currentTime);

        whiteNoise.connect(filter);
        filter.connect(this.driftGain);
        this.driftGain.connect(this.masterGain);
        whiteNoise.start();
      }

      updateEngine(rpmRatio, throttle, speedRatio) {
        if (!this.ctx || !this.enabled) return;
        const t = this.ctx.currentTime;
        const freq = 65 + rpmRatio * 280;
        this.engineOsc1.frequency.setTargetAtTime(freq, t, 0.05);
        this.engineOsc2.frequency.setTargetAtTime(freq * 0.5, t, 0.05);

        const filterCutoff = 260 + throttle * 750 + speedRatio * 950;
        this.engineFilter.frequency.setTargetAtTime(filterCutoff, t, 0.08);

        const vol = 0.05 + throttle * 0.12 + (speedRatio > 0.05 ? 0.06 : 0);
        this.engineGain.gain.setTargetAtTime(vol, t, 0.05);
      }

      setNitro(active) {
        if (!this.nitroGain || !this.enabled) return;
        this.nitroGain.gain.setTargetAtTime(active ? 0.28 : 0.001, this.ctx.currentTime, 0.08);
      }

      setDrift(active, intensity = 1.0) {
        if (!this.driftGain || !this.enabled) return;
        const vol = active ? Math.min(0.22, 0.12 * intensity) : 0.001;
        this.driftGain.gain.setTargetAtTime(vol, this.ctx.currentTime, 0.05);
      }

      playChime() {
        if (!this.ctx || !this.enabled) return;
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          const startTime = this.ctx.currentTime + idx * 0.06;
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, startTime);
          gain.gain.setValueAtTime(0.2, startTime);
          gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.3);
          osc.connect(gain);
          gain.connect(this.masterGain);
          osc.start(startTime);
          osc.stop(startTime + 0.32);
        });
      }

      playBump() {
        if (!this.ctx || !this.enabled) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        const t = this.ctx.currentTime;
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(150, t);
        osc.frequency.exponentialRampToValueAtTime(35, t + 0.15);
        gain.gain.setValueAtTime(0.35, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.18);
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(t);
        osc.stop(t + 0.2);
      }

      startSynthBGM() {
        this.bgmGain = this.ctx.createGain();
        this.bgmGain.gain.setValueAtTime(0.12, this.ctx.currentTime);
        this.bgmGain.connect(this.masterGain);

        const bassNotes = [
          146.83, 146.83, 146.83, 146.83, // D3
          174.61, 174.61, 174.61, 174.61, // F3
          130.81, 130.81, 130.81, 130.81, // C3
          196.00, 196.00, 196.00, 196.00  // G3
        ];

        const stepTime = 125;
        this.bgmTimer = setInterval(() => {
          if (!this.enabled || !this.ctx) return;
          const noteFreq = bassNotes[this.bgmStep % bassNotes.length];

          if (this.bgmStep % 4 === 0) {
            this.playKick();
          }

          const osc = this.ctx.createOscillator();
          const g = this.ctx.createGain();
          const t = this.ctx.currentTime;
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(noteFreq * 0.5, t);
          g.gain.setValueAtTime(0.08, t);
          g.gain.exponentialRampToValueAtTime(0.005, t + 0.11);
          osc.connect(g);
          g.connect(this.bgmGain);
          osc.start(t);
          osc.stop(t + 0.12);

          if (this.bgmStep % 2 === 1) {
            const arpOsc = this.ctx.createOscillator();
            const arpg = this.ctx.createGain();
            arpOsc.type = 'square';
            const chordTones = [293.66, 349.23, 440.0, 523.25, 587.33];
            const tone = chordTones[(this.bgmStep * 2) % chordTones.length];
            arpOsc.frequency.setValueAtTime(tone, t);
            arpg.gain.setValueAtTime(0.04, t);
            arpg.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
            arpOsc.connect(arpg);
            arpg.connect(this.bgmGain);
            arpOsc.start(t);
            arpOsc.stop(t + 0.11);
          }

          this.bgmStep = (this.bgmStep + 1) % 64;
        }, stepTime);
      }

      playKick() {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        const t = this.ctx.currentTime;
        osc.frequency.setValueAtTime(150, t);
        osc.frequency.exponentialRampToValueAtTime(30, t + 0.08);
        gain.gain.setValueAtTime(0.35, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.09);
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(t);
        osc.stop(t + 0.1);
      }

      toggle() {
        this.enabled = !this.enabled;
        if (this.masterGain && this.ctx) {
          this.masterGain.gain.setValueAtTime(this.enabled ? 0.75 : 0, this.ctx.currentTime);
        }
        return this.enabled;
      }
    }

    const sound = new SoundEngine();

    /* =========================================================================
       TEXTURE BUILDER (Decals, Billboards, Road, Curbs)
       ========================================================================= */
    const textureLib = {
      hoodDecal: null,
      driverFace: null,
      billboardA: null,
      billboardB: null,
      billboardC: null,
      billboardD: null,
      curbTexture: null,
      roadTexture: null
    };

    function loadCustomTextures() {
      return new Promise((resolve) => {
        const arivuImg = new Image();
        arivuImg.src = ARIVU_BASE64;
        arivuImg.onload = () => {
          // 1. Hood Decal Texture (512x512)
          const hoodCanvas = document.createElement('canvas');
          hoodCanvas.width = 512;
          hoodCanvas.height = 512;
          const hCtx = hoodCanvas.getContext('2d');

          // Dark Carbon base
          hCtx.fillStyle = '#0f172a';
          hCtx.fillRect(0, 0, 512, 512);

          // Dual Racing Stripes
          hCtx.fillStyle = '#00f0ff';
          hCtx.fillRect(230, 0, 52, 512);
          hCtx.fillStyle = '#ff007b';
          hCtx.fillRect(195, 0, 22, 512);
          hCtx.fillRect(295, 0, 22, 512);

          // Golden Circular Badge with Arivu
          hCtx.save();
          hCtx.beginPath();
          hCtx.arc(256, 256, 180, 0, Math.PI * 2);
          hCtx.fillStyle = '#1e293b';
          hCtx.fill();
          hCtx.lineWidth = 14;
          hCtx.strokeStyle = '#ffd700';
          hCtx.stroke();
          hCtx.clip();
          hCtx.drawImage(arivuImg, 100, 100, 312, 312);
          hCtx.restore();

          // Badge Text
          hCtx.fillStyle = '#ffd700';
          hCtx.font = 'bold 24px sans-serif';
          hCtx.textAlign = 'center';
          hCtx.fillText('★ ARIVU RACING GP ★', 256, 52);
          hCtx.fillStyle = '#00f0ff';
          hCtx.font = 'bold 22px sans-serif';
          hCtx.fillText('#OPENTOWORK CHAMPION', 256, 480);

          textureLib.hoodDecal = new THREE.CanvasTexture(hoodCanvas);

          // 2. Driver Face (256x256)
          const faceCanvas = document.createElement('canvas');
          faceCanvas.width = 256;
          faceCanvas.height = 256;
          const fCtx = faceCanvas.getContext('2d');
          fCtx.drawImage(arivuImg, 0, 0, 256, 256);
          textureLib.driverFace = new THREE.CanvasTexture(faceCanvas);

          // 3. Billboards
          textureLib.billboardA = createBillboardCanvas(
            arivuImg,
            '#OPENTOWORK GRAND PRIX',
            'ARIVU IS READY TO CODE AT 300 KM/H',
            'HIRE THE FASTEST DEV TODAY!',
            '#00f0ff',
            '#0b1329'
          );

          textureLib.billboardB = createBillboardCanvas(
            arivuImg,
            'CAREER ACCELERATION',
            'OFFER LETTER DETECTED AHEAD',
            'FULL THROTTLE PERFORMANCE',
            '#ffd700',
            '#1e1035'
          );

          textureLib.billboardC = createBillboardCanvas(
            arivuImg,
            'TURBO TALENT ON TRACK',
            'SOLVING BUGS IN UNDER 3 SECONDS',
            'NITRO BOOST YOUR ENGINEERING TEAM',
            '#ff007b',
            '#05252b'
          );

          textureLib.billboardD = createBillboardCanvas(
            arivuImg,
            'POLE POSITION LEADERSHIP',
            'SCALING SYSTEMS AT BREAKNECK SPEED',
            'JOIN FORCES WITH ARIVU!',
            '#10b981',
            '#1a102f'
          );

          // 4. Procedural Curb Texture
          const curbCanvas = document.createElement('canvas');
          curbCanvas.width = 64;
          curbCanvas.height = 64;
          const cCtx = curbCanvas.getContext('2d');
          cCtx.fillStyle = '#ff0055';
          cCtx.fillRect(0, 0, 32, 64);
          cCtx.fillStyle = '#ffffff';
          cCtx.fillRect(32, 0, 32, 64);
          textureLib.curbTexture = new THREE.CanvasTexture(curbCanvas);
          textureLib.curbTexture.wrapS = THREE.RepeatWrapping;
          textureLib.curbTexture.wrapT = THREE.RepeatWrapping;

          // 5. Procedural High-Visibility Road Texture
          const roadCanvas = document.createElement('canvas');
          roadCanvas.width = 512;
          roadCanvas.height = 512;
          const rCtx = roadCanvas.getContext('2d');

          // Rich slate asphalt
          rCtx.fillStyle = '#222736';
          rCtx.fillRect(0, 0, 512, 512);

          // Subtle asphalt texture speckles
          for (let i = 0; i < 4000; i++) {
            rCtx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.15)';
            rCtx.fillRect(Math.random() * 512, Math.random() * 512, 2, 2);
          }

          // Outer Solid White Road Lines
          rCtx.fillStyle = '#ffffff';
          rCtx.fillRect(24, 0, 16, 512);
          rCtx.fillRect(472, 0, 16, 512);

          // Inner Cyan Lane Guide Lines
          rCtx.fillStyle = 'rgba(0, 240, 255, 0.4)';
          rCtx.fillRect(150, 0, 4, 512);
          rCtx.fillRect(358, 0, 4, 512);

          // Bright Yellow Dashed Center Line
          rCtx.fillStyle = '#ffd700';
          for (let y = 0; y < 512; y += 64) {
            rCtx.fillRect(250, y + 10, 12, 40);
          }

          textureLib.roadTexture = new THREE.CanvasTexture(roadCanvas);
          textureLib.roadTexture.wrapS = THREE.RepeatWrapping;
          textureLib.roadTexture.wrapT = THREE.RepeatWrapping;

          resolve();
        };
      });
    }

    function createBillboardCanvas(img, tag, line1, line2, accentColor, bgColor) {
      const canvas = document.createElement('canvas');
      canvas.width = 1024;
      canvas.height = 512;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = bgColor;
      ctx.fillRect(0, 0, 1024, 512);

      ctx.lineWidth = 16;
      ctx.strokeStyle = accentColor;
      ctx.strokeRect(8, 8, 1008, 496);

      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth = 2;
      for (let x = 0; x < 1024; x += 64) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 512); ctx.stroke();
      }

      ctx.save();
      ctx.beginPath();
      ctx.arc(260, 256, 190, 0, Math.PI * 2);
      ctx.lineWidth = 14;
      ctx.strokeStyle = accentColor;
      ctx.stroke();
      ctx.clip();
      ctx.drawImage(img, 60, 56, 400, 400);
      ctx.restore();

      ctx.fillStyle = accentColor;
      ctx.font = '900 36px "Segoe UI", sans-serif';
      ctx.fillText('⚡ ' + tag, 490, 135);

      ctx.fillStyle = '#ffffff';
      ctx.font = '900 40px "Segoe UI", sans-serif';
      ctx.fillText(line1, 490, 220);

      ctx.fillStyle = '#94a3b8';
      ctx.font = '700 30px "Segoe UI", sans-serif';
      ctx.fillText(line2, 490, 300);

      ctx.fillStyle = accentColor;
      ctx.beginPath();
      ctx.roundRect(490, 360, 380, 60, 30);
      ctx.fill();

      ctx.fillStyle = '#080a12';
      ctx.font = '900 28px "Segoe UI", sans-serif';
      ctx.fillText('GO ARIVU! FULL NITRO ➔', 515, 402);

      return new THREE.CanvasTexture(canvas);
    }

    /* =========================================================================
       THREE.JS GRAPHICS SETUP
       ========================================================================= */
    let scene, camera, renderer, clock;
    const viewModes = ['chase', 'hood', 'cockpit', 'drone'];
    let currentViewModeIndex = 0;

    function initGraphics() {
      const canvas = document.getElementById('game-canvas');
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.25;

      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x0c1022);
      scene.fog = new THREE.FogExp2(0x0c1022, 0.0016);

      camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.2, 2200);
      clock = new THREE.Clock();

      buildSkybox();

      // Rich Ambient Lighting
      const hemiLight = new THREE.HemisphereLight(0x7dd3fc, 0x581c87, 1.4);
      scene.add(hemiLight);

      // Primary Warm Sun Light
      const sunLight = new THREE.DirectionalLight(0xffa200, 1.6);
      sunLight.position.set(220, 280, 180);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 2048;
      sunLight.shadow.mapSize.height = 2048;
      sunLight.shadow.camera.near = 10;
      sunLight.shadow.camera.far = 900;
      sunLight.shadow.camera.left = -160;
      sunLight.shadow.camera.right = 160;
      sunLight.shadow.camera.top = 160;
      sunLight.shadow.camera.bottom = -160;
      sunLight.shadow.bias = -0.0004;
      scene.add(sunLight);

      // Secondary Cool Fill Light
      const fillLight = new THREE.DirectionalLight(0x00f0ff, 0.7);
      fillLight.position.set(-200, 150, -200);
      scene.add(fillLight);

      window.addEventListener('resize', onWindowResize);
    }

    function buildSkybox() {
      // Synthwave Sunset Giant Sun
      const sunGeo = new THREE.CircleGeometry(130, 32);
      const sunMat = new THREE.MeshBasicMaterial({ color: 0xff007b, side: THREE.DoubleSide });
      const sunMesh = new THREE.Mesh(sunGeo, sunMat);
      sunMesh.position.set(0, 90, -950);
      scene.add(sunMesh);

      // Distant Low-Poly Mountains
      const mtnGeo = new THREE.ConeGeometry(90, 170, 4);
      const mtnMat = new THREE.MeshStandardMaterial({ color: 0x181e3a, roughness: 0.9, flatShading: true });
      for (let i = 0; i < 36; i++) {
        const mtn = new THREE.Mesh(mtnGeo, mtnMat);
        const angle = (i / 36) * Math.PI * 2;
        const dist = 780 + Math.random() * 160;
        mtn.position.set(Math.cos(angle) * dist, 65 + Math.random() * 30, Math.sin(angle) * dist);
        const s = 1.3 + Math.random() * 1.5;
        mtn.scale.set(s, s * (0.8 + Math.random() * 0.8), s);
        scene.add(mtn);
      }

      // Distant Cyber City Skyline Silhouette
      const bldgGeo = new THREE.BoxGeometry(32, 1, 32);
      const bldgMat = new THREE.MeshStandardMaterial({ color: 0x0c1024, roughness: 0.8 });
      for (let i = 0; i < 60; i++) {
        const bldg = new THREE.Mesh(bldgGeo, bldgMat);
        const angle = (i / 60) * Math.PI * 2;
        const dist = 620 + Math.random() * 90;
        const height = 45 + Math.random() * 95;
        bldg.position.set(Math.cos(angle) * dist, height / 2, Math.sin(angle) * dist);
        bldg.scale.set(1 + Math.random(), height, 1 + Math.random());
        scene.add(bldg);
      }
    }

    function onWindowResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    /* =========================================================================
       TRACK & CIRCUIT SPLINE GENERATOR
       ========================================================================= */
    let trackCurve;
    let trackLength = 0;
    const trackWidth = 24;
    const trackSegments = 900;
    const trackSamples = [];
    const billboardMeshList = [];

    function buildTrack() {
      const rawPoints = [
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0, -220),
        new THREE.Vector3(40, 2, -380),
        new THREE.Vector3(140, 5, -500),
        new THREE.Vector3(280, 4, -530),
        new THREE.Vector3(400, 2, -430),
        new THREE.Vector3(450, 0, -280),
        new THREE.Vector3(420, -2, -120),
        new THREE.Vector3(480, -1, 30),
        new THREE.Vector3(440, 1, 180),
        new THREE.Vector3(340, 3, 270),
        new THREE.Vector3(230, 4, 230),
        new THREE.Vector3(140, 2, 140),
        new THREE.Vector3(30, 0, 190),
        new THREE.Vector3(-90, 4, 280),
        new THREE.Vector3(-240, 6, 300),
        new THREE.Vector3(-360, 3, 220),
        new THREE.Vector3(-400, 1, 60),
        new THREE.Vector3(-370, -1, -90),
        new THREE.Vector3(-270, 0, -190),
        new THREE.Vector3(-150, 0, -150),
        new THREE.Vector3(-50, 0, -60)
      ];

      trackCurve = new THREE.CatmullRomCurve3(rawPoints, true, 'catmullrom', 0.5);
      trackLength = trackCurve.getLength();

      for (let i = 0; i <= trackSegments; i++) {
        const t = i / trackSegments;
        const pt = trackCurve.getPointAt(t);
        const tangent = trackCurve.getTangentAt(t);
        const up = new THREE.Vector3(0, 1, 0);
        const binormal = new THREE.Vector3().crossVectors(tangent, up).normalize();
        trackSamples.push({ t, pt, tangent, binormal });
      }

      // 1. Road Surface Mesh
      const roadGeo = new THREE.BufferGeometry();
      const vertices = [];
      const uvs = [];
      const indices = [];

      for (let i = 0; i <= trackSegments; i++) {
        const s = trackSamples[i];
        const halfW = trackWidth / 2;

        const pLeft = s.pt.clone().sub(s.binormal.clone().multiplyScalar(halfW));
        const pRight = s.pt.clone().add(s.binormal.clone().multiplyScalar(halfW));

        vertices.push(pLeft.x, pLeft.y + 0.05, pLeft.z);
        vertices.push(pRight.x, pRight.y + 0.05, pRight.z);

        const vCoord = (i / trackSegments) * 80;
        uvs.push(0, vCoord);
        uvs.push(1, vCoord);

        if (i < trackSegments) {
          const row1 = i * 2;
          const row2 = (i + 1) * 2;
          indices.push(row1, row2, row1 + 1);
          indices.push(row1 + 1, row2, row2 + 1);
        }
      }

      roadGeo.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      roadGeo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
      roadGeo.setIndex(indices);
      roadGeo.computeVertexNormals();

      const roadMat = new THREE.MeshStandardMaterial({
        map: textureLib.roadTexture,
        roughness: 0.55,
        metalness: 0.15
      });
      const roadMesh = new THREE.Mesh(roadGeo, roadMat);
      roadMesh.receiveShadow = true;
      scene.add(roadMesh);

      // 2. Curbs
      buildCurbs();

      // 3. Guardrails
      buildGuardrails();

      // 4. Start / Finish Gantry
      buildStartFinishGantry();

      // 5. Track Arches
      buildTrackArches();

      // 6. Giant Roadside Billboards with Arivu
      buildRoadsideBillboards();

      // 7. Ground Terrain
      buildTerrain();

      // 8. Trees & Street Lights
      buildStreetProps();
    }

    function buildCurbs() {
      const curbWidth = 1.4;
      const curbGeo = new THREE.BufferGeometry();
      const vertices = [];
      const uvs = [];
      const indices = [];
      let vertOffset = 0;

      for (let side = -1; side <= 1; side += 2) {
        for (let i = 0; i <= trackSegments; i++) {
          const s = trackSamples[i];
          const innerDist = (trackWidth / 2) * side;
          const outerDist = innerDist + curbWidth * side;

          const pInner = s.pt.clone().add(s.binormal.clone().multiplyScalar(innerDist));
          const pOuter = s.pt.clone().add(s.binormal.clone().multiplyScalar(outerDist));

          vertices.push(pInner.x, pInner.y + 0.08, pInner.z);
          vertices.push(pOuter.x, pOuter.y + 0.06, pOuter.z);

          const vCoord = (i / trackSegments) * 200;
          uvs.push(0, vCoord);
          uvs.push(1, vCoord);

          if (i < trackSegments) {
            const r1 = vertOffset + i * 2;
            const r2 = vertOffset + (i + 1) * 2;
            indices.push(r1, r2, r1 + 1);
            indices.push(r1 + 1, r2, r2 + 1);
          }
        }
        vertOffset += (trackSegments + 1) * 2;
      }

      curbGeo.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      curbGeo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
      curbGeo.setIndex(indices);
      curbGeo.computeVertexNormals();

      const curbMat = new THREE.MeshStandardMaterial({
        map: textureLib.curbTexture,
        roughness: 0.5
      });
      const curbMesh = new THREE.Mesh(curbGeo, curbMat);
      curbMesh.receiveShadow = true;
      scene.add(curbMesh);
    }

    function buildGuardrails() {
      const railHeight = 1.1;
      const railGeo = new THREE.BufferGeometry();
      const vertices = [];
      const indices = [];
      let vertOffset = 0;

      for (let side = -1; side <= 1; side += 2) {
        for (let i = 0; i <= trackSegments; i++) {
          const s = trackSamples[i];
          const dist = (trackWidth / 2 + 1.5) * side;
          const basePt = s.pt.clone().add(s.binormal.clone().multiplyScalar(dist));

          vertices.push(basePt.x, basePt.y, basePt.z);
          vertices.push(basePt.x, basePt.y + railHeight, basePt.z);

          if (i < trackSegments) {
            const r1 = vertOffset + i * 2;
            const r2 = vertOffset + (i + 1) * 2;
            indices.push(r1, r2, r1 + 1);
            indices.push(r1 + 1, r2, r2 + 1);
          }
        }
        vertOffset += (trackSegments + 1) * 2;
      }

      railGeo.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      railGeo.setIndex(indices);
      railGeo.computeVertexNormals();

      const railMat = new THREE.MeshStandardMaterial({
        color: 0x94a3b8,
        metalness: 0.85,
        roughness: 0.25,
        side: THREE.DoubleSide
      });
      const railMesh = new THREE.Mesh(railGeo, railMat);
      scene.add(railMesh);
    }

    function buildStartFinishGantry() {
      const startPt = trackCurve.getPointAt(0);
      const tangent = trackCurve.getTangentAt(0);
      const binormal = new THREE.Vector3().crossVectors(tangent, new THREE.Vector3(0, 1, 0)).normalize();

      const gantryGroup = new THREE.Group();

      const postGeo = new THREE.CylinderGeometry(0.5, 0.5, 11, 16);
      const postMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8 });

      const postL = new THREE.Mesh(postGeo, postMat);
      postL.position.copy(startPt).sub(binormal.clone().multiplyScalar(trackWidth / 2 + 3.5));
      postL.position.y += 5.5;

      const postR = new THREE.Mesh(postGeo, postMat);
      postR.position.copy(startPt).add(binormal.clone().multiplyScalar(trackWidth / 2 + 3.5));
      postR.position.y += 5.5;

      const beamGeo = new THREE.BoxGeometry(trackWidth + 9, 2.8, 2.2);
      const beamMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.9 });
      const beam = new THREE.Mesh(beamGeo, beamMat);
      beam.position.copy(startPt);
      beam.position.y += 10.5;
      beam.quaternion.setFromUnitVectors(new THREE.Vector3(1, 0, 0), binormal);

      const bannerCanvas = document.createElement('canvas');
      bannerCanvas.width = 1024;
      bannerCanvas.height = 128;
      const bCtx = bannerCanvas.getContext('2d');
      bCtx.fillStyle = '#000';
      bCtx.fillRect(0, 0, 1024, 128);
      for (let x = 0; x < 1024; x += 32) {
        bCtx.fillStyle = (x / 32) % 2 === 0 ? '#fff' : '#ff0055';
        bCtx.fillRect(x, 0, 32, 24);
        bCtx.fillRect(x, 104, 32, 24);
      }
      bCtx.fillStyle = '#00f0ff';
      bCtx.font = '900 52px "Segoe UI", sans-serif';
      bCtx.textAlign = 'center';
      bCtx.fillText('★ ARIVU SUPER TURBO GRAND PRIX ★', 512, 78);

      const bannerTex = new THREE.CanvasTexture(bannerCanvas);
      const signGeo = new THREE.PlaneGeometry(trackWidth + 7, 2.4);
      const signMat = new THREE.MeshBasicMaterial({ map: bannerTex, side: THREE.DoubleSide });
      const signMesh = new THREE.Mesh(signGeo, signMat);
      signMesh.position.copy(beam.position);
      signMesh.position.sub(tangent.clone().multiplyScalar(1.15));
      signMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), tangent.clone().negate());

      gantryGroup.add(postL);
      gantryGroup.add(postR);
      gantryGroup.add(beam);
      gantryGroup.add(signMesh);
      scene.add(gantryGroup);

      // Checkered Line on Asphalt
      const chkCanvas = document.createElement('canvas');
      chkCanvas.width = 512;
      chkCanvas.height = 128;
      const cCtx = chkCanvas.getContext('2d');
      for (let x = 0; x < 512; x += 32) {
        for (let y = 0; y < 128; y += 32) {
          cCtx.fillStyle = ((x / 32) + (y / 32)) % 2 === 0 ? '#ffffff' : '#111827';
          cCtx.fillRect(x, y, 32, 32);
        }
      }
      const chkTex = new THREE.CanvasTexture(chkCanvas);
      
      const chkMat = new THREE.MeshBasicMaterial({ map: chkTex, side: THREE.DoubleSide });
      // Checkered Line flat on road
      const chkGeo = new THREE.PlaneGeometry(trackWidth, 4);
      const chkMesh = new THREE.Mesh(chkGeo, chkMat);
      chkMesh.position.copy(startPt);
      chkMesh.position.y += 0.08;
      chkMesh.rotation.x = -Math.PI / 2;
      chkMesh.rotation.z = -Math.atan2(tangent.x, -tangent.z);
      scene.add(chkMesh);
    }

    function buildTrackArches() {
      const archPoints = [0.28, 0.58, 0.82];
      archPoints.forEach(t => {
        const pt = trackCurve.getPointAt(t);
        const tangent = trackCurve.getTangentAt(t);

        const archGeo = new THREE.TorusGeometry(trackWidth * 0.65, 0.6, 8, 24, Math.PI);
        const archMat = new THREE.MeshStandardMaterial({
          color: 0x00f0ff,
          emissive: 0x00f0ff,
          emissiveIntensity: 1.0
        });
        const archMesh = new THREE.Mesh(archGeo, archMat);
        archMesh.position.copy(pt);
        archMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), tangent);
        scene.add(archMesh);
      });
    }

    function buildRoadsideBillboards() {
      const billboardPositions = [
        0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95
      ];
      const textures = [
        textureLib.billboardA,
        textureLib.billboardB,
        textureLib.billboardC,
        textureLib.billboardD
      ];

      billboardPositions.forEach((t, i) => {
        const pt = trackCurve.getPointAt(t);
        const tangent = trackCurve.getTangentAt(t);
        const binormal = new THREE.Vector3().crossVectors(tangent, new THREE.Vector3(0, 1, 0)).normalize();

        const side = (i % 2 === 0) ? 1 : -1;
        const bPos = pt.clone().add(binormal.clone().multiplyScalar((trackWidth / 2 + 13) * side));
        bPos.y += 8.5;

        const bGroup = new THREE.Group();

        const poleGeo = new THREE.CylinderGeometry(0.45, 0.45, 17, 12);
        const poleMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.8 });
        const pole1 = new THREE.Mesh(poleGeo, poleMat);
        pole1.position.set(-6, -2, 0);
        const pole2 = new THREE.Mesh(poleGeo, poleMat);
        pole2.position.set(6, -2, 0);
        bGroup.add(pole1);
        bGroup.add(pole2);

        const frameGeo = new THREE.BoxGeometry(16.5, 8.5, 0.8);
        const frameMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.9 });
        const frame = new THREE.Mesh(frameGeo, frameMat);
        bGroup.add(frame);

        const screenGeo = new THREE.PlaneGeometry(16, 8);
        const screenMat = new THREE.MeshBasicMaterial({
          map: textures[i % textures.length],
          side: THREE.DoubleSide
        });
        const screen = new THREE.Mesh(screenGeo, screenMat);
        screen.position.z = 0.45;
        bGroup.add(screen);
        billboardMeshList.push(screen);

        bGroup.position.copy(bPos);
        const lookTarget = pt.clone().sub(tangent.clone().multiplyScalar(40));
        lookTarget.y = bPos.y;
        bGroup.lookAt(lookTarget);

        scene.add(bGroup);
      });
    }

    function buildTerrain() {
      const groundGeo = new THREE.PlaneGeometry(3200, 3200, 40, 40);
      const groundMat = new THREE.MeshStandardMaterial({
        color: 0x0a0d18,
        roughness: 0.95,
        metalness: 0.05
      });
      const ground = new THREE.Mesh(groundGeo, groundMat);
      ground.rotation.x = -Math.PI / 2;
      ground.position.y = -0.2;
      ground.receiveShadow = true;
      scene.add(ground);
    }

    function buildStreetProps() {
      const palmTrunkGeo = new THREE.CylinderGeometry(0.3, 0.6, 9, 8);
      const palmTrunkMat = new THREE.MeshStandardMaterial({ color: 0x1f2937 });
      const palmLeavesGeo = new THREE.ConeGeometry(5, 4, 6);
      const palmLeavesMat = new THREE.MeshStandardMaterial({
        color: 0x06d6a0,
        emissive: 0x06d6a0,
        emissiveIntensity: 0.4,
        roughness: 0.5
      });

      for (let i = 0; i < 75; i++) {
        const t = (i / 75);
        const pt = trackCurve.getPointAt(t);
        const binormal = trackSamples[Math.floor(t * trackSegments)].binormal;
        const side = (i % 2 === 0) ? 1 : -1;
        const pPos = pt.clone().add(binormal.clone().multiplyScalar((trackWidth / 2 + 7 + (i % 3) * 3) * side));

        const treeGroup = new THREE.Group();
        const trunk = new THREE.Mesh(palmTrunkGeo, palmTrunkMat);
        trunk.position.y = 4.5;
        const leaves = new THREE.Mesh(palmLeavesGeo, palmLeavesMat);
        leaves.position.y = 9;
        treeGroup.add(trunk);
        treeGroup.add(leaves);
        treeGroup.position.copy(pPos);
        treeGroup.position.y = pt.y;
        treeGroup.rotation.y = Math.random() * Math.PI;
        scene.add(treeGroup);
      }
    }

    /* =========================================================================
       CAR BUILDER: 3D CYBER SPORTS RACER (With Arivu Avatar & Decal)
       ========================================================================= */
    function createCarMesh(colorHex = 0x00f0ff, isPlayer = false) {
      const car = new THREE.Group();

      const bodyMat = new THREE.MeshStandardMaterial({
        color: colorHex,
        emissive: isPlayer ? 0x002838 : 0x1a0a1a,
        metalness: 0.75,
        roughness: 0.15
      });
      const darkMat = new THREE.MeshStandardMaterial({
        color: 0x0b0f19,
        roughness: 0.25,
        metalness: 0.85
      });
      const glassMat = new THREE.MeshStandardMaterial({
        color: 0x050811,
        metalness: 0.95,
        roughness: 0.08,
        transparent: true,
        opacity: 0.75
      });

      // Lower Chassis
      const chassisGeo = new THREE.BoxGeometry(2.2, 0.45, 4.4);
      const chassis = new THREE.Mesh(chassisGeo, bodyMat);
      chassis.position.y = 0.45;
      chassis.castShadow = true;
      car.add(chassis);

      // Front Aerodynamic Nose
      const noseGeo = new THREE.BoxGeometry(2.0, 0.28, 1.2);
      const nose = new THREE.Mesh(noseGeo, bodyMat);
      nose.position.set(0, 0.35, -2.4);
      car.add(nose);

      // Cabin Canopy Glass
      const cabinGeo = new THREE.BoxGeometry(1.65, 0.55, 2.2);
      const cabin = new THREE.Mesh(cabinGeo, glassMat);
      cabin.position.set(0, 0.88, 0.1);
      car.add(cabin);

      // Hood Decal Area (Displays Arivu's photo on the front hood!)
      let decalMesh = null;
      if (isPlayer) {
        const decalGeo = new THREE.PlaneGeometry(1.6, 1.6);
        const decalMat = new THREE.MeshBasicMaterial({
          map: textureLib.hoodDecal,
          transparent: true
        });
        decalMesh = new THREE.Mesh(decalGeo, decalMat);
        decalMesh.rotation.x = -Math.PI / 2;
        decalMesh.position.set(0, 0.69, -1.2);
        car.add(decalMesh);
      }

      // Driver avatar in cockpit (Arivu!)
      let driverHead = null;
      if (isPlayer) {
        const driverGroup = new THREE.Group();

        // Torso with black shirt
        const torsoGeo = new THREE.BoxGeometry(0.75, 0.65, 0.45);
        const torsoMat = new THREE.MeshStandardMaterial({ color: 0x111827 });
        const torso = new THREE.Mesh(torsoGeo, torsoMat);
        torso.position.set(0, 0.75, 0.3);
        driverGroup.add(torso);

        // Driver Head: 3D head cube with Arivu's face on BOTH front and rear faces!
        const faceMat = new THREE.MeshStandardMaterial({
          map: textureLib.driverFace,
          roughness: 0.5
        });
        const hairMat = new THREE.MeshStandardMaterial({
          color: 0x11141c,
          roughness: 0.8
        });

        // Box faces: [right, left, top, bottom, front, back]
        const headMaterials = [hairMat, hairMat, hairMat, hairMat, faceMat, faceMat];
        const headGeo = new THREE.BoxGeometry(0.55, 0.55, 0.55);
        driverHead = new THREE.Mesh(headGeo, headMaterials);
        driverHead.position.set(0, 1.28, 0.3);
        driverGroup.add(driverHead);

        // Mini steering wheel
        const wheelRingGeo = new THREE.TorusGeometry(0.22, 0.04, 8, 16);
        const wheelRingMat = new THREE.MeshStandardMaterial({ color: 0x334155 });
        const stWheel = new THREE.Mesh(wheelRingGeo, wheelRingMat);
        stWheel.rotation.x = Math.PI / 3;
        stWheel.position.set(0, 0.88, -0.05);
        driverGroup.add(stWheel);

        car.add(driverGroup);
        car.driverHead = driverHead;
      }

      // Carbon fiber rear spoiler
      const wingGeo = new THREE.BoxGeometry(2.2, 0.08, 0.45);
      const wing = new THREE.Mesh(wingGeo, darkMat);
      wing.position.set(0, 1.18, 2.0);

      const strutGeo = new THREE.BoxGeometry(0.08, 0.5, 0.2);
      const strutL = new THREE.Mesh(strutGeo, darkMat);
      strutL.position.set(-0.65, 0.88, 1.95);
      const strutR = new THREE.Mesh(strutGeo, darkMat);
      strutR.position.set(0.65, 0.88, 1.95);
      car.add(wing);
      car.add(strutL);
      car.add(strutR);

      // Front Headlights
      const lightGeo = new THREE.BoxGeometry(0.5, 0.16, 0.1);
      const lightMat = new THREE.MeshStandardMaterial({
        color: 0x00f0ff,
        emissive: 0x00f0ff,
        emissiveIntensity: 2.5
      });
      const lightL = new THREE.Mesh(lightGeo, lightMat);
      lightL.position.set(-0.7, 0.45, -2.95);
      const lightR = new THREE.Mesh(lightGeo, lightMat);
      lightR.position.set(0.7, 0.45, -2.95);
      car.add(lightL);
      car.add(lightR);

      // Rear Brake Lights
      const brakeGeo = new THREE.BoxGeometry(1.9, 0.14, 0.08);
      const brakeMat = new THREE.MeshStandardMaterial({
        color: 0xff0044,
        emissive: 0xff0044,
        emissiveIntensity: 1.5
      });
      const brakeMesh = new THREE.Mesh(brakeGeo, brakeMat);
      brakeMesh.position.set(0, 0.55, 2.22);
      car.add(brakeMesh);
      car.brakeMesh = brakeMesh;

      // Exhaust Pipes
      const exhaustGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.35, 12);
      const exhaustMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.95 });
      const exhL = new THREE.Mesh(exhaustGeo, exhaustMat);
      exhL.rotation.x = Math.PI / 2;
      exhL.position.set(-0.45, 0.3, 2.2);
      const exhR = new THREE.Mesh(exhaustGeo, exhaustMat);
      exhR.rotation.x = Math.PI / 2;
      exhR.position.set(0.45, 0.3, 2.2);
      car.add(exhL);
      car.add(exhR);

      // Underglow Neon Glow
      const underglowGeo = new THREE.PlaneGeometry(2.0, 3.8);
      const underglowMat = new THREE.MeshBasicMaterial({
        color: colorHex,
        transparent: true,
        opacity: 0.55,
        side: THREE.DoubleSide
      });
      const underglow = new THREE.Mesh(underglowGeo, underglowMat);
      underglow.rotation.x = -Math.PI / 2;
      underglow.position.y = 0.08;
      car.add(underglow);

      if (isPlayer) {
        // Dynamic Player Point Lights
        const underglowLight = new THREE.PointLight(0x00f0ff, 2.2, 7);
        underglowLight.position.set(0, 0.3, 0);
        car.add(underglowLight);

        const headSpotL = new THREE.SpotLight(0x00f0ff, 3.0, 45, Math.PI / 5, 0.4);
        headSpotL.position.set(-0.7, 0.5, -2.8);
        headSpotL.target.position.set(-0.7, 0.2, -20);
        car.add(headSpotL);
        car.add(headSpotL.target);

        const headSpotR = new THREE.SpotLight(0x00f0ff, 3.0, 45, Math.PI / 5, 0.4);
        headSpotR.position.set(0.7, 0.5, -2.8);
        headSpotR.target.position.set(0.7, 0.2, -20);
        car.add(headSpotR);
        car.add(headSpotR.target);
      }

      // Wheels
      const wheels = [];
      const wheelPos = [
        { x: -1.1, y: 0.4, z: -1.35, isFront: true },
        { x: 1.1, y: 0.4, z: -1.35, isFront: true },
        { x: -1.1, y: 0.45, z: 1.35, isFront: false },
        { x: 1.1, y: 0.45, z: 1.35, isFront: false }
      ];

      const tireGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.34, 18);
      const tireMat = new THREE.MeshStandardMaterial({ color: 0x11141c, roughness: 0.8 });
      const rimGeo = new THREE.CylinderGeometry(0.26, 0.26, 0.36, 12);
      const rimMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.95, roughness: 0.15 });

      wheelPos.forEach(wp => {
        const wGroup = new THREE.Group();
        const tire = new THREE.Mesh(tireGeo, tireMat);
        tire.rotation.z = Math.PI / 2;
        tire.castShadow = true;
        const rim = new THREE.Mesh(rimGeo, rimMat);
        rim.rotation.z = Math.PI / 2;
        wGroup.add(tire);
        wGroup.add(rim);

        wGroup.position.set(wp.x, wp.y, wp.z);
        car.add(wGroup);
        wheels.push({ mesh: wGroup, isFront: wp.isFront });
      });

      car.wheels = wheels;
      car.decalMesh = decalMesh;
      return car;
    }

    /* =========================================================================
       PARTICLE SYSTEM (Nitro Flame, Drift Smoke, Sparks)
       ========================================================================= */
    class ParticleManager {
      constructor() {
        this.particles = [];
        this.maxParticles = 180;

        const pGeo = new THREE.BufferGeometry();
        this.positions = new Float32Array(this.maxParticles * 3);
        this.colors = new Float32Array(this.maxParticles * 3);
        pGeo.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
        pGeo.setAttribute('color', new THREE.BufferAttribute(this.colors, 3));

        const pMat = new THREE.PointsMaterial({
          size: 0.65,
          vertexColors: true,
          transparent: true,
          opacity: 0.9,
          blending: THREE.AdditiveBlending
        });

        this.pointsMesh = new THREE.Points(pGeo, pMat);
        scene.add(this.pointsMesh);
      }

      emit(pos, velocity, color, life = 0.5, size = 0.5) {
        if (this.particles.length >= this.maxParticles) {
          this.particles.shift();
        }
        this.particles.push({
          pos: pos.clone(),
          vel: velocity.clone(),
          color: color.clone(),
          life: life,
          maxLife: life,
          size: size
        });
      }

      update(dt) {
        for (let i = this.particles.length - 1; i >= 0; i--) {
          const p = this.particles[i];
          p.life -= dt;
          if (p.life <= 0) {
            this.particles.splice(i, 1);
            continue;
          }
          p.pos.addScaledVector(p.vel, dt);
        }

        for (let i = 0; i < this.maxParticles; i++) {
          const idx = i * 3;
          if (i < this.particles.length) {
            const p = this.particles[i];
            const alpha = p.life / p.maxLife;
            this.positions[idx] = p.pos.x;
            this.positions[idx + 1] = p.pos.y;
            this.positions[idx + 2] = p.pos.z;

            this.colors[idx] = p.color.r * alpha;
            this.colors[idx + 1] = p.color.g * alpha;
            this.colors[idx + 2] = p.color.b * alpha;
          } else {
            this.positions[idx + 1] = -9999;
          }
        }
        this.pointsMesh.geometry.attributes.position.needsUpdate = true;
        this.pointsMesh.geometry.attributes.color.needsUpdate = true;
      }
    }

    let particles;

    /* =========================================================================
       COLLECTIBLES (Offer Letters, Nitro, Stars)
       ========================================================================= */
    const collectibles = [];
    function buildCollectibles() {
      const types = ['offer', 'nitro', 'star'];
      const offerMat = new THREE.MeshStandardMaterial({
        color: 0xffd700,
        metalness: 0.8,
        roughness: 0.2,
        emissive: 0xffb703,
        emissiveIntensity: 0.4
      });
      const nitroMat = new THREE.MeshStandardMaterial({
        color: 0x00f0ff,
        metalness: 0.7,
        roughness: 0.3,
        emissive: 0x00f0ff,
        emissiveIntensity: 0.6
      });
      const starMat = new THREE.MeshStandardMaterial({
        color: 0xff007b,
        metalness: 0.6,
        roughness: 0.2,
        emissive: 0xff007b,
        emissiveIntensity: 0.5
      });

      for (let i = 0; i < 30; i++) {
        const t = (i / 30) + 0.02;
        const type = types[i % 3];
        const s = trackSamples[Math.floor(t * trackSegments) % trackSegments];
        const laneOffset = ((i % 5) - 2) * 3.8;
        const pos = s.pt.clone().add(s.binormal.clone().multiplyScalar(laneOffset));
        pos.y += 1.4;

        let mesh;
        if (type === 'offer') {
          const bGeo = new THREE.BoxGeometry(1.2, 0.9, 0.4);
          mesh = new THREE.Mesh(bGeo, offerMat);
        } else if (type === 'nitro') {
          const nGeo = new THREE.CylinderGeometry(0.4, 0.4, 1.2, 16);
          mesh = new THREE.Mesh(nGeo, nitroMat);
        } else {
          const sGeo = new THREE.OctahedronGeometry(0.7, 0);
          mesh = new THREE.Mesh(sGeo, starMat);
        }

        mesh.position.copy(pos);
        scene.add(mesh);

        collectibles.push({
          mesh: mesh,
          type: type,
          baseY: pos.y,
          active: true,
          respawnTimer: 0
        });
      }
    }

    function updateCollectibles(dt, playerCar) {
      const time = clock.getElapsedTime();
      collectibles.forEach((item, idx) => {
        if (!item.active) {
          item.respawnTimer -= dt;
          if (item.respawnTimer <= 0) {
            item.active = true;
            item.mesh.visible = true;
          }
          return;
        }

        item.mesh.rotation.y += dt * 2.5;
        item.mesh.rotation.x = Math.sin(time * 3 + idx) * 0.2;
        item.mesh.position.y = item.baseY + Math.sin(time * 4 + idx) * 0.35;

        const dist = playerCar.group.position.distanceTo(item.mesh.position);
        if (dist < 2.8) {
          collectItem(item);
        }
      });
    }

    function collectItem(item) {
      item.active = false;
      item.mesh.visible = false;
      item.respawnTimer = 12;

      sound.playChime();

      if (item.type === 'offer') {
        gameState.score += 500;
        playerCar.nitro = Math.min(100, playerCar.nitro + 50);
        showToast('💼 JOB OFFER LETTER ACCEPTED! +500 PTS', 'gold');
      } else if (item.type === 'nitro') {
        playerCar.nitro = 100;
        gameState.score += 200;
        showToast('⚡ FULL NITRO RECHARGE! +200 PTS', 'boost');
      } else {
        gameState.score += 350;
        showToast('⭐ CAREER SKILL BADGE! +350 PTS', '');
      }
    }

    /* =========================================================================
       AI RIVAL RACERS
       ========================================================================= */
    const rivals = [];
    function initRivals() {
      const rivalData = [
        { name: 'Apex', color: 0xff0044, startT: 0.04, lane: -4.5, baseSpeed: 54 },
        { name: 'Viper', color: 0xffb703, startT: 0.03, lane: 4.5, baseSpeed: 52 },
        { name: 'Phantom', color: 0x9d4edd, startT: 0.02, lane: -2.0, baseSpeed: 50 },
        { name: 'Volt', color: 0x06d6a0, startT: 0.01, lane: 2.5, baseSpeed: 48 }
      ];

      rivalData.forEach(data => {
        const mesh = createCarMesh(data.color, false);
        scene.add(mesh);
        rivals.push({
          name: data.name,
          mesh: mesh,
          t: data.startT,
          lap: 1,
          lane: data.lane,
          targetLane: data.lane,
          laneTimer: Math.random() * 5,
          speed: data.baseSpeed,
          baseSpeed: data.baseSpeed,
          totalDistance: data.startT * trackLength
        });
      });
    }

    function updateRivals(dt) {
      rivals.forEach(r => {
        r.laneTimer -= dt;
        if (r.laneTimer <= 0) {
          r.laneTimer = 3 + Math.random() * 4;
          r.targetLane = (Math.random() - 0.5) * (trackWidth - 8);
          r.speed = r.baseSpeed + (Math.random() - 0.5) * 6;
        }

        r.lane += (r.targetLane - r.lane) * dt * 1.5;

        const deltaT = (r.speed * dt) / trackLength;
        const prevT = r.t;
        r.t = (r.t + deltaT) % 1.0;
        if (r.t < prevT) {
          r.lap++;
        }
        r.totalDistance = (r.lap - 1) * trackLength + r.t * trackLength;

        const pt = trackCurve.getPointAt(r.t);
        const tangent = trackCurve.getTangentAt(r.t);
        const binormal = new THREE.Vector3().crossVectors(tangent, new THREE.Vector3(0, 1, 0)).normalize();

        const carPos = pt.clone().add(binormal.clone().multiplyScalar(r.lane));
        r.mesh.position.copy(carPos);
        r.mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, -1), tangent);

        r.mesh.wheels.forEach(w => {
          w.mesh.rotation.x += r.speed * dt * 2.5;
        });

        const distToPlayer = playerCar.group.position.distanceTo(r.mesh.position);
        if (distToPlayer < 3.2 && playerCar.speed > 40 && !r.nearMissed) {
          r.nearMissed = true;
          gameState.score += 150;
          showToast(`🔥 NEAR MISS WITH ${r.name.toUpperCase()}! +150 PTS`, 'boost');
          setTimeout(() => { r.nearMissed = false; }, 3000);
        }

        if (distToPlayer < 2.2) {
          sound.playBump();
          playerCar.speed *= 0.85;
          const pushDir = playerCar.group.position.clone().sub(r.mesh.position).normalize();
          playerCar.group.position.addScaledVector(pushDir, 0.4);
        }
      });
    }

    /* =========================================================================
       PLAYER VEHICLE & PHYSICS ENGINE
       ========================================================================= */
    const playerCar = {
      group: null,
      decalMesh: null,
      driverHead: null,
      wheels: [],
      brakeMesh: null,
      // Dynamics
      speed: 0,
      maxSpeed: 64,      // ~230 km/h standard
      nitroMaxSpeed: 86, // ~310 km/h on nitro
      accel: 26,
      brakePower: 40,
      friction: 0.985,
      steerAngle: 0,
      heading: 0,
      driftAngle: 0,
      isDrifting: false,
      driftScore: 0,
      nitro: 100,
      nitroActive: false,
      rpm: 1000,
      gear: 1,
      // Progression
      trackT: 0,
      lap: 1,
      totalDistance: 0
    };

    function initPlayerVehicle() {
      playerCar.group = createCarMesh(0x00f0ff, true);
      scene.add(playerCar.group);

      const startPt = trackCurve.getPointAt(0);
      const tangent = trackCurve.getTangentAt(0);
      playerCar.group.position.copy(startPt);
      playerCar.group.position.y = 0;
      playerCar.heading = Math.atan2(-tangent.x, -tangent.z);
      playerCar.group.rotation.y = playerCar.heading;
    }

    const keys = {
      up: false,
      down: false,
      left: false,
      right: false,
      space: false,
      shift: false
    };

    window.addEventListener('keydown', e => {
      sound.init();
      if (e.code === 'KeyW' || e.code === 'ArrowUp') keys.up = true;
      if (e.code === 'KeyS' || e.code === 'ArrowDown') keys.down = true;
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
      if (e.code === 'Space') { keys.space = true; e.preventDefault(); }
      if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') keys.shift = true;
      if (e.code === 'KeyC') cycleCamera();
      if (e.code === 'KeyM') toggleMute();
      if (e.code === 'KeyP' || e.code === 'Escape') togglePause();
    });

    window.addEventListener('keyup', e => {
      if (e.code === 'KeyW' || e.code === 'ArrowUp') keys.up = false;
      if (e.code === 'KeyS' || e.code === 'ArrowDown') keys.down = false;
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = false;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = false;
      if (e.code === 'Space') keys.space = false;
      if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') keys.shift = false;
    });

    function setupTouchEvents() {
      const bindTouch = (id, keyName) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('touchstart', (e) => { e.preventDefault(); sound.init(); keys[keyName] = true; });
        el.addEventListener('touchend', (e) => { e.preventDefault(); keys[keyName] = false; });
      };
      bindTouch('touch-left', 'left');
      bindTouch('touch-right', 'right');
      bindTouch('touch-gas', 'up');
      bindTouch('touch-brake', 'down');
      bindTouch('touch-nitro', 'space');
    }

    function updatePlayerPhysics(dt) {
      if (gameState.state !== 'racing') return;

      const p = playerCar;

      // Nitro
      if (keys.space && p.nitro > 0 && p.speed > 5) {
        p.nitroActive = true;
        p.nitro = Math.max(0, p.nitro - dt * 25);
        sound.setNitro(true);
      } else {
        p.nitroActive = false;
        sound.setNitro(false);
      }

      const currentMaxSpeed = p.nitroActive ? p.nitroMaxSpeed : p.maxSpeed;
      const accelMulti = p.nitroActive ? 1.85 : 1.0;

      // Throttle
      let throttle = 0;
      if (keys.up) {
        throttle = 1;
        if (p.speed < currentMaxSpeed) {
          p.speed += p.accel * accelMulti * dt;
        }
      } else if (keys.down) {
        if (p.speed > 1) {
          throttle = -1;
          p.speed -= p.brakePower * dt;
        } else {
          p.speed = Math.max(-14, p.speed - p.accel * 0.5 * dt);
        }
      } else {
        p.speed *= Math.pow(p.friction, dt * 60);
        if (Math.abs(p.speed) < 0.1) p.speed = 0;
      }

      // Steering
      const steerSpeed = 3.6;
      let targetSteer = 0;
      if (keys.left) targetSteer = 0.55;
      if (keys.right) targetSteer = -0.55;

      p.steerAngle += (targetSteer - p.steerAngle) * steerSpeed * dt;

      // Drift
      const isSharpTurn = Math.abs(p.steerAngle) > 0.35 && Math.abs(p.speed) > 28;
      p.isDrifting = (keys.shift && Math.abs(p.speed) > 15) || isSharpTurn;

      const turnFactor = p.isDrifting ? 1.6 : 1.0;
      const speedSteerRatio = Math.min(1.0, Math.abs(p.speed) / 25);
      p.heading += p.steerAngle * speedSteerRatio * turnFactor * dt * 2.2;

      const targetDriftAngle = p.isDrifting ? p.steerAngle * 0.8 : 0;
      p.driftAngle += (targetDriftAngle - p.driftAngle) * 6 * dt;

      if (p.isDrifting && Math.abs(p.speed) > 20) {
        p.driftScore += dt * 320;
        sound.setDrift(true, Math.abs(p.steerAngle) * 2);
        document.getElementById('drift-alert').style.display = 'block';
        document.getElementById('drift-alert').innerText = `DRIFT +${Math.floor(p.driftScore)}`;
      } else {
        if (p.driftScore > 50) {
          gameState.score += Math.floor(p.driftScore);
          showToast(`✨ DRIFT BONUS +${Math.floor(p.driftScore)} PTS`, 'gold');
        }
        p.driftScore = 0;
        sound.setDrift(false);
        document.getElementById('drift-alert').style.display = 'none';
      }

      const moveAngle = p.heading + p.driftAngle;
      const forwardX = -Math.sin(moveAngle);
      const forwardZ = -Math.cos(moveAngle);

      p.group.position.x += forwardX * p.speed * dt;
      p.group.position.z += forwardZ * p.speed * dt;
      p.group.rotation.y = p.heading + p.driftAngle;

      p.group.rotation.x = (keys.up ? 0.03 : 0) - (keys.down ? 0.05 : 0);
      p.group.rotation.z = -p.steerAngle * (p.speed / p.maxSpeed) * 0.12;

      if (p.driverHead) {
        p.driverHead.rotation.y = -p.steerAngle * 0.4;
        p.driverHead.rotation.x = (keys.up ? -0.1 : 0) + (keys.down ? 0.15 : 0);
      }

      p.wheels.forEach(w => {
        w.mesh.rotation.x += p.speed * dt * 2.5;
        if (w.isFront) {
          w.mesh.rotation.y = p.steerAngle * 0.6;
        }
      });

      if (p.brakeMesh) {
        p.brakeMesh.material.emissiveIntensity = keys.down ? 3.5 : 1.2;
      }

      checkTrackBoundary(p);
      emitVehicleParticles(p, dt);
      calculateRpmAndGear(p, throttle);
      sound.updateEngine(p.rpm / 8000, Math.abs(throttle), Math.abs(p.speed) / p.maxSpeed);
      updatePlayerRaceProgress(p);
    }

    function checkTrackBoundary(p) {
      let minDist = Infinity;
      let closestIdx = 0;
      const pPos = p.group.position;

      for (let i = 0; i < trackSegments; i += 4) {
        const d = pPos.distanceTo(trackSamples[i].pt);
        if (d < minDist) {
          minDist = d;
          closestIdx = i;
        }
      }

      const sample = trackSamples[closestIdx];
      const toCar = pPos.clone().sub(sample.pt);
      const lateralDist = toCar.dot(sample.binormal);

      p.group.position.y = sample.pt.y;

      const roadLimit = trackWidth / 2 - 0.5;
      if (Math.abs(lateralDist) > roadLimit) {
        sound.playBump();
        p.speed = Math.max(-5, p.speed * 0.88);
        const overDist = Math.abs(lateralDist) - roadLimit;
        const pushDir = lateralDist > 0 ? -1 : 1;
        pPos.addScaledVector(sample.binormal, pushDir * (overDist + 0.3));

        triggerCameraShake(0.25);
        for (let k = 0; k < 5; k++) {
          particles.emit(
            pPos.clone().add(new THREE.Vector3((Math.random() - 0.5) * 1.5, 0.5, (Math.random() - 0.5) * 1.5)),
            new THREE.Vector3((Math.random() - 0.5) * 8, Math.random() * 6, (Math.random() - 0.5) * 8),
            new THREE.Color(1, 0.85, 0.3),
            0.25
          );
        }
      }
    }

    function emitVehicleParticles(p, dt) {
      if (p.nitroActive) {
        const exhOffsets = [-0.45, 0.45];
        exhOffsets.forEach(ox => {
          const flamePos = p.group.position.clone().add(
            new THREE.Vector3(ox, 0.35, 2.2).applyEuler(p.group.rotation)
          );
          const flameVel = new THREE.Vector3((Math.random() - 0.5) * 2, (Math.random() - 0.5) * 2, 14)
            .applyEuler(p.group.rotation);
          particles.emit(flamePos, flameVel, new THREE.Color(0, 0.95, 1), 0.25);
        });
      }

      if (p.isDrifting && Math.abs(p.speed) > 15) {
        const wheelOffsets = [-1.1, 1.1];
        wheelOffsets.forEach(ox => {
          const smokePos = p.group.position.clone().add(
            new THREE.Vector3(ox, 0.1, 1.35).applyEuler(p.group.rotation)
          );
          const smokeVel = new THREE.Vector3((Math.random() - 0.5) * 4, 1.5 + Math.random() * 2, (Math.random() - 0.5) * 4);
          particles.emit(smokePos, smokeVel, new THREE.Color(0.85, 0.85, 0.95), 0.45);
        });
      }
    }

    function calculateRpmAndGear(p, throttle) {
      const kmh = Math.abs(p.speed) * 3.6;
      if (kmh < 40) p.gear = 1;
      else if (kmh < 85) p.gear = 2;
      else if (kmh < 135) p.gear = 3;
      else if (kmh < 190) p.gear = 4;
      else if (kmh < 250) p.gear = 5;
      else p.gear = 6;

      const gearMinSpeed = [0, 0, 40, 85, 135, 190, 250][p.gear];
      const gearMaxSpeed = [0, 40, 85, 135, 190, 250, 320][p.gear];
      const ratio = (kmh - gearMinSpeed) / (gearMaxSpeed - gearMinSpeed);
      p.rpm = 2000 + Math.min(1.0, Math.max(0, ratio)) * 5800 + (throttle > 0 ? 400 : 0);
    }

    function updatePlayerRaceProgress(p) {
      let minDist = Infinity;
      let closestIdx = 0;
      for (let i = 0; i < trackSegments; i += 2) {
        const d = p.group.position.distanceTo(trackSamples[i].pt);
        if (d < minDist) {
          minDist = d;
          closestIdx = i;
        }
      }

      const prevT = p.trackT;
      p.trackT = closestIdx / trackSegments;

      if (prevT > 0.85 && p.trackT < 0.15) {
        p.lap++;
        onLapComplete(p.lap);
      }
      p.totalDistance = (p.lap - 1) * trackLength + p.trackT * trackLength;
    }

    /* =========================================================================
       CAMERA MODES
       ========================================================================= */
    let cameraShake = 0;

    function triggerCameraShake(amount = 0.3) {
      cameraShake = amount;
    }

    function updateCamera(dt) {
      const p = playerCar;
      const mode = viewModes[currentViewModeIndex];

      if (cameraShake > 0) {
        cameraShake -= dt * 1.5;
        if (cameraShake < 0) cameraShake = 0;
      }
      const shakeOffset = new THREE.Vector3(
        (Math.random() - 0.5) * cameraShake,
        (Math.random() - 0.5) * cameraShake,
        (Math.random() - 0.5) * cameraShake
      );

      const targetFov = p.nitroActive ? 78 : (62 + (Math.abs(p.speed) / p.maxSpeed) * 8);
      camera.fov += (targetFov - camera.fov) * dt * 4;
      camera.updateProjectionMatrix();

      const speedLinesCanvas = document.getElementById('speed-lines');
      if (p.speed > 55 || p.nitroActive) {
        speedLinesCanvas.style.opacity = Math.min(0.8, (p.speed - 50) / 30);
      } else {
        speedLinesCanvas.style.opacity = '0';
      }

      if (mode === 'chase') {
        const chaseDist = 6.8 + (Math.abs(p.speed) / p.maxSpeed) * 1.5;
        const chaseHeight = 2.8;
        const idealOffset = new THREE.Vector3(0, chaseHeight, chaseDist).applyEuler(new THREE.Euler(0, p.heading, 0));
        const idealPos = p.group.position.clone().add(idealOffset);

        camera.position.lerp(idealPos, dt * 7);
        camera.position.add(shakeOffset);

        const lookTarget = p.group.position.clone().add(new THREE.Vector3(0, 1.2, 0));
        camera.lookAt(lookTarget);

      } else if (mode === 'hood') {
        const hoodPos = p.group.position.clone().add(
          new THREE.Vector3(0, 0.85, -1.2).applyEuler(new THREE.Euler(0, p.heading, 0))
        );
        camera.position.copy(hoodPos).add(shakeOffset);

        const lookTarget = p.group.position.clone().add(
          new THREE.Vector3(0, 0.8, -20).applyEuler(new THREE.Euler(0, p.heading, 0))
        );
        camera.lookAt(lookTarget);

      } else if (mode === 'cockpit') {
        const cockPos = p.group.position.clone().add(
          new THREE.Vector3(0, 1.35, 0.6).applyEuler(new THREE.Euler(0, p.heading, 0))
        );
        camera.position.copy(cockPos).add(shakeOffset);

        const lookTarget = p.group.position.clone().add(
          new THREE.Vector3(0, 1.2, -15).applyEuler(new THREE.Euler(0, p.heading, 0))
        );
        camera.lookAt(lookTarget);

      } else if (mode === 'drone') {
        const dronePos = p.group.position.clone().add(
          new THREE.Vector3(12, 14, 12)
        );
        camera.position.lerp(dronePos, dt * 3);
        camera.lookAt(p.group.position);
      }
    }

    function cycleCamera() {
      currentViewModeIndex = (currentViewModeIndex + 1) % viewModes.length;
      showToast(`CAMERA: ${viewModes[currentViewModeIndex].toUpperCase()}`, '');
    }

    /* =========================================================================
       GAME STATE & HUD
       ========================================================================= */
    const gameState = {
      state: 'menu',
      mode: 'gp',
      score: 0,
      totalTime: 0,
      lapTime: 0,
      maxSpeedRecord: 0,
      topPosition: 1
    };

    function setGameMode(mode) {
      gameState.mode = mode;
      document.getElementById('mode-gp').classList.toggle('active', mode === 'gp');
      document.getElementById('mode-endless').classList.toggle('active', mode === 'endless');
      document.getElementById('hud-lap-container').style.display = mode === 'gp' ? 'block' : 'none';
    }

    function startGame() {
      sound.init();
      document.getElementById('title-modal').style.display = 'none';
      document.getElementById('finish-modal').style.display = 'none';
      document.getElementById('pause-modal').style.display = 'none';

      gameState.state = 'racing';
      gameState.score = 0;
      gameState.totalTime = 0;
      gameState.lapTime = 0;
      gameState.maxSpeedRecord = 0;

      playerCar.speed = 0;
      playerCar.nitro = 100;
      playerCar.lap = 1;
      playerCar.trackT = 0;
      playerCar.totalDistance = 0;

      const startPt = trackCurve.getPointAt(0);
      const tangent = trackCurve.getTangentAt(0);
      playerCar.group.position.copy(startPt);
      playerCar.heading = Math.atan2(-tangent.x, -tangent.z);
      playerCar.group.rotation.y = playerCar.heading;

      showToast('🏁 GREEN LIGHT! GO ARIVU!', 'boost');
    }

    function onLapComplete(newLap) {
      if (gameState.mode === 'gp') {
        if (newLap <= 3) {
          showToast(`🚩 COMPLETED LAP ${newLap - 1}! STARTING LAP ${newLap}/3`, 'gold');
          gameState.score += 1000;
        } else {
          finishRace();
        }
      } else {
        showToast(`🚩 LAP ${newLap} PASSED! +1000 BONUS`, 'boost');
        gameState.score += 1000;
      }
    }

    function finishRace() {
      gameState.state = 'finished';
      const isWinner = gameState.topPosition === 1;

      document.getElementById('finish-title').innerText = isWinner ? '🏆 GRAND PRIX CHAMPION!' : 'RACE FINISHED!';
      document.getElementById('finish-msg').innerHTML = isWinner
        ? `<strong>Arivu</strong> dominates the circuit and claims 1st Place! #OPENTOWORK Offer letters unlocked!`
        : `Great race! Arivu finished with elite driving performance.`;

      document.getElementById('res-pos').innerText = `${gameState.topPosition}${getOrdinal(gameState.topPosition)} Place`;
      document.getElementById('res-time').innerText = formatTime(gameState.totalTime);
      document.getElementById('res-speed').innerText = `${Math.floor(gameState.maxSpeedRecord)} KM/H`;
      document.getElementById('res-score').innerText = `${gameState.score.toLocaleString()} PTS`;

      document.getElementById('finish-modal').style.display = 'flex';
      sound.playChime();
    }

    function togglePause() {
      if (gameState.state === 'racing') {
        gameState.state = 'paused';
        document.getElementById('pause-modal').style.display = 'flex';
      } else if (gameState.state === 'paused') {
        gameState.state = 'racing';
        document.getElementById('pause-modal').style.display = 'none';
      }
    }

    function toggleMute() {
      const active = sound.toggle();
      document.getElementById('btn-audio').innerText = active ? '🔊' : '🔇';
      showToast(active ? 'AUDIO: UNMUTED' : 'AUDIO: MUTED', '');
    }

    function showToast(text, type = '') {
      const container = document.getElementById('toast-box');
      const toast = document.createElement('div');
      toast.className = `toast-msg ${type}`;
      toast.innerText = text;
      container.appendChild(toast);
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 2300);
    }

    function formatTime(sec) {
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      const ms = Math.floor((sec % 1) * 10);
      return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${ms}`;
    }

    function getOrdinal(n) {
      const s = ['th', 'st', 'nd', 'rd'];
      const v = n % 100;
      return s[(v - 20) % 10] || s[v] || s[0];
    }

    /* Radar Minimap */
    const radarCanvas = document.getElementById('radar-canvas');
    const rCtx = radarCanvas.getContext('2d');

    function updateRadar() {
      rCtx.clearRect(0, 0, 145, 145);

      const centerX = 72;
      const centerY = 72;
      const scale = 0.12;

      rCtx.strokeStyle = 'rgba(0, 240, 255, 0.45)';
      rCtx.lineWidth = 3.5;
      rCtx.beginPath();
      for (let i = 0; i <= 60; i++) {
        const pt = trackCurve.getPointAt(i / 60);
        const rx = centerX + pt.x * scale;
        const ry = centerY + pt.z * scale;
        if (i === 0) rCtx.moveTo(rx, ry);
        else rCtx.lineTo(rx, ry);
      }
      rCtx.closePath();
      rCtx.stroke();

      rivals.forEach(r => {
        const rx = centerX + r.mesh.position.x * scale;
        const ry = centerY + r.mesh.position.z * scale;
        rCtx.fillStyle = '#ff0055';
        rCtx.beginPath();
        rCtx.arc(rx, ry, 3.5, 0, Math.PI * 2);
        rCtx.fill();
      });

      const px = centerX + playerCar.group.position.x * scale;
      const py = centerY + playerCar.group.position.z * scale;
      rCtx.fillStyle = '#00f0ff';
      rCtx.shadowColor = '#00f0ff';
      rCtx.shadowBlur = 9;
      rCtx.beginPath();
      rCtx.arc(px, py, 5, 0, Math.PI * 2);
      rCtx.fill();
      rCtx.shadowBlur = 0;
    }

    function updateHUD(dt) {
      const kmh = Math.floor(Math.abs(playerCar.speed) * 3.6);
      if (kmh > gameState.maxSpeedRecord) gameState.maxSpeedRecord = kmh;

      document.getElementById('hud-speed').innerText = kmh;
      const ringOffset = 235 - (Math.min(320, kmh) / 320) * 157;
      document.getElementById('speedo-fill-ring').style.strokeDashoffset = ringOffset;

      document.getElementById('hud-gear').innerText = playerCar.speed < -1 ? 'R' : playerCar.gear;
      const rpmPercent = Math.min(100, (playerCar.rpm / 8000) * 100);
      document.getElementById('hud-rpm').style.width = `${rpmPercent}%`;

      const nitroVal = Math.floor(playerCar.nitro);
      document.getElementById('hud-nitro-val').innerText = `${nitroVal}%`;
      document.getElementById('hud-nitro-fill').style.width = `${nitroVal}%`;

      if (gameState.state === 'racing') {
        gameState.totalTime += dt;
        gameState.lapTime += dt;
        document.getElementById('hud-time').innerText = formatTime(gameState.totalTime);
        document.getElementById('hud-score').innerText = gameState.score.toLocaleString();

        if (gameState.mode === 'gp') {
          document.getElementById('hud-lap').innerText = `${Math.min(3, playerCar.lap)}/3`;
        } else {
          document.getElementById('hud-lap').innerText = `${playerCar.lap}`;
        }

        const allRacers = [
          { isPlayer: true, dist: playerCar.totalDistance },
          ...rivals.map(r => ({ isPlayer: false, dist: r.totalDistance }))
        ];
        allRacers.sort((a, b) => b.dist - a.dist);
        const playerRank = allRacers.findIndex(r => r.isPlayer) + 1;
        gameState.topPosition = playerRank;

        document.getElementById('hud-pos').innerText = `${playerRank}${getOrdinal(playerRank).toUpperCase()}`;
      }

      updateRadar();
    }

    const speedCanvas = document.getElementById('speed-lines');
    const spCtx = speedCanvas.getContext('2d');
    function resizeSpeedLines() {
      speedCanvas.width = window.innerWidth;
      speedCanvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeSpeedLines);
    resizeSpeedLines();

    function drawSpeedLines() {
      if (speedCanvas.style.opacity === '0') return;
      spCtx.clearRect(0, 0, speedCanvas.width, speedCanvas.height);
      const cx = speedCanvas.width / 2;
      const cy = speedCanvas.height / 2;
      spCtx.strokeStyle = 'rgba(0, 240, 255, 0.45)';
      spCtx.lineWidth = 2.5;
      for (let i = 0; i < 24; i++) {
        const angle = Math.random() * Math.PI * 2;
        const innerR = 140 + Math.random() * 80;
        const outerR = innerR + 100 + Math.random() * 200;
        spCtx.beginPath();
        spCtx.moveTo(cx + Math.cos(angle) * innerR, cy + Math.sin(angle) * innerR);
        spCtx.lineTo(cx + Math.cos(angle) * outerR, cy + Math.sin(angle) * outerR);
        spCtx.stroke();
      }
    }

    document.getElementById('btn-start-game').addEventListener('click', startGame);
    document.getElementById('btn-play-again').addEventListener('click', startGame);
    document.getElementById('btn-resume').addEventListener('click', togglePause);
    document.getElementById('btn-restart').addEventListener('click', startGame);
    document.getElementById('btn-cam').addEventListener('click', cycleCamera);
    document.getElementById('btn-audio').addEventListener('click', toggleMute);
    document.getElementById('btn-pause').addEventListener('click', togglePause);

    /* =========================================================================
       INITIALIZATION
       ========================================================================= */
    async function init() {
      initGraphics();
      await loadCustomTextures();
      buildTrack();
      initPlayerVehicle();
      initRivals();
      buildCollectibles();
      particles = new ParticleManager();
      setupTouchEvents();

      requestAnimationFrame(gameLoop);
    }

    let lastTime = performance.now();
    function gameLoop(now) {
      requestAnimationFrame(gameLoop);

      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      updatePlayerPhysics(dt);
      updateRivals(dt);
      updateCollectibles(dt, playerCar);
      particles.update(dt);
      updateCamera(dt);
      drawSpeedLines();
      updateHUD(dt);

      renderer.render(scene, camera);
    }

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
'''

html_final = html_content.replace("__ARIVU_IMAGE_BASE64__", b64_image)

with open("arivu_racing.html", "w", encoding="utf-8") as f:
    f.write(html_final)
print("Updated arivu_racing.html successfully.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_final)
print("Updated index.html successfully.")
