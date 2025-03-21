const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const BLOCK_SIZE = 20;

const COLORS = [
    '#00F0F0', // I
    '#0000F0', // J
    '#F0A000', // L
    '#F0F000', // O
    '#00F000', // S
    '#A000F0', // T
    '#F00000'  // Z
];

const GRAY = '#808080';

function drawGrid(grid) {
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[y].length; x++) {
            ctx.fillStyle = grid[y][x];
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = GRAY;
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }
    }
}

function drawPiece(piece) {
    for (let y = 0; y < piece.shape.length; y++) {
        for (let x = 0; x < piece.shape[y].length; x++) {
            if (piece.shape[y][x]) {
                ctx.fillStyle = piece.color;
                ctx.fillRect((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                ctx.strokeStyle = GRAY;
                ctx.strokeRect((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        }
    }
}

function drawNextPiece(piece) {
    // Implement drawing logic for the next piece
}

function drawHoldPiece(piece) {
    // Implement drawing logic for the hold piece
}

function drawUI(score, level, highScore) {
    ctx.fillStyle = '#fff';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 420, 50);
    ctx.fillText(`Level: ${level}`, 420, 100);
    ctx.fillText(`High Score: ${highScore}`, 420, 150);
}

const socket = new WebSocket('ws://localhost:8765');

socket.onopen = function() {
    console.log('WebSocket connection established');
};

socket.onmessage = function(event) {
    console.log('Message received from server');
    const gameState = JSON.parse(event.data);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGrid(gameState.grid);
    drawPiece(gameState.current_piece);
    drawNextPiece(gameState.next_piece);
    drawHoldPiece(gameState.hold_piece);
    drawUI(gameState.score, gameState.level, gameState.high_score);
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};

socket.onclose = function() {
    console.log('WebSocket connection closed');
};
