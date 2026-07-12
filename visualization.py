"""
visualization.py
-----------------
Reusable matplotlib / plotly chart builders used across the analysis
notebooks, ensuring a consistent visual style throughout the project.

Author: Analytics Engineering Team
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

PALETTE = {
    "Google Ads": "#4285F4", "Facebook Ads": "#1877F2", "LinkedIn": "#0A66C2",
    "Email Marketing": "#EA4335", "Organic Search": "#34A853",
    "Referral": "#FBBC05", "Affiliate": "#8E44AD",
}

sns.set_theme(style="whitegrid", context="talk")


def plot_channel_roi(campaigns: pd.DataFrame, save_path: str = None):
    """Bar chart of average ROI by channel."""
    agg = campaigns.groupby("channel")["roi"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [PALETTE.get(c, "#888") for c in agg.index]
    ax.bar(agg.index, agg.values, color=colors)
    ax.set_title("Average ROI by Marketing Channel")
    ax.set_ylabel("ROI (x)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    return fig


def plot_monthly_revenue_trend(monthly: pd.DataFrame, save_path: str = None):
    """Interactive Plotly line chart of monthly revenue by channel."""
    fig = px.line(
        monthly, x="month", y="total_revenue", color="channel",
        color_discrete_map=PALETTE,
        title="Monthly Revenue Trend by Channel",
        markers=True,
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)")
    if save_path:
        fig.write_html(save_path)
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, columns: list, save_path: str = None):
    """Correlation heatmap for a set of numeric columns."""
    corr = df[columns].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
    ax.set_title("Correlation Matrix — Campaign KPIs")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    return fig


def plot_conversion_funnel(stage_labels: list, stage_values: list, save_path: str = None):
    """Plotly funnel chart (e.g. Impressions -> Clicks -> Conversions -> Purchases)."""
    fig = go.Figure(go.Funnel(y=stage_labels, x=stage_values,
                               textinfo="value+percent initial"))
    fig.update_layout(title="Acquisition Conversion Funnel")
    if save_path:
        fig.write_html(save_path)
    return fig


def plot_geo_performance(customers: pd.DataFrame, save_path: str = None):
    """Bar chart of total lifetime value by country."""
    agg = customers.groupby("country")["lifetime_value"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(agg.index[::-1], agg.values[::-1], color="#2E86AB")
    ax.set_title("Total Customer Lifetime Value by Country")
    ax.set_xlabel("Lifetime Value ($)")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    return fig


def plot_device_conversion(campaigns_or_master: pd.DataFrame, save_path: str = None):
    """Grouped bar of conversion rate by device (expects a 'device' column)."""
    agg = campaigns_or_master.groupby("device").size().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(agg.index, agg.values, color="#F18F01")
    ax.set_title("Transaction Volume by Device")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    return fig
