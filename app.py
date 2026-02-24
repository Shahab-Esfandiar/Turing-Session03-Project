import streamlit as st
import re
import time
import logging
import requests
import os

from src.config import AVALAI_API_KEY
from src.crawler import DigikalaCrawler
from src.analyzer import CommentAnalyzer
from src.db_manager import DatabaseManager
from src.analytics import ProductAnalytics

# UI Configuration & Styling
st.set_page_config(page_title="Digikala AI Sentiment Analyzer", layout="wide", page_icon="🛍️")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        direction: ltr;
    }
    h1, h2, h3 {
        font-weight: 800 !important;
        color: #e53935;
    }
    .stButton>button {
        font-weight: bold;
        border-radius: 8px;
        background-color: #e53935;
        color: white;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #b71c1c;
        color: white;
    }
    /* Terminal Box Styling */
    .terminal-box {
        background-color: #1e1e1e;
        color: #4af626; /* gray */
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 13px;
        height: 380px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px #000000;
        line-height: 1.6;
        margin-top: 15px;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

logging.basicConfig(filename='app_execution.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Helper Functions
def extract_product_id(url: str) -> int:
    match = re.search(r'dkp-(\d+)', url)
    return int(match.group(1)) if match else None

def fetch_product_title(product_id: int) -> str:
    try:
        url = f"https://api.digikala.com/v1/product/{product_id}/"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("data", {}).get("product", {}).get("title_fa", "Unknown Product")
    except:
        pass
    return f"Product #{product_id}"

# Main Application
def main():
    st.title("🛍️ Digikala AI Sentiment Analyzer")
    st.markdown("Automated pipeline for extracting reviews, AI sentiment analysis, and NPS calculation.")
    st.divider()

    # Create Two Columns: Left (40% width) and Right (60% width)
    col_left, col_right = st.columns([4, 6], gap="large")

    # ---------------- LEFT COLUMN: CONTROLS & LOGS ----------------
    with col_left:
        st.subheader("⚙️ Control Panel")
        product_url = st.text_input("🔗 Digikala Product Link:", placeholder="https://www.digikala.com/product/dkp-123456/...")
        start_btn = st.button("🚀 Start Processing & Analysis")
        
        # Placeholders for progress bar and terminal
        progress_bar_placeholder = st.empty()
        terminal_placeholder = st.empty()
        
        # Render empty terminal initially
        terminal_placeholder.markdown("<div class='terminal-box'>Waiting for system initiation...</div>", unsafe_allow_html=True)

    # ---------------- RIGHT COLUMN: OUTPUTS ----------------
    with col_right:
        st.subheader("📊 Analytics Dashboard")
        output_placeholder = st.empty()
        output_placeholder.info("👈 Enter a URL and click Start to view results here.")

    # ---------------- EXECUTION LOGIC ----------------
    if start_btn:
        if not product_url:
            with col_left:
                st.warning("⚠️ Please enter a product link.")
            return

        product_id = extract_product_id(product_url)
        if not product_id:
            with col_left:
                st.error("❌ Invalid URL. Missing 'dkp-' identifier.")
            return

        # Initialize tracking variables
        terminal_logs = []
        def update_terminal(msg):
            logging.info(msg)
            terminal_logs.append(f"> {msg}")
            # Keep only the last 20 lines to prevent extreme scrolling
            display_logs = terminal_logs[-20:]
            html_content = f"<div class='terminal-box'>{'<br>'.join(display_logs)}</div>"
            terminal_placeholder.markdown(html_content, unsafe_allow_html=True)

        # Clear right column placeholder
        output_placeholder.empty()

        try:
            crawler = DigikalaCrawler()
            analyzer = CommentAnalyzer()
            db = DatabaseManager()
            analytics = ProductAnalytics()

            # Step 1: Info
            update_terminal(f"Extracting metadata for Product ID: {product_id}")
            product_title = fetch_product_title(product_id)
            update_terminal(f"Product Name: {product_title}")
            
            # Step 2: Crawling
            update_terminal("Connecting to Digikala API...")
            sampled_comments = crawler.fetch_comments(product_id)
            total_comments = len(sampled_comments)
            
            if total_comments == 0:
                update_terminal("⚠️ ERROR: No reviews found.")
                return

            update_terminal(f"Sampled {total_comments} reviews. Starting AI pipeline...")
            
            # Step 3: AI Processing Loop
            progress_bar = progress_bar_placeholder.progress(0)
            
            for index, comment in enumerate(sampled_comments):
                progress_percent = int(((index + 1) / total_comments) * 100)
                progress_bar.progress(progress_percent)
                update_terminal(f"Analyzing review [{index + 1}/{total_comments}] via LLM...")
                
                try:
                    ai_extracted_data = analyzer.analyze_comment(comment)
                    db.insert_review(product_id, comment, ai_extracted_data)
                    time.sleep(0.3)
                except Exception as e:
                    update_terminal(f"❌ Error on review {index+1}: {str(e)[:50]}")
                    continue

            # Step 4: Analytics
            update_terminal("AI Processing complete. Generating charts...")
            saved_reviews = db.get_product_reviews(product_id)
            analytics.generate_report_and_charts(product_id, saved_reviews)
            nps_score = analytics.calculate_nps(saved_reviews)
            satisfaction_ratio = sum(1 for r in saved_reviews if r['is_satisfied'])
            
            update_terminal("✅ Pipeline execution finished successfully!")

            # ---------------- DISPLAY RESULTS IN RIGHT COLUMN ----------------
            with col_right:
                st.success(f"**Product:** {product_title}")
                
                # Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("📊 NPS Score", f"{nps_score}")
                m2.metric("📝 Analyzed Reviews", total_comments)
                m3.metric("😊 Satisfied Users", satisfaction_ratio)

                # Chart
                chart_path = f"outputs/analytics_product_{product_id}.png"
                if os.path.exists(chart_path):
                    st.image(chart_path, use_container_width=True)
                    
                    with open(chart_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Analytics Chart",
                            data=file,
                            file_name=f"Analytics_Report_{product_id}.png",
                            mime="image/png",
                            use_container_width=True
                        )

        except Exception as e:
            update_terminal(f"❌ SYSTEM CRASH: {e}")

if __name__ == "__main__":
    main()