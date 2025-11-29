import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# --------------------------------------------------------
# 🔥 COMPLETE + SAFE PREPROCESSING PIPELINE
# --------------------------------------------------------

def preprocess_data(df, encoding_type="onehot"):
    df = df.copy()

    # -----------------------------
    # 1. Fix Date Columns
    # -----------------------------
    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.datetime64):
            df[col + "_year"] = df[col].dt.year.fillna(df[col].dt.year.median())
            df[col + "_month"] = df[col].dt.month.fillna(df[col].dt.month.median())
            df[col + "_day"] = df[col].dt.day.fillna(df[col].dt.day.median())
            df.drop(columns=[col], inplace=True)

    # -----------------------------
    # 2. Boolean → int
    # -----------------------------
    for col in df.select_dtypes(include=["bool"]).columns:
        df[col] = df[col].astype(int)

    # -----------------------------
    # 3. Categorical Encoding
    # -----------------------------
    cat_cols = df.select_dtypes(include=["object", "category"]).columns

    if encoding_type == "onehot":
        # Fill NA in categories BEFORE one-hot
        df[cat_cols] = df[cat_cols].fillna("Unknown")
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    elif encoding_type == "label":
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = df[col].fillna("Unknown")
            df[col] = le.fit_transform(df[col])

    # -----------------------------
    # 4. Fill Numeric Missing Values
    # -----------------------------
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # -----------------------------
    # 5. Final Check – Remove ANY Remaining NaN
    # -----------------------------
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)

    return df

# ------------------------------------------------------------------------------------------------


def show_overview_cards(df):
    try:
        total_records = len(df)
        total_features = len(df.columns)
        missing_values = df.isnull().sum().sum()
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Records", f"{total_records:,}")
        with c2:
            st.metric("Features", f"{total_features}")
        with c3:
            st.metric("Missing Values", f"{missing_values}")
        with c4:
            st.metric("Numeric Columns", f"{numeric_cols}")
    except Exception as e:
        st.error(f"Error displaying overview: {e}")




def analyze_query_and_respond(df, query):
    query = query.lower().strip()
    
    try:
        # Advanced pattern matching for intelligent responses
        
        # Dataset overview and insights
        if any(word in query for word in ["insight", "tell me about", "overview", "analyze", "summary of data", "what can you tell"]):
            numeric_df = df.select_dtypes(include=[np.number])
            categorical_df = df.select_dtypes(include=['object'])
            
            result = "## 📊 Comprehensive Dataset Analysis\n\n"
            result += f"**Structure:** {len(df):,} rows × {len(df.columns)} columns\n\n"
            
            # Data completeness
            total_cells = len(df) * len(df.columns)
            missing_cells = df.isnull().sum().sum()
            completeness = ((total_cells - missing_cells) / total_cells) * 100
            result += f"**Data Quality:** {completeness:.1f}% complete ({missing_cells:,} missing values)\n\n"
            
            # Numeric insights
            if not numeric_df.empty:
                result += f"### 📈 Numeric Analysis ({len(numeric_df.columns)} columns)\n\n"
                for col in numeric_df.columns[:5]:
                    mean_val = numeric_df[col].mean()
                    std_val = numeric_df[col].std()
                    cv = (std_val / mean_val * 100) if mean_val != 0 else 0
                    result += f"**{col}:**\n"
                    result += f"- Range: [{numeric_df[col].min():.2f}, {numeric_df[col].max():.2f}]\n"
                    result += f"- Mean ± Std: {mean_val:.2f} ± {std_val:.2f}\n"
                    result += f"- Coefficient of Variation: {cv:.1f}%\n\n"
            
            # Categorical insights
            if not categorical_df.empty:
                result += f"### 🏷️ Categorical Analysis ({len(categorical_df.columns)} columns)\n\n"
                for col in categorical_df.columns[:3]:
                    nunique = categorical_df[col].nunique()
                    mode_val = categorical_df[col].mode()[0] if len(categorical_df[col].mode()) > 0 else "N/A"
                    mode_count = (categorical_df[col] == mode_val).sum()
                    result += f"**{col}:** {nunique} categories, most frequent: '{mode_val}' ({mode_count} times)\n"
            
            return result
        
        # Specific column analysis
        for col in df.columns:
            if col.lower() in query and any(word in query for word in ["about", "analyze", "tell", "show", "describe"]):
                result = f"## 📋 Detailed Analysis: '{col}'\n\n"
                result += f"**Data Type:** {df[col].dtype}\n"
                result += f"**Completeness:** {df[col].count()}/{len(df)} values ({df[col].count()/len(df)*100:.1f}%)\n"
                result += f"**Unique Values:** {df[col].nunique()} distinct\n"
                result += f"**Missing:** {df[col].isnull().sum()} values\n\n"
                
                if df[col].dtype in ['int64', 'float64']:
                    result += "### 📊 Statistical Summary\n\n"
                    result += f"| Metric | Value |\n|--------|-------|\n"
                    result += f"| Mean | {df[col].mean():.4f} |\n"
                    result += f"| Median | {df[col].median():.4f} |\n"
                    result += f"| Std Dev | {df[col].std():.4f} |\n"
                    result += f"| Min | {df[col].min():.4f} |\n"
                    result += f"| 25% | {df[col].quantile(0.25):.4f} |\n"
                    result += f"| 75% | {df[col].quantile(0.75):.4f} |\n"
                    result += f"| Max | {df[col].max():.4f} |\n"
                    result += f"| Range | {df[col].max() - df[col].min():.4f} |\n"
                    result += f"| Variance | {df[col].var():.4f} |\n\n"
                    
                    # Outlier detection
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outlier_mask = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
                    outliers = len(df[outlier_mask])
                    
                    if outliers > 0:
                        result += f"### ⚠️ Outlier Detection\n\n"
                        result += f"Found **{outliers}** potential outliers ({outliers/len(df)*100:.1f}% of data)\n"
                        result += f"- Lower bound: {Q1 - 1.5 * IQR:.2f}\n"
                        result += f"- Upper bound: {Q3 + 1.5 * IQR:.2f}\n\n"
                    
                    # Distribution
                    skew = df[col].skew()
                    result += f"### 📉 Distribution\n\n"
                    result += f"**Skewness:** {skew:.3f} "
                    if abs(skew) < 0.5:
                        result += "(approximately symmetric)\n"
                    elif skew > 0:
                        result += "(right-skewed, tail extends right)\n"
                    else:
                        result += "(left-skewed, tail extends left)\n"
                else:
                    result += "### 🏷️ Category Distribution\n\n"
                    top_values = df[col].value_counts().head(10)
                    result += "| Value | Count | Percentage |\n|-------|-------|------------|\n"
                    for val, count in top_values.items():
                        pct = (count / len(df)) * 100
                        result += f"| {val} | {count} | {pct:.1f}% |\n"
                
                return result
        
        # Correlation analysis
        if "correlat" in query or "relationship" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) >= 2:
                corr = numeric_df.corr()
                result = "## 🔗 Correlation Analysis\n\n"
                
                # Find strong correlations
                strong_corr = []
                for i in range(len(corr.columns)):
                    for j in range(i+1, len(corr.columns)):
                        corr_val = corr.iloc[i, j]
                        if abs(corr_val) > 0.3:  # Lowered threshold
                            strong_corr.append((corr.columns[i], corr.columns[j], corr_val))
                
                if strong_corr:
                    result += "### 📊 Significant Correlations\n\n"
                    result += "| Feature 1 | Feature 2 | Correlation | Strength |\n"
                    result += "|-----------|-----------|-------------|----------|\n"
                    for col1, col2, val in sorted(strong_corr, key=lambda x: abs(x[2]), reverse=True):
                        strength = "Very Strong" if abs(val) > 0.8 else "Strong" if abs(val) > 0.6 else "Moderate"
                        result += f"| {col1} | {col2} | {val:.3f} | {strength} |\n"
                else:
                    result += "No significant correlations (>0.3) found between numeric columns.\n"
                
                result += "\n**Interpretation:**\n"
                result += "- Values close to 1: Strong positive relationship\n"
                result += "- Values close to -1: Strong negative relationship\n"
                result += "- Values close to 0: Little to no linear relationship\n"
                
                return result
            return "❌ Need at least 2 numeric columns for correlation analysis."
        
        # Comparison queries
        if "compare" in query or "difference between" in query or "versus" in query or "vs" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                result = "## ⚖️ Numeric Columns Comparison\n\n"
                result += "| Column | Mean | Median | Std Dev | Min | Max | Range |\n"
                result += "|--------|------|--------|---------|-----|-----|-------|\n"
                for col in numeric_df.columns:
                    result += f"| {col} | {numeric_df[col].mean():.2f} | {numeric_df[col].median():.2f} | "
                    result += f"{numeric_df[col].std():.2f} | {numeric_df[col].min():.2f} | "
                    result += f"{numeric_df[col].max():.2f} | {numeric_df[col].max() - numeric_df[col].min():.2f} |\n"
                return result
            return "❌ No numeric columns available for comparison."
        
        # Outlier detection
        if "outlier" in query or "anomal" in query or "extreme" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                result = "## 🎯 Outlier Detection Analysis\n\n"
                result += "Using IQR method (1.5 × IQR beyond quartiles)\n\n"
                result += "| Column | Outliers | Percentage | Lower Bound | Upper Bound |\n"
                result += "|--------|----------|------------|-------------|-------------|\n"
                
                has_outliers = False
                for col in numeric_df.columns:
                    Q1 = numeric_df[col].quantile(0.25)
                    Q3 = numeric_df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    outliers = len(numeric_df[(numeric_df[col] < lower) | (numeric_df[col] > upper)])
                    
                    if outliers > 0:
                        has_outliers = True
                        pct = outliers/len(df)*100
                        result += f"| {col} | {outliers} | {pct:.1f}% | {lower:.2f} | {upper:.2f} |\n"
                
                if not has_outliers:
                    result += "| - | No outliers detected | - | - | - |\n"
                
                return result
            return "❌ No numeric columns to check for outliers."
        
        # Distribution queries
        if "distribut" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                result = "## 📊 Distribution Analysis\n\n"
                result += "| Column | Skewness | Interpretation | Kurtosis |\n"
                result += "|--------|----------|----------------|----------|\n"
                
                for col in numeric_df.columns:
                    skew = numeric_df[col].skew()
                    kurt = numeric_df[col].kurtosis()
                    
                    if abs(skew) < 0.5:
                        interp = "Symmetric"
                    elif skew > 0:
                        interp = "Right-skewed"
                    else:
                        interp = "Left-skewed"
                    
                    result += f"| {col} | {skew:.3f} | {interp} | {kurt:.3f} |\n"
                
                result += "\n**Notes:**\n"
                result += "- Skewness: measures asymmetry (0 = symmetric)\n"
                result += "- Kurtosis: measures tail heaviness (3 = normal)\n"
                
                return result
            return "❌ No numeric columns for distribution analysis."
        
        # Cleaning recommendations
        if "clean" in query or "should i" in query or "recommend" in query or "improve" in query:
            issues = []
            recommendations = []
            
            # Check duplicates
            dup = df.duplicated().sum()
            if dup > 0:
                issues.append(f"✗ **{dup}** duplicate rows found ({dup/len(df)*100:.1f}%)")
                recommendations.append("→ Remove duplicates using the Clean page")
            
            # Check missing values
            missing = df.isnull().sum()
            high_missing = missing[missing > len(df) * 0.5]
            if len(high_missing) > 0:
                issues.append(f"✗ **{len(high_missing)}** columns with >50% missing data")
                recommendations.append(f"→ Consider dropping: {', '.join(high_missing.index.tolist())}")
            
            moderate_missing = missing[(missing > 0) & (missing <= len(df) * 0.5)]
            if len(moderate_missing) > 0:
                issues.append(f"✗ **{len(moderate_missing)}** columns with missing values")
                recommendations.append(f"→ Fill missing in: {', '.join(moderate_missing.index.tolist())}")
            
            # Check data types
            object_cols = df.select_dtypes(include=['object']).columns
            convertible = []
            for col in object_cols:
                try:
                    pd.to_numeric(df[col].dropna(), errors='raise')
                    convertible.append(col)
                except:
                    pass
            
            if convertible:
                issues.append(f"✗ **{len(convertible)}** columns could be numeric")
                recommendations.append(f"→ Convert to numeric: {', '.join(convertible)}")
            
            # Build result
            result = "## 🧹 Data Quality Assessment\n\n"
            
            if issues:
                result += "### ⚠️ Issues Found:\n\n"
                for issue in issues:
                    result += f"{issue}\n"
                
                result += "\n### 💡 Recommendations:\n\n"
                for rec in recommendations:
                    result += f"{rec}\n"
            else:
                result += "### ✅ Data Quality: Excellent!\n\n"
                result += "No major issues detected. Your data is ready for analysis!"
            
            return result
        
        # Feature selection for ML
        if "feature" in query or "machine learning" in query or "ml model" in query or "prediction" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                result = "## 🤖 Machine Learning Feature Analysis\n\n"
                
                # Check variance
                variances = numeric_df.var().sort_values(ascending=False)
                result += "### 📊 Feature Variance (Higher is Better)\n\n"
                result += "| Feature | Variance | Recommendation |\n"
                result += "|---------|----------|----------------|\n"
                for col, var in variances.items():
                    rec = "Good" if var > variances.median() else "Consider removing"
                    result += f"| {col} | {var:.4f} | {rec} |\n"
                
                # Check correlations
                corr = numeric_df.corr()
                result += "\n### 🔗 Multicollinearity Check\n\n"
                high_corr = []
                for i in range(len(corr.columns)):
                    for j in range(i+1, len(corr.columns)):
                        if abs(corr.iloc[i, j]) > 0.9:
                            high_corr.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
                
                if high_corr:
                    result += "⚠️ **Highly correlated features detected (consider removing one):**\n\n"
                    for col1, col2, val in high_corr:
                        result += f"- {col1} ↔ {col2}: {val:.3f}\n"
                else:
                    result += "✅ No problematic multicollinearity detected!\n"
                
                return result
            return "❌ No numeric columns available for feature analysis."
        
        # Count/size queries
        if any(word in query for word in ["how many", "count", "number of", "total"]):
            if "row" in query:
                return f"📊 The dataset contains **{len(df):,}** rows."
            elif "column" in query or "feature" in query:
                return f"📊 The dataset has **{len(df.columns)}** columns: {', '.join(df.columns.tolist())}"
            elif "missing" in query or "null" in query:
                total_missing = df.isnull().sum().sum()
                return f"📊 There are **{total_missing:,}** missing values in the dataset ({total_missing/(len(df)*len(df.columns))*100:.2f}% of all cells)"
            else:
                return f"📊 **Dataset Size:**\n- Rows: {len(df):,}\n- Columns: {len(df.columns)}\n- Total cells: {len(df) * len(df.columns):,}"
        
        # Fallback to basic handler
        return fallback_query_handler(df, query)
        
    except Exception as e:
        return f"❌ Error analyzing query: {str(e)}\n\n💡 Try asking a simpler question or check your data format."

def fallback_query_handler(df, query):
    """"""
    query = query.lower().strip()
    
    try:
        # Basic statistics queries
        if any(word in query for word in ["how many", "count", "total rows", "number of rows"]):
            return f"📊 The dataset contains **{len(df):,}** rows and **{len(df.columns)}** columns."
        
        elif "columns" in query or "features" in query or "what columns" in query:
            cols = ", ".join(df.columns.tolist())
            return f"📋 **Columns in dataset:** {cols}"
        
        elif "missing" in query or "null" in query:
            missing = df.isnull().sum()
            missing_cols = missing[missing > 0]
            if len(missing_cols) > 0:
                result = "⚠️ **Missing values:**\n\n"
                for col, count in missing_cols.items():
                    result += f"- {col}: {count} ({count/len(df)*100:.1f}%)\n"
                return result
            else:
                return "✅ No missing values found in the dataset!"
        
        elif "summary" in query or "describe" in query or "statistics" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                stats = numeric_df.describe().round(2)
                result = "📈 **Summary Statistics:**\n\n"
                result += stats.to_string()
                return result
            else:
                return "No numeric columns to summarize."
        
        elif "mean" in query or "average" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                means = numeric_df.mean()
                result = "📊 **Mean values:**\n\n"
                for col, val in means.items():
                    result += f"- {col}: {val:.2f}\n"
                return result
            else:
                return "No numeric columns to calculate mean."
        
        elif "max" in query or "maximum" in query or "highest" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                maxs = numeric_df.max()
                result = "📈 **Maximum values:**\n\n"
                for col, val in maxs.items():
                    result += f"- {col}: {val:.2f}\n"
                return result
            else:
                return "No numeric columns to find maximum."
        
        elif "min" in query or "minimum" in query or "lowest" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                mins = numeric_df.min()
                result = "📉 **Minimum values:**\n\n"
                for col, val in mins.items():
                    result += f"- {col}: {val:.2f}\n"
                return result
            else:
                return "No numeric columns to find minimum."
        
        elif "unique" in query or "distinct" in query:
            result = "🔢 **Unique values per column:**\n\n"
            for col in df.columns:
                result += f"- {col}: {df[col].nunique()} unique values\n"
            return result
        
        elif "show" in query and "data" in query:
            return f"📄 **First few rows:**\n\n{df.head().to_string()}"
        
        elif "correlation" in query or "corr" in query:
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) >= 2:
                corr = numeric_df.corr().round(2)
                return f"🔗 **Correlation Matrix:**\n\n{corr.to_string()}"
            else:
                return "Need at least 2 numeric columns for correlation analysis."
        
        # Column-specific queries
        for col in df.columns:
            if col.lower() in query:
                result = f"📊 **Information about '{col}':**\n\n"
                result += f"- Data type: {df[col].dtype}\n"
                result += f"- Non-null count: {df[col].count()}\n"
                result += f"- Missing values: {df[col].isnull().sum()}\n"
                result += f"- Unique values: {df[col].nunique()}\n"
                
                if df[col].dtype in ['int64', 'float64']:
                    result += f"- Mean: {df[col].mean():.2f}\n"
                    result += f"- Min: {df[col].min():.2f}\n"
                    result += f"- Max: {df[col].max():.2f}\n"
                    result += f"- Median: {df[col].median():.2f}\n"
                else:
                    top_values = df[col].value_counts().head(5)
                    result += f"\n**Top 5 values:**\n"
                    for val, count in top_values.items():
                        result += f"- {val}: {count} occurrences\n"
                
                return result
        
        # Default response
        return """💡 I can help you explore your data! Try asking:

**General Questions:**
- "How many rows are there?"
- "What are the columns?"
- "Show me the data"
- "Give me a summary"

**Statistics:**
- "What's the average/mean?"
- "Show maximum/minimum values"
- "What are the missing values?"
- "Show unique values"
- "Calculate correlation"

**Column-Specific:**
- "Tell me about [column name]"
- "What's the average [column name]?"

Ask me anything about your dataset!"""
    
    except Exception as e:
        return f"❌ Error processing query: {e}"
