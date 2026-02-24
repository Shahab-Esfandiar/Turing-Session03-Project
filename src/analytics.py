import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import List, Dict, Any

class ProductAnalytics:
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)

    def calculate_nps(self, reviews: List[Dict[str, Any]]) -> float:
        if not reviews:
            return 0.0

        df = pd.DataFrame(reviews)
        total_responses = len(df)

        promoters = len(df[df['estimated_score'] >= 9])
        detractors = len(df[df['estimated_score'] <= 6])

        pct_promoters = (promoters / total_responses) * 100
        pct_detractors = (detractors / total_responses) * 100

        nps_score = pct_promoters - pct_detractors
        return round(nps_score, 2)

    def generate_report_and_charts(self, product_id: int, reviews: List[Dict[str, Any]]):
        if not reviews:
            print("❌ No data available to generate charts.")
            return

        df = pd.DataFrame(reviews)
        nps = self.calculate_nps(reviews)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # 1. Bold Title
        fig.suptitle(
            f'Data Analytics Report for Product #{product_id}\nTotal Sampled Reviews: {len(df)} | NPS: {nps}', 
            fontsize=18, 
            fontweight='bold',
            color='#2c3e50'
        )

        # Chart 1: Estimated Score Distribution
        ax1.hist(df['estimated_score'], bins=range(1, 12), align='left', color='#3498db', edgecolor='black')
        ax1.set_title('Distribution of Estimated Scores (1-10)', fontweight='bold')
        ax1.set_xlabel('Score')
        ax1.set_ylabel('Number of Reviews')
        ax1.set_xticks(range(1, 11))

        # Chart 2: Satisfaction Ratio
        satisfaction_counts = df['is_satisfied'].value_counts()
        labels = ['Satisfied', 'Dissatisfied'] if True in satisfaction_counts.index else ['Dissatisfied', 'Satisfied']
        colors = ['#2ecc71', '#e74c3c'] 
        ax2.pie(satisfaction_counts, labels=[labels[i] for i in range(len(satisfaction_counts))], 
                autopct='%1.1f%%', startangle=90, colors=colors)
        ax2.set_title('Overall Customer Satisfaction', fontweight='bold')

        # 2. Add Spacing between title and charts
        plt.tight_layout()
        plt.subplots_adjust(top=0.80)
        
        output_file = os.path.join(self.output_dir, f"analytics_product_{product_id}.png")
        plt.savefig(output_file, dpi=300)
        plt.close()