// API base URL
const API_BASE = window.location.origin;

// Handle Enter key in input
document.getElementById('symbolInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        analyzeStock();
    }
});

async function analyzeStock() {
    const symbolInput = document.getElementById('symbolInput');
    const symbol = symbolInput.value.trim().toUpperCase();

    if (!symbol) {
        showError('Please enter a stock symbol');
        return;
    }

    // Hide previous results and errors
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';

    // Show loading state
    const btn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';

    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol: symbol })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function displayResults(data) {
    // Update company info
    document.getElementById('companyName').textContent = data.company_name;
    document.getElementById('symbolDisplay').textContent = `Symbol: ${data.symbol} | ${data.timestamp}`;

    // Update overall score
    const score = Math.round(data.summary.overall_score);
    document.getElementById('overallScore').textContent = score;

    // Update recommendation
    const recBadge = document.getElementById('recBadge');
    const recClass = data.summary.recommendation_en.toLowerCase().replace(' ', '-');
    recBadge.className = `rec-badge ${recClass}`;
    recBadge.textContent = data.summary.recommendation_en.toUpperCase();

    document.getElementById('recEn').textContent = data.summary.recommendation_en;
    document.getElementById('recZh').textContent = data.summary.recommendation_zh;
    document.getElementById('confidence').textContent = `${data.summary.confidence} Confidence`;

    // Update category scores
    updateCategoryScore('fundamental', data.summary.category_scores.fundamental);
    updateCategoryScore('valuation', data.summary.category_scores.valuation);
    updateCategoryScore('technical', data.summary.category_scores.technical);
    updateCategoryScore('sentiment', data.summary.category_scores.sentiment);
    updateCategoryScore('dividend', data.summary.category_scores.dividend);

    // Display detailed questions
    displayQuestions(data.results);

    // Show results
    document.getElementById('results').style.display = 'block';

    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function updateCategoryScore(category, score) {
    const roundedScore = Math.round(score);
    document.getElementById(`${category}Score`).textContent = roundedScore;
    document.getElementById(`${category}Bar`).style.width = `${roundedScore}%`;
}

function displayQuestions(results) {
    const container = document.getElementById('questionsList');
    container.innerHTML = '';

    results.forEach((item, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-item';

        let html = `
            <div class="question-header">
                <div class="question-en">Q${index + 1}. ${item.question_en}</div>
                <div class="question-zh">${item.question_zh}</div>
                ${item.score !== null ? `<span class="question-score">${Math.round(item.score)}/100</span>` : ''}
            </div>
            <div class="answer-details">
        `;

        // Display answer details
        for (const [key, value] of Object.entries(item.answer)) {
            const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

            if (Array.isArray(value)) {
                html += `<div class="answer-item"><span class="answer-key">${formattedKey}:</span></div>`;
                value.forEach(v => {
                    html += `<div class="answer-item" style="padding-left: 20px;">• ${v}</div>`;
                });
            } else {
                html += `<div class="answer-item"><span class="answer-key">${formattedKey}:</span> ${value}</div>`;
            }
        }

        html += '</div>';
        questionDiv.innerHTML = html;
        container.appendChild(questionDiv);
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = `❌ Error: ${message}`;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}
