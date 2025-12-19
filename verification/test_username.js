const { JSDOM } = require("jsdom");
const { window } = new JSDOM(`<!DOCTYPE html><html><body><input id="usernameInput"><input id="apiKeyInput"><div id="settingsModal" class="hidden"></div></body></html>`);
global.window = window;
global.document = window.document;
global.localStorage = {
  getItem: (key) => global.store[key],
  setItem: (key, val) => global.store[key] = val
};
global.store = {};

// Mock Chess.js
const Chess = function() {
  this.header = () => ({ 'White': 'Hikaru', 'Black': 'Magnus' });
  this.load_pgn = () => true;
  this.history = () => [];
  this.reset = () => {};
  this.fen = () => 'startpos';
};
global.game = new Chess();
global.gameHistory = [];
global.currentMoveIndex = -1;
global.analysisData = [];
global.geminiComments = {};
global.gameStats = null;
global.isAnalyzing = false;
global.board = {
  position: () => {},
  orientation: (c) => console.log("ORIENTATION SET TO: " + c),
  resize: () => {}
};
global.updateUI = () => {};
global.stopInteractiveMode = () => {};

// Mock Element for PGN
global.document.getElementById('pgnInput') = { value: 'some pgn' };
global.document.getElementById('loadPgnBtn') = { innerText: 'Load' };
global.document.getElementById('gameStatus') = { innerText: '' };
global.document.getElementById('feedbackPlaceholder') = { innerHTML: '' };
global.document.getElementById('pgnModal') = { classList: { add: () => {} } };


// --- THE LOGIC TO TEST ---

// 1. Test Save/Load Settings
global.store = {};
// Manually setting input
document.getElementById('usernameInput').value = 'Hikaru';
// Define saveSettings (simplified version of what we wrote)
function saveSettings() {
    localStorage.setItem('chess_username', document.getElementById('usernameInput').value.trim());
}
saveSettings();
console.log("Saved Username: " + localStorage.getItem('chess_username'));

// 2. Test Load PGN Logic
function runPgnLogic() {
    const headers = game.header();
    const username = localStorage.getItem('chess_username');
    let orient = 'white';

    if (username && headers) {
        const userLower = username.toLowerCase();
        if (headers['White'] && headers['White'].toLowerCase() === userLower) orient = 'white';
        else if (headers['Black'] && headers['Black'].toLowerCase() === userLower) orient = 'black';
    }
    board.orientation(orient);
}

console.log("--- TEST 1: User is White (Hikaru) ---");
runPgnLogic();

console.log("--- TEST 2: User is Black (Magnus) ---");
localStorage.setItem('chess_username', 'Magnus');
runPgnLogic();

console.log("--- TEST 3: User is Unknown (Gary) ---");
localStorage.setItem('chess_username', 'Gary');
runPgnLogic();

console.log("--- TEST 4: Case Insensitivity (magnus) ---");
localStorage.setItem('chess_username', 'magnus');
runPgnLogic();
