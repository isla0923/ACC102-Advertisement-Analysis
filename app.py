import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import arff

st.set_page_config(page_title="Ad Click-Through Rate Analysis", layout="wide")
st.title("What Makes an Ad Attractive?")
st.markdown("### Interactive Dashboard for Advertising Agencies")

@st.cache_data
def load_data():
    data, _ = arff.loadarff('dataset.arff')
    df = pd.DataFrame(data)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.decode('utf-8')
    df['click'] = df['click'].astype(int)
    return df

df = load_data()

# Calculate metrics
overall_click_through_rate = df['click'].mean() * 100
position_click_through_rate = df.groupby('position')['click'].mean() * 100
depth_click_through_rate = df.groupby('depth')['click'].mean() * 100
cross_click_through_rate = df.groupby(['position', 'depth'])['click'].mean().unstack() * 100
impression_counts = df['impression'].value_counts().sort_index()

st.sidebar.title("Menu")
page = st.sidebar.radio("Select", 
                        ["Overview", "Position Analysis", "Depth Analysis", 
                         "Heatmap", "Impression Distribution", "Predictor & Budget Calculator"])

# ========== Overview ==========
if page == "Overview":
    st.header("Overall Click-Through Rate")
    fig, ax = plt.subplots()
    click_count = df['click'].sum()
    no_click = len(df) - click_count
    ax.pie([click_count, no_click], labels=['Clicked', 'Not Clicked'], 
           autopct='%1.1f%%', colors=['green', 'red'])
    ax.set_title(f'Overall Click-Through Rate: {overall_click_through_rate:.1f}%')
    st.pyplot(fig)

# ========== Position Analysis ==========
elif page == "Position Analysis":
    st.header("Click-Through Rate by Ad Position")
    fig, ax = plt.subplots()
    bars = ax.bar(position_click_through_rate.index.astype(str), position_click_through_rate.values, 
                  color=['blue', 'orange', 'red'])
    ax.set_xlabel('Ad Position')
    ax.set_ylabel('Click-Through Rate (%)')
    ax.set_title('Click-Through Rate by Ad Position')
    for bar, val in zip(bars, position_click_through_rate.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{val:.1f}%', ha='center')
    st.pyplot(fig)
    st.info(f"Position 1 is {position_click_through_rate[1]/position_click_through_rate[3]:.1f}x better than Position 3")

# ========== Depth Analysis ==========
elif page == "Depth Analysis":
    st.header("Click-Through Rate by Ad Depth")
    fig, ax = plt.subplots()
    bars = ax.bar(depth_click_through_rate.index.astype(str), depth_click_through_rate.values, 
                  color=['green', 'orange', 'purple'])
    ax.set_xlabel('Number of Ads on Page (Depth)')
    ax.set_ylabel('Click-Through Rate (%)')
    ax.set_title('Click-Through Rate by Ad Depth')
    for bar, val in zip(bars, depth_click_through_rate.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{val:.1f}%', ha='center')
    st.pyplot(fig)
    st.info(f"Depth 1 is {depth_click_through_rate[1]/depth_click_through_rate[3]:.1f}x better than Depth 3")

# ========== Heatmap ==========
elif page == "Heatmap":
    st.header("Position × Depth Heatmap")
    cross_filtered = cross_click_through_rate.dropna(how='all').dropna(axis=1, how='all')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cross_filtered, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax)
    ax.set_xlabel('Ad Depth')
    ax.set_ylabel('Ad Position')
    ax.set_title('Click-Through Rate Heatmap (%)')
    st.pyplot(fig)
    best_val = cross_filtered.max().max()
    best_pos, best_depth = cross_filtered.stack().idxmax()
    st.success(f"Best combination: Position {best_pos} + Depth {best_depth} = {best_val:.1f}%")

# ========== Impression Distribution ==========
elif page == "Impression Distribution":
    st.header("Ad Impression Distribution")
    imp_filtered = impression_counts[impression_counts.index <= 20]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(imp_filtered.index.astype(str), imp_filtered.values, color='steelblue')
    ax.set_xlabel('Number of Impressions')
    ax.set_ylabel('Number of Ads')
    ax.set_title('85% of ads are shown only once')
    st.pyplot(fig)
    st.info(f"Ads shown once: {impression_counts[1]:,} ({impression_counts[1]/len(df)*100:.1f}%)")

# ========== Predictor & Budget Calculator ==========
elif page == "Predictor & Budget Calculator":
    st.header("Click-Through Rate Predictor & Budget Calculator")
    st.markdown("### Find the best ad placement and calculate your return")
    
    col1, col2 = st.columns(2)
    
    with col1:
        position = st.selectbox("Select Ad Position", [1, 2, 3], 
                                help="Position 1 = top of page, Position 3 = bottom")
    with col2:
        depth = st.selectbox("Select Ad Depth", [1, 2, 3],
                             help="Depth 1 = only your ad, Depth 3 = 3 ads on page")
    
    # Get predicted click-through rate
    if position in cross_click_through_rate.index and depth in cross_click_through_rate.columns:
        predicted_rate = cross_click_through_rate.loc[position, depth]
        if not pd.isna(predicted_rate):
            # Display predicted click-through rate
            st.markdown("---")
            st.subheader("Predicted Click-Through Rate")
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Ad Position", position)
            col_b.metric("Ad Depth", depth)
            col_c.metric("Predicted Click-Through Rate", f"{predicted_rate:.1f}%", 
                         delta=f"{predicted_rate - overall_click_through_rate:.1f}% vs average")
            
            # Show gauge chart
            fig, ax = plt.subplots(figsize=(8, 2))
            ax.barh([0], [predicted_rate], color='green' if predicted_rate > overall_click_through_rate else 'red', height=0.5)
            ax.axvline(x=overall_click_through_rate, color='blue', linestyle='--', linewidth=2, 
                       label=f'Average: {overall_click_through_rate:.1f}%')
            ax.set_xlim(0, max(30, predicted_rate + 5))
            ax.set_yticks([])
            ax.set_xlabel('Click-Through Rate (%)')
            ax.legend()
            ax.set_title('Your Predicted Rate vs Average')
            st.pyplot(fig)
            
            # ========== BUDGET CALCULATOR ==========
            st.markdown("---")
            st.subheader("Budget Calculator")
            st.markdown("Calculate how many clicks you can get with your budget")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                budget = st.number_input("Your Budget (US Dollars)", min_value=100, max_value=100000, value=1000, step=100)
            with col_d2:
                cost_per_click = st.number_input("Cost Per Click (US Dollars)", min_value=0.1, max_value=10.0, value=0.5, step=0.1)
            
            # Calculate estimated clicks
            click_through_rate_decimal = predicted_rate / 100
            estimated_clicks = int(budget / cost_per_click * click_through_rate_decimal)
            
            st.markdown("---")
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("Your Budget", f"${budget:,.0f}")
            col_r2.metric("Cost Per Click", f"${cost_per_click:.2f}")
            col_r3.metric("Estimated Clicks", f"{estimated_clicks:,}")
            
            # Show comparison with average
            avg_estimated_clicks = int(budget / cost_per_click * (overall_click_through_rate / 100))
            if estimated_clicks > avg_estimated_clicks:
                st.success(f"Your selected placement will get {estimated_clicks - avg_estimated_clicks:,} more clicks than average!")
                st.info(f"That is {(estimated_clicks/avg_estimated_clicks - 1)*100:.0f}% more clicks for the same budget")
            else:
                st.warning(f"This placement is below average. Try Position 1 or Depth 1 for better results")
            
            # Recommendation based on position and depth
            st.markdown("---")
            st.subheader("Recommendation")
            if position == 1 and depth == 2:
                st.success("Excellent! This is the best possible combination!")
            elif position == 1 and depth == 1:
                st.success("Great choice! Consider trying Depth 2 for even higher click-through rate")
            elif position == 3 or depth == 3:
                st.warning("This combination has low click-through rate. Recommendations:")
                if position == 3:
                    st.write("- Move your ad to Position 1 (3 times higher click-through rate)")
                if depth == 3:
                    st.write("- Choose a page with fewer ads (Depth 1 or Depth 2)")
            else:
                st.info("💡 Try Position 1 + Depth 2 for the best results (24.0% click-through rate)")
            
            # Best combination reminder
            best_val = cross_click_through_rate.max().max()
            best_pos, best_depth = cross_click_through_rate.stack().idxmax()
            if predicted_rate < best_val:
                st.caption(f"Tip: The best combination is Position {best_pos} + Depth {best_depth} with {best_val:.1f}% click-through rate")
        else:
            st.warning("No data available for this combination. Try Position 1 or 2 with Depth 1, 2, or 3.")
    else:
        st.warning("Please select a valid combination")