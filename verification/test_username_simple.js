
global.store = {};
global.localStorage = {
  getItem: (key) => global.store[key],
  setItem: (key, val) => global.store[key] = val
};

global.document = {
    getElementById: (id) => {
        if (!global.elements[id]) global.elements[id] = { value: '' };
        return global.elements[id];
    }
};
global.elements = {};

global.board = {
  orientation: (c) => console.log("ORIENTATION SET TO: " + c)
};

global.game = {
    header: () => ({ 'White': 'Hikaru', 'Black': 'Magnus' })
};

// Logic under test
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
global.localStorage.setItem('chess_username', 'Hikaru');
runPgnLogic();

console.log("--- TEST 2: User is Black (Magnus) ---");
global.localStorage.setItem('chess_username', 'Magnus');
runPgnLogic();

console.log("--- TEST 3: User is Unknown (Gary) ---");
global.localStorage.setItem('chess_username', 'Gary');
runPgnLogic();

console.log("--- TEST 4: Case Insensitivity (magnus) ---");
global.localStorage.setItem('chess_username', 'magnus');
runPgnLogic();
