# What Makes an Advertisement Attractive?
## An Interactive Click-Through Rate Analysis Dashboard

## 1. Problem and User

Advertising agencies spend millions on online advertisements without knowing which placement works best. This dashboard helps advertisement optimizers and marketing professionals answer: Which advertisement position gets the most clicks? How many advertisements on a page is optimal? How many clicks can I get with my budget?

## 2. Data

**Source:** OpenML dataset identification number 1220 (Click_prediction_small)

**Original Source:** Knowledge Discovery and Data mining Cup 2012 / Tencent Incorporated

**Access Date:** April 2026

**Key Fields:**
- `click` - Whether the user clicked the advertisement (0 means no, 1 means yes)
- `position` - Advertisement position on the page (1, 2, or 3)
- `depth` - Number of advertisements on the same page (1, 2, or 3)
- `impression` - How many times the advertisement was shown

## 3. Methods

The analysis follows this workflow:

1. Load the ARFF file using the scipy dot io dot arff module
2. Clean the data by converting byte columns to strings and converting the click column to integer
3. Calculate click-through rates by advertisement position and by advertisement depth
4. Create visualizations including a pie chart, bar charts, a heatmap, and a histogram
5. Build an interactive Streamlit dashboard with a predictor and a budget calculator

## 4. Key Findings

- Position 1 has a 20.4 percent click-through rate, which is 3 times higher than Position 3 at 6.9 percent
- Depth 1 has a 17.8 percent click-through rate, which is 1.5 times higher than Depth 3 at 11.9 percent
- The best combination is Position 1 plus Depth 2, which achieves a 24.0 percent click-through rate
- 85 percent of advertisements are shown only once, meaning advertisers have only one chance to attract users

## 5. How to Run

Open your terminal and run the following commands:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open your browser at `http://localhost:8501`
6. Product Link and Demo

Product Link: After running the application, access it at http://localhost:8501

GitHub Repository: [Insert your GitHub repository link here]

Demo Video: [Insert your 1 to 3 minute demo video link here] 
7. Limitations and Next Steps

Limitations:

The dataset is from 2012 and may not reflect current advertising trends
The data comes from a search engine in India, so results may vary in different markets
Several fields such as advertiser identification, title identification, and user identification contained no usable data and were excluded
The analysis only considers position, depth, and impression frequency. Advertisement creative quality, targeting, and timing are not included
Next Steps:

Add real-time data from advertising platforms like Google Ads or Facebook Ads
Include advertisement creative analysis such as images and text length
Build a multi-platform comparison tool
