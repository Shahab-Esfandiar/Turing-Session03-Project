import sys
import time
from src.config import AVALAI_API_KEY
from src.exceptions import DigikalaAnalyzerBaseException
from src.crawler import DigikalaCrawler
from src.analyzer import CommentAnalyzer
from src.db_manager import DatabaseManager
from src.analytics import ProductAnalytics

def process_product_pipeline(product_id: int):
    """
    Main orchestration pipeline:
    1. Crawl & Sample
    2. Analyze via LLM
    3. Save to DB
    4. Generate Analytics
    """
    print(f"🚀 Starting Data Pipeline for Product ID: {product_id}\n")
    
    try:
        # Initialize components
        crawler = DigikalaCrawler()
        analyzer = CommentAnalyzer()
        db = DatabaseManager()
        analytics = ProductAnalytics()

        # Step 1: Crawl and Sample Comments
        print("[1/4] Fetching and sampling comments from Digikala API...")
        sampled_comments = crawler.fetch_comments(product_id)
        
        if not sampled_comments:
            print("⚠️ No comments found for this product. Exiting.")
            sys.exit(0)

        # Step 2 & 3: AI Analysis and Database Insertion
        print("\n[2/4] & [3/4] Processing via LLM and saving to SQLite Database...")
        total_samples = len(sampled_comments)
        
        for index, comment in enumerate(sampled_comments, start=1):
            print(f"   -> Processing comment {index}/{total_samples}...")
            try:
                # Ask AI to analyze
                ai_extracted_data = analyzer.analyze_comment(comment)
                
                # Save to Database
                db.insert_review(product_id, comment, ai_extracted_data)
                
                # Small delay to respect API rate limits
                time.sleep(0.5) 
            except Exception as e:
                print(f"   ❌ Failed to process comment {index}: {e}")
                continue 
                
        # Step 4: Analytics and Chart Generation
        print("\n[4/4] Generating Analytics and NPS Report...")
        saved_reviews = db.get_product_reviews(product_id)
        analytics.generate_report_and_charts(product_id, saved_reviews)

        print("\n✅ Pipeline completed successfully!")

    except DigikalaAnalyzerBaseException as e:
        print(f"\n❌ Pipeline Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected System Error: {e}")

if __name__ == "__main__":
    # You can change this ID to test different products
    TARGET_PRODUCT_ID = 17588414 
    process_product_pipeline(TARGET_PRODUCT_ID)