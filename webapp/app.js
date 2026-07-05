// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let currentAnalysis = null;
let currentTab = 'all';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    addSVGGradient();
});

function setupEventListeners() {
    // Search button
    document.getElementById('analyzeBtn').addEventListener('click', handleAnalyze);

    // Enter key on input
    document.getElementById('stockInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAnalyze();
    });

    // Popular stock chips
    document.querySelectorAll('.stock-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.getElementById('stockInput').value = chip.dataset.symbol;
            handleAnalyze();
        });
    });

    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentTab = tab.dataset.tab;
            filterQuestions();
        });
    });
}

function addSVGGradient() {
    const svg = document.querySelector('.score-ring');
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
    gradient.setAttribute('id', 'scoreGradient');
    gradient.setAttribute('x1', '0%');
    gradient.setAttribute('y1', '0%');
    gradient.setAttribute('x2', '100%');
    gradient.setAttribute('y2', '100%');

    const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop1.setAttribute('offset', '0%');
    stop1.setAttribute('stop-color', '#667eea');

    const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop2.setAttribute('offset', '100%');
    stop2.setAttribute('stop-color', '#764ba2');

    gradient.appendChild(stop1);
    gradient.appendChild(stop2);
    defs.appendChild(gradient);
    svg.insertBefore(defs, svg.firstChild);
}

async function handleAnalyze() {
    const input = document.getElementById('stockInput');
    const symbol = input.value.trim().toUpperCase();

    if (!symbol) {
        showError('Please enter a stock symbol');
        return;
    }

    // Show loading state
    setLoadingState(true);
    closeError();

    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
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
        currentAnalysis = data;
        displayResults(data);

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (error) {
        showError(error.message);
        console.error('Analysis error:', error);
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(loading) {
    const btn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    btn.disabled = loading;
    btnText.style.display = loading ? 'none' : 'inline';
    btnLoader.style.display = loading ? 'inline-block' : 'none';
}

function displayResults(data) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';

    // Update company info
    document.getElementById('companyName').textContent = data.company_name;
    document.getElementById('stockSymbol').textContent = data.symbol;
    document.getElementById('analysisTime').textContent = data.timestamp;

    // Update overall score
    const score = Math.round(data.summary.overall_score);
    document.getElementById('overallScore').textContent = score;

    // Animate score ring
    animateScoreRing(score);

    // Update recommendation
    updateRecommendation(data.summary);

    // Update category scores
    updateCategoryScores(data.summary.category_scores);

    // Display questions
    displayQuestions(data.results);
}

function animateScoreRing(score) {
    const circle = document.getElementById('scoreRingProgress');
    const circumference = 534; // 2 * PI * 85
    const offset = circumference - (score / 100) * circumference;

    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 100);
}

function updateRecommendation(summary) {
    const badge = document.getElementById('recommendationBadge');
    const recEn = document.getElementById('recEn');
    const recZh = document.getElementById('recZh');
    const confidence = document.getElementById('confidence');

    // Remove all rec classes
    badge.className = 'rec-badge';

    // Add appropriate class
    const recClass = summary.recommendation_en.toLowerCase().replace(' ', '-');
    badge.classList.add(recClass);

    // Update text
    badge.textContent = summary.recommendation_en.toUpperCase();
    recEn.textContent = summary.recommendation_en;
    recZh.textContent = summary.recommendation_zh;
    confidence.textContent = `${summary.confidence} Confidence`;
}

function updateCategoryScores(scores) {
    const categories = ['fundamental', 'valuation', 'technical', 'sentiment', 'dividend'];

    categories.forEach(category => {
        const score = Math.round(scores[category]);
        document.getElementById(`${category}Score`).textContent = score;

        // Animate bar
        setTimeout(() => {
            document.getElementById(`${category}Bar`).style.width = `${score}%`;
        }, 100);
    });
}

function displayQuestions(results) {
    const container = document.getElementById('questionsList');
    container.innerHTML = '';

    results.forEach((item, index) => {
        const card = createQuestionCard(item, index + 1);
        container.appendChild(card);
    });

    filterQuestions();
}

function createQuestionCard(item, number) {
    const card = document.createElement('div');
    card.className = 'question-card';
    card.dataset.category = getCategoryFromNumber(number);

    const header = document.createElement('div');
    header.className = 'question-header';

    const questionEn = document.createElement('div');
    questionEn.className = 'question-en';
    questionEn.innerHTML = `<span class="question-number">Q${number}.</span>${item.question_en}`;

    const questionZh = document.createElement('div');
    questionZh.className = 'question-zh';
    questionZh.textContent = item.question_zh;

    header.appendChild(questionEn);
    header.appendChild(questionZh);

    if (item.score !== null) {
        const scoreBadge = document.createElement('span');
        scoreBadge.className = 'question-score-badge';
        scoreBadge.textContent = `${Math.round(item.score)}/100`;
        header.appendChild(scoreBadge);
    }

    const answerSection = document.createElement('div');
    answerSection.className = 'answer-section';

    for (const [key, value] of Object.entries(item.answer)) {
        const answerItem = createAnswerItem(key, value);
        answerSection.appendChild(answerItem);
    }

    card.appendChild(header);
    card.appendChild(answerSection);

    return card;
}

function createAnswerItem(key, value) {
    const item = document.createElement('div');
    item.className = 'answer-item';

    const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

    if (Array.isArray(value)) {
        item.innerHTML = `<span class="answer-key">${formattedKey}:</span>`;
        const list = document.createElement('ul');
        list.style.marginLeft = '1.5rem';
        list.style.marginTop = '0.5rem';
        value.forEach(v => {
            const li = document.createElement('li');
            li.textContent = v;
            list.appendChild(li);
        });
        item.appendChild(list);
    } else {
        item.innerHTML = `<span class="answer-key">${formattedKey}:</span> ${value}`;
    }

    return item;
}

function getCategoryFromNumber(number) {
    if (number <= 6) return 'fundamental';
    if (number <= 10) return 'valuation';
    if (number === 11) return 'dividend';
    if (number <= 16) return 'technical';
    return 'sentiment';
}

function filterQuestions() {
    const cards = document.querySelectorAll('.question-card');

    cards.forEach(card => {
        if (currentTab === 'all' || card.dataset.category === currentTab) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function showError(message) {
    const container = document.getElementById('errorContainer');
    const messageEl = document.getElementById('errorMessage');

    messageEl.textContent = message;
    container.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        closeError();
    }, 5000);
}

function closeError() {
    document.getElementById('errorContainer').style.display = 'none';
}

function resetSearch() {
    document.getElementById('stockInput').value = '';
    document.getElementById('resultsSection').style.display = 'none';
    currentAnalysis = null;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Smooth scroll for nav links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = link.getAttribute('href');
        if (target.startsWith('#')) {
            const element = document.querySelector(target);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});
