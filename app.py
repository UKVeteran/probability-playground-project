import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Probability Playground",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for clean typography and cards
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎲 Probability Playground")
st.sidebar.markdown("Explore randomness, convergence, and statistical reasoning.")
app_mode = st.sidebar.selectbox(
    "Choose a Module",
    [
        "1. Coin Tosses & Law of Large Numbers",
        "2. Dice Rolls (Single & Two Dice)",
        "3. Card Draws & Combinatorics",
        "4. Sampling Variability & CLT",
        "5. Interactive Quiz",
        "6. Teacher Resources & Worksheets"
    ]
)

# ==========================================
# MODULE 1: COIN TOSSES
# ==========================================
if app_mode == "1. Coin Tosses & Law of Large Numbers":
    st.markdown('<p class="main-header">Coin Toss Simulation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Observe how experimental probability converges to theoretical probability (0.50) as the number of trials increases.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Controls")
        n_flips = st.slider("Number of Tosses ($N$)", min_value=10, max_value=5000, value=500, step=10)
        bias = st.slider("Probability of Heads ($P(H)$)", min_value=0.1, max_value=0.9, value=0.5, step=0.05)
        run_sim = st.button("Run Simulation", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.markdown("**Key Mathematical Concept:**")
        st.info("The **Law of Large Numbers** states that as a sample size grows, its mean gets closer to the expected value of the whole population.")

    with col2:
        if run_sim or True:
            np.random.seed(42)
            outcomes = np.random.choice([1, 0], size=n_flips, p=[bias, 1-bias])
            cumulative_heads = np.cumsum(outcomes)
            trials = np.arange(1, n_flips + 1)
            cumulative_prob = cumulative_heads / trials
            
            df = pd.DataFrame({
                "Trial": trials,
                "Cumulative Probability": cumulative_prob,
                "Outcome": outcomes
            })
            
            fig = px.line(
                df, x="Trial", y="Cumulative Probability",
                title=f"Convergence of Coin Tosses (True P = {bias})",
                labels={"Cumulative Probability": "Experimental P(Heads)"}
            )
            fig.add_hline(y=bias, line_dash="dash", line_color="red", annotation_text=f"Theoretical P = {bias}")
            fig.update_layout(yaxis=dict(range=[0, 1]))
            st.plotly_chart(fig, use_container_width=True)
            
            total_heads = int(np.sum(outcomes))
            total_tails = n_flips - total_heads
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Tosses", n_flips)
            m2.metric("Heads Count", total_heads, f"{total_heads/n_flips*100:.1f}%")
            m3.metric("Tails Count", total_tails, f"{total_tails/n_flips*100:.1f}%")

# ==========================================
# MODULE 2: DICE ROLLS
# ==========================================
elif app_mode == "2. Dice Rolls (Single & Two Dice)":
    st.markdown('<p class="main-header">Dice Roll Experiments</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compare empirical frequencies with theoretical probability distributions for 1 or 2 six-sided dice.</p>', unsafe_allow_html=True)
    
    dice_mode = st.radio("Select Experiment:", ["Single Die (1d6)", "Two Dice Sum (2d6)"], horizontal=True)
    n_rolls = st.slider("Number of Rolls", min_value=100, max_value=10000, value=1000, step=100)
    
    if dice_mode == "Single Die (1d6)":
        rolls = np.random.randint(1, 7, size=n_rolls)
        counts = pd.Series(rolls).value_counts().sort_index()
        
        df_dice = pd.DataFrame({
            "Outcome": range(1, 7),
            "Experimental Frequency": [counts.get(i, 0) / n_rolls for i in range(1, 7)],
            "Theoretical Probability": [1/6]*6
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_dice["Outcome"], y=df_dice["Experimental Frequency"], name="Experimental", marker_color="#3B82F6"))
        fig.add_trace(go.Scatter(x=df_dice["Outcome"], y=df_dice["Theoretical Probability"], mode="lines+markers", name="Theoretical (1/6)", line=dict(color="red", width=3)))
        fig.update_layout(title="Single Die Roll Distribution", xaxis_title="Outcome", yaxis_title="Relative Frequency")
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        die1 = np.random.randint(1, 7, size=n_rolls)
        die2 = np.random.randint(1, 7, size=n_rolls)
        sums = die1 + die2
        
        counts = pd.Series(sums).value_counts().sort_index()
        
        # Theoretical distribution for 2d6 sums (2 to 12)
        theo_counts = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}
        
        df_2d6 = pd.DataFrame({
            "Sum": list(range(2, 13)),
            "Experimental": [counts.get(s, 0) / n_rolls for s in range(2, 13)],
            "Theoretical": [theo_counts[s]/36 for s in range(2, 13)]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_2d6["Sum"], y=df_2d6["Experimental"], name="Experimental", marker_color="#10B981"))
        fig.add_trace(go.Scatter(x=df_2d6["Sum"], y=df_2d6["Theoretical"], mode="lines+markers", name="Theoretical", line=dict(color="red", width=3)))
        fig.update_layout(title="Sum of Two Dice (2d6) Distribution", xaxis_title="Sum", yaxis_title="Relative Frequency")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MODULE 3: CARD DRAWS
# ==========================================
elif app_mode == "3. Card Draws & Combinatorics":
    st.markdown('<p class="main-header">Card Draws & Deck Sampling</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore conditional probability, suits, face cards, and sampling with/without replacement.</p>', unsafe_allow_html=True)
    
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(v, s) for s in suits for v in values]
    
    n_draws = st.slider("Number of Simulation Iterations", min_value=100, max_value=5000, value=1000, step=100)
    target_type = st.selectbox("Target Condition", ["Drawing a Heart", "Drawing a Face Card (Jack, Queen, King)", "Drawing an Ace"])
    
    matches = 0
    for _ in range(n_draws):
        card = deck[np.random.choice(len(deck))]
        if target_type == "Drawing a Heart" and card[1] == 'Hearts':
            matches += 1
        elif target_type == "Drawing a Face Card (Jack, Queen, King)" and card[0] in ['Jack', 'Queen', 'King']:
            matches += 1
        elif target_type == "Drawing an Ace" and card[0] == 'Ace':
            matches += 1
            
    exp_prob = matches / n_draws
    theo_prob = 13/52 if target_type == "Drawing a Heart" else (12/52 if target_type.startswith("Drawing a Face") else 4/52)
    
    col1, col2 = st.columns(2)
    col1.metric("Experimental Probability", f"{exp_prob:.4f}", f"{(exp_prob - theo_prob)*100:+.2f}% vs True")
    col2.metric("Theoretical Probability", f"{theo_prob:.4f}")
    
    st.markdown("### Standard Deck Breakdown")
    st.info("A standard deck has 52 cards, 4 suits (13 cards each), 12 face cards, and 4 aces.")

# ==========================================
# MODULE 4: SAMPLING VARIABILITY
# ==========================================
elif app_mode == "4. Sampling Variability & CLT":
    st.markdown('<p class="main-header">Sampling Variability & The Central Limit Theorem</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Draw multiple samples from a population and watch the distribution of sample means form a bell curve.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        sample_size = st.slider("Sample Size ($n$ per sample)", min_value=2, max_value=100, value=30)
        num_samples = st.slider("Number of Samples", min_value=100, max_value=2000, value=500, step=100)
        pop_dist = st.selectbox("Population Distribution", ["Uniform (1 to 6)", "Skewed (Exponential)", "Binomial"])
    
    with col2:
        if pop_dist == "Uniform (1 to 6)":
            pop_data = np.random.randint(1, 7, size=10000)
        elif pop_dist == "Skewed (Exponential)":
            pop_data = np.random.exponential(scale=2.0, size=10000)
        else:
            pop_data = np.random.binomial(n=10, p=0.3, size=10000)
            
        sample_means = [np.mean(np.random.choice(pop_data, size=sample_size)) for _ in range(num_samples)]
        
        fig = px.histogram(x=sample_means, nbins=30, title="Distribution of Sample Means", labels={"x": "Sample Mean"})
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MODULE 5: INTERACTIVE QUIZ
# ==========================================
elif app_mode == "5. Interactive Quiz":
    st.markdown('<p class="main-header">Probability & Statistics Quiz</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Test your understanding with instant feedback and step-by-step explanations.</p>', unsafe_allow_html=True)
    
    q_choice = st.radio("Select Question:", ["Question 1: Coin Independence", "Question 2: Two Dice Sum", "Question 3: Conditional Card Probability"])
    
    if q_choice == "Question 1: Coin Independence":
        st.markdown("**A fair coin is tossed 4 times and lands on Heads every time. What is the probability that the 5th toss is Heads?**")
        ans = st.radio("Your Answer:", ["1/32 (Very unlikely, due for tails)", "1/2 (Coins have no memory)", "1/16"], key="q1")
        if st.button("Submit Answer", key="b1"):
            if "1/2" in ans:
                st.success("Correct! Coin tosses are independent events. Past outcomes do not influence future tosses.")
            else:
                st.error("Incorrect. Remember the gambler's fallacy: independent events have no memory!")
                
    elif q_choice == "Question 2: Two Dice Sum":
        st.markdown("**What is the most likely sum when rolling two standard 6-sided dice?**")
        ans = st.radio("Your Answer:", ["6", "7", "8", "12"], key="q2")
        if st.button("Submit Answer", key="b2"):
            if ans == "7":
                st.success("Correct! There are 6 different combinations that sum to 7 (1+6, 2+5, 3+4, 4+3, 5+2, 6+1), making it the most frequent outcome.")
            else:
                st.error("Incorrect. 7 has the highest number of combinations (6 ways out of 36).")
                
    else:
        st.markdown("**What is the probability of drawing a King from a standard 52-card deck?**")
        ans = st.radio("Your Answer:", ["1/52", "1/13", "4/13"], key="q3")
        if st.button("Submit Answer", key="b3"):
            if ans == "1/13":
                st.success("Correct! There are 4 Kings in 52 cards, so 4/52 simplifies to 1/13.")
            else:
                st.error("Incorrect. There are 4 Kings in a standard deck of 52 cards (4/52 = 1/13).")

# ==========================================
# MODULE 6: TEACHER RESOURCES
# ==========================================
elif app_mode == "6. Teacher Resources & Worksheets":
    st.markdown('<p class="main-header">Teacher Resources & Lesson Plans</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Downloadable classroom guides, curriculum alignment notes, and printable student worksheets.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>📚 Lesson Plan: Introduction to Experimental vs Theoretical Probability</h3>
        <p><b>Target Audience:</b> KS3 / Year 8 Mathematics<br>
        <b>Duration:</b> 60 minutes<br>
        <b>Learning Objectives:</b>
        <ul>
            <li>Understand the difference between theoretical and experimental probability.</li>
            <li>Conduct trial simulations and record relative frequency data.</li>
            <li>Observe how the Law of Large Numbers stabilizes estimates over time.</li>
        </ul></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>📄 Printable Student Worksheet (Preview)</h3>
        <ol>
            <li><b>Warm-up:</b> If you roll a single die 60 times, how many times would you theoretically expect to roll a 6?</li>
            <li><b>Simulation Task:</b> Using the coin toss module, record the relative frequency of heads after 10, 100, and 1000 trials. What do you notice?</li>
            <li><b>Challenge Problem:</b> Explain why the sum of two dice has a triangular distribution peaking at 7.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.download_button(
        label="Download Full Teacher Activity Pack (PDF / Markdown)",
        data="# Probability Playground - Teacher Pack\n\nFull lesson plan and worksheets for classroom delivery.",
        file_name="probability_playground_teacher_pack.md",
        mime="text/markdown"
    )
