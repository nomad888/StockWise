# StockWise - Comprehensive Stock Analysis System
# StockWise - 综合股票分析系统

A powerful Python application that analyzes stocks based on 20 comprehensive questions covering fundamental analysis, valuation metrics, technical indicators, and market sentiment to generate actionable buy/sell recommendations.

一个强大的Python应用程序，基于20个综合问题分析股票，涵盖基本面分析、估值指标、技术指标和市场情绪，生成可操作的买入/卖出建议。

## Features | 功能特点

### 📊 Comprehensive Analysis | 全面分析
- **20 Critical Questions** covering all aspects of stock analysis
- **基于20个关键问题**，涵盖股票分析的所有方面

### 🎯 Multi-Factor Scoring | 多因子评分
- Weighted scoring system across 5 categories
- 5个类别的加权评分系统
- Automated buy/sell/hold recommendations
- 自动化买入/卖出/持有建议

### 🌐 Bilingual Support | 双语支持
- Full English and Chinese support
- 完整的中英文支持
- Questions and answers in both languages
- 问题和答案均为双语

### 📈 Real-Time Data | 实时数据
- Powered by Yahoo Finance (yfinance)
- 由Yahoo Finance提供数据支持
- Live stock prices and financial data
- 实时股价和财务数据

## The 20 Questions | 20个问题

### Fundamental Analysis | 基本面分析 (Q1-Q6)
1. What does this company do? Core products/services? | 这家公司主要是做什么的？核心产品或服务是什么？
2. Is profitability strong? Net profit and gross margin trends? | 它的盈利能力强吗？净利润和毛利率近几年变化如何？
3. Is revenue growth stable? YoY and QoQ growth? | 它的营收增长稳不稳？同比和环比增长如何？
4. How is the balance sheet? Any high leverage risk? | 资产负债情况怎么样？有没有高杠杆风险？
5. Is cash flow sufficient? Is operating cash flow positive? | 现金流是否充足？经营活动现金流为正吗？
6. Management and major shareholder background? Long-term holdings? | 管理层和大股东背景如何？他们有没有长期持股？

### Valuation Analysis | 估值分析 (Q7-Q10)
7. How do P/E and P/B ratios compare to industry average? | 这只股票的市盈率、市净率相比行业平均如何？
8. Is it historically overvalued or undervalued? | 现在是历史高估还是低估阶段？估值在历史区间哪一档？
9. How do P/S, P/CF ratios rank among peers? | 市销率、市现率等估值指标在同行中排第几？
10. Do future earnings forecasts match current price? | 未来的盈利预测和当前价格匹配吗？

### Dividend Analysis | 分红分析 (Q11)
11. Does this stock pay dividends? Is the dividend yield high? | 这只股票有没有分红？股息率高不高？

### Technical Analysis | 技术分析 (Q12-Q16)
12. What is the current price trend? Uptrend, sideways, or downtrend? | 当前股价处于什么趋势？上涨、震荡还是下跌？
13. How do key technical indicators like MACD, RSI, KDJ look? | 关键技术指标如MACD、RSI、KDJ怎么看？
14. Are there important technical patterns? | 有没有形成重要的技术形态？如双底、头肩顶？
15. Where is the current price relative to moving averages? | 当前价格处于年线、季线、均线哪个区间？
16. Are there significant volume changes? Price-volume relationship? | 近期成交量变化大吗？量价关系是否健康？

### Sentiment Analysis | 情绪分析 (Q17-Q20)
17. Are there any recent major news or announcements? | 最近有没有和这家公司相关的重大新闻或公告？
18. Are analysts bullish or bearish? Consensus target price? | 分析师是看多还是看空这家公司？一致目标价是多少？
19. Is social media/forum sentiment optimistic or pessimistic? | 社交媒体、股吧、论坛对这只股票情绪偏向乐观还是悲观？
20. Any recent unexpected events, regulatory policies, or black swans? | 近期有没有突发事件、监管政策或行业黑天鹅？

## Installation | 安装

### Prerequisites | 前置要求
- Python 3.8 or higher | Python 3.8或更高版本
- pip package manager | pip包管理器

### Setup | 设置

1. Clone or download this repository | 克隆或下载此仓库

2. Install dependencies | 安装依赖:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure API keys | (可选) 配置API密钥:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage | 使用方法

### Basic Usage | 基本用法

Analyze a stock with interactive prompt | 交互式分析股票:
```bash
python main.py
```

Analyze a specific stock | 分析特定股票:
```bash
python main.py --symbol AAPL
```

### Save Report | 保存报告

Save report with auto-generated filename | 自动生成文件名保存报告:
```bash
python main.py --symbol MSFT --save
```

Save report with custom filename | 自定义文件名保存报告:
```bash
python main.py --symbol TSLA --output tesla_analysis.txt
```

### Command-Line Options | 命令行选项

```
--symbol, -s    Stock symbol to analyze (e.g., AAPL, MSFT, TSLA)
                要分析的股票代码

--save          Save report to file with auto-generated name
                保存报告到自动生成的文件

--output, -o    Custom output filename
                自定义输出文件名
```

## Examples | 示例

### Example 1: Apple Inc.
```bash
python main.py --symbol AAPL --save
```

### Example 2: Microsoft
```bash
python main.py -s MSFT -o microsoft_report.txt
```

### Example 3: Tesla
```bash
python main.py --symbol TSLA
```

## Project Structure | 项目结构

```
StockWise/
├── main.py                      # Main entry point | 主入口
├── stock_analyzer.py            # Main analyzer orchestrator | 主分析协调器
├── report_generator.py          # Report generation | 报告生成
├── config.py                    # Configuration settings | 配置设置
├── requirements.txt             # Python dependencies | Python依赖
├── .env.example                 # Environment variables template | 环境变量模板
├── analyzers/                   # Analysis modules | 分析模块
│   ├── __init__.py
│   ├── fundamental.py          # Fundamental analysis (Q1-Q6) | 基本面分析
│   ├── valuation.py            # Valuation analysis (Q7-Q10) | 估值分析
│   ├── dividend.py             # Dividend analysis (Q11) | 分红分析
│   ├── technical.py            # Technical analysis (Q12-Q16) | 技术分析
│   └── sentiment.py            # Sentiment analysis (Q17-Q20) | 情绪分析
└── utils/                       # Utility modules | 工具模块
    ├── __init__.py
    ├── data_fetcher.py         # Data fetching with caching | 数据获取与缓存
    └── scorer.py               # Scoring and recommendation engine | 评分和建议引擎
```

## Scoring System | 评分系统

The application uses a weighted scoring system | 应用程序使用加权评分系统:

- **Fundamental Analysis | 基本面分析**: 30%
- **Valuation Analysis | 估值分析**: 25%
- **Technical Analysis | 技术分析**: 25%
- **Sentiment Analysis | 情绪分析**: 15%
- **Dividend Analysis | 分红分析**: 5%

### Recommendation Thresholds | 建议阈值

- **Strong Buy | 强烈买入**: 75-100
- **Buy | 买入**: 60-74
- **Hold | 持有**: 40-59
- **Sell | 卖出**: 25-39
- **Strong Sell | 强烈卖出**: 0-24

## Configuration | 配置

You can customize the analysis by editing `config.py`:

- Scoring weights | 评分权重
- Buy/sell thresholds | 买卖阈值
- Technical indicator parameters | 技术指标参数
- Valuation parameters | 估值参数
- Language preferences | 语言偏好

## Data Sources | 数据来源

- **Stock Data**: Yahoo Finance (via yfinance)
- **Financial Statements**: Yahoo Finance
- **News**: Yahoo Finance News
- **Analyst Ratings**: Yahoo Finance
- **Technical Indicators**: Calculated using ta library

## Limitations | 局限性

1. **Free Data**: Uses free data sources which may have delays or limitations
   使用免费数据源，可能存在延迟或限制

2. **US Stocks Focus**: Optimized for US stocks (NYSE, NASDAQ)
   针对美国股票优化（纽交所、纳斯达克）

3. **Social Sentiment**: Limited social media analysis without premium APIs
   没有高级API的社交媒体分析有限

4. **Pattern Detection**: Basic technical pattern detection
   基础的技术形态检测

## Disclaimer | 免责声明

**IMPORTANT**: This tool is for educational and informational purposes only. It does NOT constitute financial advice, investment recommendations, or an offer to buy or sell securities.

**重要提示**：此工具仅用于教育和信息目的。它不构成财务建议、投资推荐或买卖证券的要约。

- Always conduct your own research | 始终进行自己的研究
- Consult with licensed financial professionals | 咨询持牌金融专业人士
- Past performance does not guarantee future results | 过去的表现不保证未来的结果
- Investing involves risk of loss | 投资涉及损失风险

## Contributing | 贡献

Contributions are welcome! Feel free to:
- Report bugs | 报告错误
- Suggest features | 建议功能
- Submit pull requests | 提交拉取请求

## License | 许可证

This project is provided as-is for educational purposes.

## Support | 支持

For issues or questions:
1. Check the documentation | 查看文档
2. Review existing issues | 查看现有问题
3. Create a new issue with details | 创建新问题并提供详细信息

---

**Made with ❤️ for better investment decisions**
**用❤️打造，助力更好的投资决策**
