"""
Main entry point for StockWise Analysis System
"""
import sys
import argparse
from stock_analyzer import StockAnalyzer
from report_generator import ReportGenerator
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

def print_banner():
    """Print application banner"""
    banner = r"""
{Fore.CYAN}{'='*100}
   _____ _             _   _    _ _          
  / ____| |           | | | |  | (_)         
 | (___ | |_ ___   ___| | | |  | |_ ___  ___ 
  \___ \| __/ _ \ / __| | | |/\| | / __|/ _ \
  ____) | || (_) | (__| | \  /\  / \__ \  __/
 |_____/ \__\___/ \___|_|  \/  \/|_|___/\___|
                                              
        Comprehensive Stock Analysis System
        基于20个关键问题的股票分析系统
{'='*100}{Style.RESET_ALL}
"""
    # Format the banner with colors
    banner = banner.format(Fore=Fore, Style=Style)
    print(banner)

def main():
    """Main application entry point"""
    # print_banner()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Analyze stocks based on 20 comprehensive questions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbol AAPL
  python main.py --symbol MSFT --save
  python main.py --symbol TSLA --output tesla_report.txt

Questions covered:
  1-6:   Fundamental Analysis (Business, Profitability, Growth, Balance Sheet, Cash Flow, Management)
  7-10:  Valuation Analysis (P/E, P/B, Historical Valuation, Peer Comparison, Earnings Forecast)
  11:    Dividend Analysis
  12-16: Technical Analysis (Trend, Indicators, Patterns, Moving Averages, Volume)
  17-20: Sentiment Analysis (News, Analyst Ratings, Social Sentiment, Risk Events)
        """
    )
    
    parser.add_argument(
        '--symbol', '-s',
        type=str,
        help='Stock symbol to analyze (e.g., AAPL, MSFT, TSLA)'
    )
    
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save report to file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output filename for the report'
    )
    
    args = parser.parse_args()
    
    # Get stock symbol
    symbol = args.symbol
    
    if not symbol:
        print(f"\n{Fore.YELLOW}Please enter a stock symbol to analyze:{Style.RESET_ALL}")
        symbol = input("Symbol: ").strip().upper()
        
        if not symbol:
            print(f"{Fore.RED}Error: No symbol provided. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
    
    try:
        # Create analyzer
        print(f"\n{Fore.GREEN}Initializing analysis for {symbol}...{Style.RESET_ALL}")
        analyzer = StockAnalyzer(symbol)
        
        # Run analysis
        results = analyzer.run_analysis()
        
        # Generate report
        print(f"\n{Fore.GREEN}Generating report...{Style.RESET_ALL}")
        report_gen = ReportGenerator(results)
        report = report_gen.generate_report()
        
        # Display report
        print(report)
        
        # Save report if requested
        if args.save or args.output:
            filename = args.output if args.output else None
            report_gen.save_report(filename)
        else:
            print(f"\n{Fore.YELLOW}Tip: Use --save to save this report to a file{Style.RESET_ALL}")
        
        # Display quick summary
        summary = results['summary']
        print(f"\n{Fore.CYAN}{'='*100}")
        print(f"QUICK SUMMARY | 快速摘要")
        print(f"{'='*100}{Style.RESET_ALL}")
        print(f"Overall Score: {summary['overall_score']}/100")
        print(f"Recommendation: {summary['recommendation_en']} | {summary['recommendation_zh']}")
        print(f"Confidence: {summary['confidence']}")
        print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"\n{Fore.RED}Error during analysis: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please check that the symbol is valid and try again.{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
