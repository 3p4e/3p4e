import { TEAM, TEAM_INFO, RULES } from './config.js';

const $ = (id) => document.getElementById(id);

export class UI {
  constructor() {
    this.healthFill = $('healthFill');
    this.healthText = $('healthText');
    this.scoreRed = $('scoreRed');
    this.scoreBlue = $('scoreBlue');
    this.scoreRedBar = $('scoreRedBar');
    this.scoreBlueBar = $('scoreBlueBar');
    this.blockSwatch = $('blockSwatch');
    this.blockName = $('blockName');
    this.killfeed = $('killfeed');
    this.respawn = $('respawn');
    this.respawnText = $('respawnText');
    this.start = $('start');
    this.win = $('win');
    this.winText = $('winText');
    this.winSub = $('winSub');
    this.scoreboard = $('scoreboard');
    this.sbBody = $('sbBody');
    this.crosshair = $('crosshair');
  }

  setHealth(hp, max) {
    const pct = Math.max(0, Math.min(1, hp / max));
    this.healthFill.style.width = (pct * 100).toFixed(0) + '%';
    this.healthFill.style.background =
      pct > 0.5 ? '#06d6a0' : pct > 0.25 ? '#ffd166' : '#ef476f';
    this.healthText.textContent = Math.ceil(hp);
  }

  setScores(red, blue) {
    this.scoreRed.textContent = red;
    this.scoreBlue.textContent = blue;
    this.scoreRedBar.style.width = Math.min(100, (red / RULES.scoreToWin) * 100) + '%';
    this.scoreBlueBar.style.width = Math.min(100, (blue / RULES.scoreToWin) * 100) + '%';
  }

  setBlock(name, cssColor) {
    this.blockSwatch.style.background = cssColor;
    this.blockName.textContent = name;
  }

  addKill(killerName, victimName, killerTeam) {
    const el = document.createElement('div');
    el.className = 'kill';
    const c = TEAM_INFO[killerTeam].css;
    el.innerHTML = `<span style="color:${c}">${killerName}</span> <span class="sk">▸</span> ${victimName}`;
    this.killfeed.appendChild(el);
    setTimeout(() => {
      el.classList.add('fade');
      setTimeout(() => el.remove(), 600);
    }, 3500);
    // Cap the feed length.
    while (this.killfeed.children.length > 6) this.killfeed.firstChild.remove();
  }

  showRespawn(seconds) {
    this.respawn.style.display = 'flex';
    this.respawnText.textContent = Math.ceil(seconds);
  }
  hideRespawn() {
    this.respawn.style.display = 'none';
  }

  showStart(show) {
    this.start.style.display = show ? 'flex' : 'none';
  }

  showWin(team) {
    this.win.style.display = 'flex';
    const info = TEAM_INFO[team];
    this.winText.textContent = info.name + ' TEAM WINS';
    this.winText.style.color = info.css;
    this.winSub.textContent = 'Click to play again';
  }
  hideWin() {
    this.win.style.display = 'none';
  }

  setCrosshairMode(alive) {
    this.crosshair.style.opacity = alive ? '1' : '0.25';
  }

  showScoreboard(show, combatants, scores) {
    this.scoreboard.style.display = show ? 'block' : 'none';
    if (!show) return;
    const rows = combatants
      .map((c) => ({
        name: c.isPlayer ? 'You' : (c.team === TEAM.RED ? 'Red Bot' : 'Blue Bot') + ' #' + (c.id ?? 0),
        team: c.team,
        kills: c.kills || 0,
        deaths: c.deaths || 0,
        isPlayer: !!c.isPlayer,
      }))
      .sort((a, b) => b.kills - a.kills);

    let html = `<div class="sbhead"><span style="color:${TEAM_INFO[TEAM.RED].css}">RED ${scores[TEAM.RED]}</span> — <span style="color:${TEAM_INFO[TEAM.BLUE].css}">BLUE ${scores[TEAM.BLUE]}</span></div>`;
    html += '<table><tr><th>Player</th><th>Team</th><th>K</th><th>D</th></tr>';
    for (const r of rows) {
      const c = TEAM_INFO[r.team].css;
      html += `<tr${r.isPlayer ? ' class="me"' : ''}><td>${r.name}</td><td style="color:${c}">${TEAM_INFO[r.team].name}</td><td>${r.kills}</td><td>${r.deaths}</td></tr>`;
    }
    html += '</table>';
    this.sbBody.innerHTML = html;
  }
}
