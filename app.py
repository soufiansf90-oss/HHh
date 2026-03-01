<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Elite Trader Journal</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {
    background: #0f172a;
    color: white;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}
h1 { text-align: center; }

.dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
    gap: 15px;
    margin-bottom: 20px;
}
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.green { color: #22c55e; }
.red { color: #ef4444; }

form {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}
input, select {
    padding: 8px;
    margin: 5px;
    border-radius: 5px;
    border: none;
}
button {
    padding: 8px 12px;
    background: #22c55e;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px,1fr));
    gap: 20px;
}
</style>
</head>
<body>

<h1>Elite Trader Journal</h1>

<div class="dashboard">
    <div class="card">Net Profit: <span id="netProfit">0</span></div>
    <div class="card">Win Rate: <span id="winRate">0%</span></div>
    <div class="card">Total Trades: <span id="totalTrades">0</span></div>
    <div class="card">Profit Factor: <span id="profitFactor">0</span></div>
</div>

<form id="tradeForm">
    <input type="date" id="date" required>
    <input type="text" id="pair" placeholder="Pair" required>
    <select id="type">
        <option value="Long">Long</option>
        <option value="Short">Short</option>
    </select>
    <input type="number" id="result" placeholder="Result ($)" required>
    <select id="strategy">
        <option value="SMC">SMC</option>
        <option value="ICT">ICT</option>
        <option value="Liquidity">Liquidity</option>
    </select>
    <select id="emotion">
        <option value="Calm">Calm</option>
        <option value="FOMO">FOMO</option>
        <option value="Frustrated">Frustrated</option>
    </select>
    <button type="submit">Add Trade</button>
</form>

<div class="charts">
    <canvas id="equityChart"></canvas>
    <canvas id="winLossChart"></canvas>
    <canvas id="dayChart"></canvas>
</div>

<script>
let trades = [];

const equityCtx = document.getElementById('equityChart');
const winLossCtx = document.getElementById('winLossChart');
const dayCtx = document.getElementById('dayChart');

let equityChart = new Chart(equityCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Equity Curve', data: [], borderColor: '#22c55e' }] }
});

let winLossChart = new Chart(winLossCtx, {
    type: 'pie',
    data: {
        labels: ['Wins', 'Losses'],
        datasets: [{ data: [0,0], backgroundColor: ['#22c55e','#ef4444'] }]
    }
});

let dayChart = new Chart(dayCtx, {
    type: 'bar',
    data: {
        labels: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
        datasets: [{ label: 'Performance by Day', data: [0,0,0,0,0,0,0], backgroundColor:'#3b82f6' }]
    }
});

document.getElementById('tradeForm').addEventListener('submit', function(e){
    e.preventDefault();

    const trade = {
        date: document.getElementById('date').value,
        pair: document.getElementById('pair').value,
        type: document.getElementById('type').value,
        result: parseFloat(document.getElementById('result').value),
        strategy: document.getElementById('strategy').value,
        emotion: document.getElementById('emotion').value
    };

    trades.push(trade);
    updateDashboard();
    updateCharts();
    this.reset();
});

function updateDashboard(){
    let net = trades.reduce((acc,t)=>acc+t.result,0);
    let wins = trades.filter(t=>t.result>0).length;
    let losses = trades.filter(t=>t.result<0).length;

    document.getElementById('netProfit').innerText = net.toFixed(2);
    document.getElementById('totalTrades').innerText = trades.length;
    document.getElementById('winRate').innerText =
        trades.length ? ((wins/trades.length)*100).toFixed(1)+'%' : '0%';

    let totalProfit = trades.filter(t=>t.result>0).reduce((a,t)=>a+t.result,0);
    let totalLoss = Math.abs(trades.filter(t=>t.result<0).reduce((a,t)=>a+t.result,0));
    let pf = totalLoss ? (totalProfit/totalLoss).toFixed(2) : totalProfit;

    document.getElementById('profitFactor').innerText = pf;
}

function updateCharts(){
    let cumulative = 0;
    equityChart.data.labels = [];
    equityChart.data.datasets[0].data = [];

    trades.forEach((t,i)=>{
        cumulative += t.result;
        equityChart.data.labels.push(i+1);
        equityChart.data.datasets[0].data.push(cumulative);
    });
    equityChart.update();

    let wins = trades.filter(t=>t.result>0).length;
    let losses = trades.filter(t=>t.result<0).length;
    winLossChart.data.datasets[0].data = [wins, losses];
    winLossChart.update();

    let dayPerf = [0,0,0,0,0,0,0];
    trades.forEach(t=>{
        let day = new Date(t.date).getDay();
        dayPerf[day] += t.result;
    });
    dayChart.data.datasets[0].data = dayPerf;
    dayChart.update();
}
</script>

</body>
</html>
