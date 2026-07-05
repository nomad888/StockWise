# StockWise Pro - Standalone Web Application

A modern, standalone web application that consumes the StockWise API to provide comprehensive stock analysis.

## Features

- 🎨 **Modern UI/UX** - Beautiful gradient design with smooth animations
- 📊 **Real-time Analysis** - Fetches live stock data via StockWise API
- 🌐 **Bilingual Support** - Full English and Chinese support
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- ⚡ **Fast & Interactive** - Smooth animations and instant feedback
- 🎯 **20 Questions** - Comprehensive analysis across 5 categories

## Prerequisites

The StockWise API must be running on `http://localhost:8000`

To start the API:
```bash
cd /Users/xiangshi/Workspace/StockWise
source venv/bin/activate
uvicorn api:app --reload
```

## Usage

### Option 1: Open Directly in Browser

Simply open `index.html` in your web browser:
```bash
open index.html
```

### Option 2: Serve with Python HTTP Server

```bash
cd webapp
python3 -m http.server 8080
```

Then visit: http://localhost:8080

### Option 3: Serve with Node.js

```bash
cd webapp
npx serve
```

## How to Use

1. **Enter Stock Symbol**: Type a stock symbol (e.g., AAPL, MSFT, GOOGL)
2. **Click Analyze**: Or press Enter to start analysis
3. **View Results**: See comprehensive analysis with:
   - Overall score and recommendation
   - Category breakdown (Fundamental, Valuation, Technical, Sentiment, Dividend)
   - Detailed answers to all 20 questions
4. **Filter Questions**: Use tabs to filter by category
5. **New Search**: Click "New Search" to analyze another stock

## Quick Stocks

Click on any of the popular stock chips to quickly analyze:
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc.
- **TSLA** - Tesla Inc.
- **NVDA** - NVIDIA Corporation

## Project Structure

```
webapp/
├── index.html      # Main HTML structure
├── styles.css      # Comprehensive styling
├── app.js          # API integration and interactivity
└── README.md       # This file
```

## API Integration

The app calls the following StockWise API endpoints:

### POST /api/analyze
```javascript
fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ symbol: 'AAPL' })
})
```

### Response Format
```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "timestamp": "2026-01-21 11:00:00",
  "summary": {
    "overall_score": 54.24,
    "recommendation_en": "Hold",
    "recommendation_zh": "持有",
    "confidence": "Medium",
    "category_scores": { ... }
  },
  "results": [ ... ]
}
```

## Features Breakdown

### Hero Section
- Animated gradient background
- Stock symbol input with autocomplete
- Popular stock quick access chips
- Responsive design

### Results Dashboard
- Animated score ring (SVG)
- Color-coded recommendation badge
- Category score cards with progress bars
- Smooth animations and transitions

### Detailed Analysis
- Tabbed interface for filtering questions
- All 20 questions with bilingual display
- Individual question scores
- Structured answer display

### Error Handling
- User-friendly error messages
- Auto-dismiss notifications
- Network error handling
- Invalid symbol detection

## Customization

### Change API URL
Edit `app.js`:
```javascript
const API_BASE_URL = 'http://your-api-url:8000';
```

### Modify Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    /* ... */
}
```

### Add More Stocks
Edit `index.html` to add more popular stock chips:
```html
<button class="stock-chip" data-symbol="AMZN">AMZN</button>
```

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance

- Lightweight (< 100KB total)
- No external dependencies
- Fast load times
- Smooth 60fps animations

## Troubleshooting

### API Connection Error
- Ensure StockWise API is running on port 8000
- Check CORS is enabled in the API
- Verify network connectivity

### Styles Not Loading
- Make sure all files are in the same directory
- Check file paths are correct
- Clear browser cache

### Animations Not Working
- Ensure JavaScript is enabled
- Check browser console for errors
- Try a different browser

## License

Part of the StockWise project.

## Credits

- Design: Modern gradient UI with glassmorphism
- Fonts: Inter from Google Fonts
- Icons: Unicode emoji
- Data: Yahoo Finance via StockWise API
