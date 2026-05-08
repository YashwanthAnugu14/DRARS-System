import streamlit as st
import pandas as pd
import numpy as np
import json
import hashlib
import datetime
import io
import csv
import random
import math
import copy
from collections import defaultdict

st.set_page_config(
    page_title="DRARS - Dual-Relationship Analysis System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DARK_BG = "#0a0a0a"
CARD_BG = "#111111"
CARD_BORDER = "#1a1a1a"
ACCENT = "#76b900"
ACCENT2 = "#5a8f00"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#999999"
TEXT_MUTED = "#555555"
DANGER = "#e53935"
WARNING = "#f59e0b"
INFO = "#0ea5e9"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
}}

.stApp {{
    background-color: {DARK_BG};
}}

section[data-testid="stSidebar"] {{
    display: none !important;
    width: 0px !important;
}}

header[data-testid="stHeader"] {{
    background-color: transparent;
    border-bottom: 1px solid {CARD_BORDER};
}}

div[data-testid="stToolbar"] {{
    display: none;
}}

.main-topbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: rgba(10,10,10,0.97);
    border-bottom: 2px solid {ACCENT};
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    height: 64px;
    backdrop-filter: blur(12px);
}}

.topbar-brand {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.topbar-logo-block {{
    width: 38px;
    height: 38px;
    background: {ACCENT};
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.topbar-logo-inner {{
    width: 18px;
    height: 18px;
    background: {DARK_BG};
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}}

.topbar-title {{
    font-size: 18px;
    font-weight: 800;
    color: {TEXT_PRIMARY};
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

.topbar-title span {{
    color: {ACCENT};
}}

.topbar-nav {{
    display: flex;
    align-items: center;
    gap: 6px;
}}

.topbar-nav-item {{
    padding: 6px 14px;
    border-radius: 4px;
    color: {TEXT_SECONDARY};
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: 1px solid transparent;
}}

.topbar-nav-item:hover {{
    color: {TEXT_PRIMARY};
    background: rgba(118,185,0,0.1);
    border-color: rgba(118,185,0,0.2);
}}

.topbar-nav-active {{
    color: {ACCENT};
    background: rgba(118,185,0,0.12);
    border-color: {ACCENT};
}}

.topbar-user {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.user-badge {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: rgba(118,185,0,0.08);
    border: 1px solid rgba(118,185,0,0.2);
    border-radius: 4px;
}}

.user-avatar {{
    width: 28px;
    height: 28px;
    background: {ACCENT};
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    color: {DARK_BG};
}}

.user-info {{
    display: flex;
    flex-direction: column;
}}

.user-name {{
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}

.user-role {{
    font-size: 10px;
    color: {ACCENT};
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.main-content {{
    margin-top: 80px;
    padding: 24px 32px;
}}

.hero-section {{
    background: linear-gradient(135deg, #0d1a00 0%, #0a0a0a 50%, #001a0d 100%);
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 48px 56px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}}

.hero-section::before {{
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(118,185,0,0.08) 0%, transparent 70%);
    pointer-events: none;
}}

.hero-section::after {{
    content: '';
    position: absolute;
    bottom: -80px;
    left: -80px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(118,185,0,0.05) 0%, transparent 70%);
    pointer-events: none;
}}

.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(118,185,0,0.1);
    border: 1px solid rgba(118,185,0,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    color: {ACCENT};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
}}

.hero-title {{
    font-size: 48px;
    font-weight: 900;
    line-height: 1.1;
    color: {TEXT_PRIMARY};
    margin-bottom: 16px;
    letter-spacing: -1px;
}}

.hero-title span {{
    color: {ACCENT};
}}

.hero-subtitle {{
    font-size: 17px;
    color: {TEXT_SECONDARY};
    max-width: 680px;
    line-height: 1.6;
    margin-bottom: 32px;
}}

.hero-stats {{
    display: flex;
    gap: 40px;
}}

.hero-stat {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.hero-stat-value {{
    font-size: 32px;
    font-weight: 800;
    color: {ACCENT};
    line-height: 1;
}}

.hero-stat-label {{
    font-size: 12px;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 20px;
    position: relative;
    transition: border-color 0.2s;
}}

.card:hover {{
    border-color: rgba(118,185,0,0.2);
}}

.card-accent {{
    border-top: 3px solid {ACCENT};
}}

.card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid {CARD_BORDER};
}}

.card-title {{
    font-size: 15px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.card-title-dot {{
    width: 8px;
    height: 8px;
    background: {ACCENT};
    border-radius: 50%;
}}

.section-heading {{
    font-size: 22px;
    font-weight: 800;
    color: {TEXT_PRIMARY};
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}}

.section-sub {{
    font-size: 13px;
    color: {TEXT_MUTED};
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.metric-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}}

.metric-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: {ACCENT};
}}

.metric-value {{
    font-size: 36px;
    font-weight: 900;
    color: {ACCENT};
    line-height: 1;
    margin-bottom: 4px;
}}

.metric-label {{
    font-size: 11px;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 500;
}}

.metric-delta {{
    font-size: 12px;
    color: {TEXT_SECONDARY};
    margin-top: 8px;
}}

.metric-delta.up {{
    color: {ACCENT};
}}

.metric-delta.down {{
    color: {DANGER};
}}

.tag {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}}

.tag-green {{
    background: rgba(118,185,0,0.12);
    color: {ACCENT};
    border: 1px solid rgba(118,185,0,0.2);
}}

.tag-red {{
    background: rgba(229,57,53,0.12);
    color: {DANGER};
    border: 1px solid rgba(229,57,53,0.2);
}}

.tag-blue {{
    background: rgba(14,165,233,0.12);
    color: {INFO};
    border: 1px solid rgba(14,165,233,0.2);
}}

.tag-yellow {{
    background: rgba(245,158,11,0.12);
    color: {WARNING};
    border: 1px solid rgba(245,158,11,0.2);
}}

.tag-gray {{
    background: rgba(85,85,85,0.2);
    color: {TEXT_SECONDARY};
    border: 1px solid {CARD_BORDER};
}}

.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

.data-table th {{
    background: rgba(118,185,0,0.06);
    color: {ACCENT};
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 10px 16px;
    text-align: left;
    border-bottom: 1px solid {CARD_BORDER};
}}

.data-table td {{
    padding: 10px 16px;
    border-bottom: 1px solid rgba(26,26,26,0.8);
    color: {TEXT_SECONDARY};
    vertical-align: middle;
}}

.data-table tr:hover td {{
    background: rgba(118,185,0,0.03);
    color: {TEXT_PRIMARY};
}}

.data-table td:first-child {{
    color: {TEXT_PRIMARY};
    font-weight: 500;
}}

.alert-card {{
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 13px;
}}

.alert-success {{
    background: rgba(118,185,0,0.08);
    border: 1px solid rgba(118,185,0,0.2);
    color: {ACCENT};
}}

.alert-error {{
    background: rgba(229,57,53,0.08);
    border: 1px solid rgba(229,57,53,0.2);
    color: {DANGER};
}}

.alert-warning {{
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    color: {WARNING};
}}

.alert-info {{
    background: rgba(14,165,233,0.08);
    border: 1px solid rgba(14,165,233,0.2);
    color: {INFO};
}}

.group-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.2s;
}}

.group-card:hover {{
    border-color: rgba(118,185,0,0.3);
    transform: translateY(-1px);
}}

.group-rank {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}}

.rank-badge {{
    width: 36px;
    height: 36px;
    background: {ACCENT};
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 800;
    color: {DARK_BG};
}}

.group-members {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
}}

.member-chip {{
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.04);
    border: 1px solid {CARD_BORDER};
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: {TEXT_SECONDARY};
}}

.member-chip-dot {{
    width: 6px;
    height: 6px;
    background: {ACCENT};
    border-radius: 50%;
}}

.score-bar-container {{
    margin-bottom: 8px;
}}

.score-bar-label {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: {TEXT_MUTED};
    margin-bottom: 4px;
}}

.score-bar-track {{
    height: 4px;
    background: rgba(255,255,255,0.05);
    border-radius: 2px;
    overflow: hidden;
}}

.score-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, {ACCENT2}, {ACCENT});
    border-radius: 2px;
    transition: width 0.5s ease;
}}

.network-node {{
    cursor: pointer;
    transition: all 0.2s;
}}

.log-entry {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(26,26,26,0.5);
    font-size: 12px;
}}

.log-time {{
    color: {TEXT_MUTED};
    white-space: nowrap;
    min-width: 130px;
}}

.log-user {{
    color: {ACCENT};
    font-weight: 600;
    min-width: 80px;
}}

.log-action {{
    color: {TEXT_SECONDARY};
    flex: 1;
}}

.login-page {{
    min-height: 100vh;
    background: {DARK_BG};
    display: flex;
    align-items: center;
    justify-content: center;
}}

.login-container {{
    width: 100%;
    max-width: 460px;
}}

.login-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-top: 3px solid {ACCENT};
    border-radius: 8px;
    padding: 48px;
}}

.login-logo-area {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 36px;
}}

.login-logo-hex {{
    width: 64px;
    height: 64px;
    background: {ACCENT};
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
}}

.login-logo-inner {{
    width: 28px;
    height: 28px;
    background: {DARK_BG};
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}}

.login-system-name {{
    font-size: 22px;
    font-weight: 900;
    color: {TEXT_PRIMARY};
    letter-spacing: 1px;
    text-align: center;
    text-transform: uppercase;
}}

.login-system-name span {{
    color: {ACCENT};
}}

.login-tagline {{
    font-size: 12px;
    color: {TEXT_MUTED};
    text-align: center;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.login-form-label {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
    display: block;
}}

.progress-ring-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.progress-ring-value {{
    position: absolute;
    font-size: 20px;
    font-weight: 800;
    color: {ACCENT};
}}

.scenario-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 14px;
    cursor: pointer;
    transition: all 0.2s;
}}

.scenario-card:hover {{
    border-color: rgba(118,185,0,0.3);
}}

.scenario-card-active {{
    border-color: {ACCENT};
    background: rgba(118,185,0,0.04);
}}

.tab-bar {{
    display: flex;
    gap: 0;
    border-bottom: 1px solid {CARD_BORDER};
    margin-bottom: 24px;
}}

.tab-item {{
    padding: 12px 20px;
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_MUTED};
    cursor: pointer;
    border-bottom: 2px solid transparent;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.2s;
}}

.tab-item:hover {{
    color: {TEXT_SECONDARY};
}}

.tab-active {{
    color: {ACCENT};
    border-bottom-color: {ACCENT};
}}

.comparison-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
}}

.empty-state {{
    text-align: center;
    padding: 60px 20px;
}}

.empty-state-icon {{
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.3;
}}

.empty-state-title {{
    font-size: 16px;
    font-weight: 600;
    color: {TEXT_SECONDARY};
    margin-bottom: 8px;
}}

.empty-state-text {{
    font-size: 13px;
    color: {TEXT_MUTED};
}}

div.stButton > button {{
    background: {ACCENT};
    color: {DARK_BG};
    font-weight: 700;
    font-size: 13px;
    border: none;
    border-radius: 4px;
    padding: 8px 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
    width: 100%;
}}

div.stButton > button:hover {{
    background: {ACCENT2};
    transform: translateY(-1px);
}}

div.stButton > button[kind="secondary"] {{
    background: transparent;
    color: {ACCENT};
    border: 1px solid {ACCENT};
}}

div.stButton > button[kind="secondary"]:hover {{
    background: rgba(118,185,0,0.08);
}}

.stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {{
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 4px !important;
    color: {TEXT_PRIMARY} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}}

.stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 2px rgba(118,185,0,0.12) !important;
}}

label, .stRadio label, .stCheckbox label, .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label, .stSlider label {{
    color: {TEXT_MUTED} !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-family: 'Inter', sans-serif !important;
}}

.stSlider .stSlider-thumb {{
    background: {ACCENT} !important;
}}

.stMultiSelect div {{
    background: rgba(255,255,255,0.04) !important;
    border-color: {CARD_BORDER} !important;
}}

.stExpander {{
    background: {CARD_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 6px !important;
}}

.stExpander details summary {{
    color: {TEXT_PRIMARY} !important;
    font-weight: 600 !important;
}}

div.stAlert {{
    background: rgba(118,185,0,0.08) !important;
    border: 1px solid rgba(118,185,0,0.2) !important;
    color: {ACCENT} !important;
    border-radius: 6px !important;
}}

.stDataFrame {{
    background: {CARD_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 6px !important;
}}

div[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 16px 20px;
    border-top: 3px solid {ACCENT};
}}

div[data-testid="stMetricValue"] {{
    color: {ACCENT} !important;
    font-weight: 800 !important;
}}

div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED} !important;
    text-transform: uppercase !important;
    font-size: 11px !important;
    letter-spacing: 0.5px !important;
}}

div[data-testid="column"] {{
    padding: 0 6px !important;
}}

.stProgress .st-bo {{
    background: {ACCENT} !important;
}}

.stProgress .st-bg {{
    background: rgba(255,255,255,0.05) !important;
}}

hr {{
    border-color: {CARD_BORDER} !important;
}}

.stRadio div[role="radiogroup"] label {{
    color: {TEXT_SECONDARY} !important;
    font-size: 13px !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}}

.streamlit-expanderContent {{
    background: rgba(0,0,0,0.2) !important;
}}

::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: {DARK_BG};
}}
::-webkit-scrollbar-thumb {{
    background: rgba(118,185,0,0.3);
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {ACCENT};
}}

.sparkline-container {{
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 40px;
}}

.sparkline-bar {{
    flex: 1;
    background: rgba(118,185,0,0.3);
    border-radius: 2px 2px 0 0;
    transition: background 0.2s;
    min-width: 4px;
}}

.sparkline-bar:hover {{
    background: {ACCENT};
}}

.node-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 10px;
    padding: 10px 0;
}}

.node-box {{
    background: rgba(255,255,255,0.03);
    border: 1px solid {CARD_BORDER};
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    font-size: 11px;
    color: {TEXT_SECONDARY};
    transition: all 0.2s;
    cursor: pointer;
}}

.node-box:hover {{
    border-color: {ACCENT};
    background: rgba(118,185,0,0.06);
    color: {TEXT_PRIMARY};
}}

.node-box-active {{
    border-color: {ACCENT};
    background: rgba(118,185,0,0.1);
    color: {ACCENT};
}}

.node-box-name {{
    font-weight: 700;
    font-size: 13px;
    color: {TEXT_PRIMARY};
    margin-bottom: 2px;
}}

.node-box-role {{
    font-size: 10px;
    color: {TEXT_MUTED};
    text-transform: uppercase;
}}

.divider {{
    height: 1px;
    background: {CARD_BORDER};
    margin: 20px 0;
}}

.fullwidth-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 28px 32px;
    margin-bottom: 20px;
}}

.annotation-chip {{
    background: rgba(118,185,0,0.08);
    border: 1px solid rgba(118,185,0,0.15);
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 12px;
    color: {TEXT_SECONDARY};
    margin-bottom: 8px;
    display: flex;
    gap: 8px;
}}

.annotation-author {{
    color: {ACCENT};
    font-weight: 600;
    white-space: nowrap;
}}

.sim-progress-bar {{
    height: 8px;
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
    margin: 4px 0 16px;
    overflow: hidden;
}}

.sim-progress-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #2d5a00, {ACCENT});
    transition: width 0.4s;
}}

.heatmap-cell {{
    width: 28px;
    height: 28px;
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    font-weight: 700;
    color: {DARK_BG};
    cursor: pointer;
    transition: transform 0.1s;
}}

.heatmap-cell:hover {{
    transform: scale(1.15);
}}

.pulse-dot {{
    width: 8px;
    height: 8px;
    background: {ACCENT};
    border-radius: 50%;
    animation: pulse 2s infinite;
    display: inline-block;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.5; transform: scale(1.2); }}
}}

.filter-chip {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(118,185,0,0.08);
    border: 1px solid rgba(118,185,0,0.2);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    color: {ACCENT};
    margin: 2px;
    cursor: pointer;
    transition: all 0.2s;
}}

.filter-chip-inactive {{
    background: rgba(255,255,255,0.03);
    border-color: {CARD_BORDER};
    color: {TEXT_MUTED};
}}

.filter-chip:hover {{
    background: rgba(118,185,0,0.14);
}}

.conflict-card {{
    background: rgba(229,57,53,0.06);
    border: 1px solid rgba(229,57,53,0.2);
    border-radius: 6px;
    padding: 14px;
    margin-bottom: 10px;
    font-size: 12px;
    color: {TEXT_SECONDARY};
}}

.conflict-title {{
    color: {DANGER};
    font-weight: 700;
    font-size: 13px;
    margin-bottom: 6px;
}}

.strength-bar-wrap {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}}

.strength-label {{
    font-size: 11px;
    color: {TEXT_MUTED};
    width: 90px;
    text-transform: uppercase;
}}

.strength-track {{
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.04);
    border-radius: 3px;
    overflow: hidden;
}}

.strength-fill {{
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, {ACCENT2}, {ACCENT});
}}

.strength-value {{
    font-size: 11px;
    font-weight: 700;
    color: {ACCENT};
    width: 36px;
    text-align: right;
}}
</style>
""", unsafe_allow_html=True)

def init_state():
    if "db" not in st.session_state:
        st.session_state.db = {
            "users": {
                "admin": {
                    "password": hashlib.sha256("admin123".encode()).hexdigest(),
                    "role": "Admin",
                    "created": str(datetime.datetime.now())
                },
                "analyst": {
                    "password": hashlib.sha256("analyst123".encode()).hexdigest(),
                    "role": "Analyst",
                    "created": str(datetime.datetime.now())
                }
            },
            "individuals": {},
            "skill_categories": {
                "Engineering": ["Python", "Java", "C++", "Machine Learning", "Data Engineering"],
                "Design": ["UI/UX", "Graphic Design", "Prototyping", "Figma"],
                "Management": ["Agile", "Scrum", "Leadership", "Planning"],
                "Analytics": ["Statistics", "Power BI", "Tableau", "SQL"],
                "Communication": ["Technical Writing", "Presentation", "Stakeholder Management"]
            },
            "collaborations": {},
            "skill_similarities": {},
            "scenarios": {},
            "rules": {
                "collab_weight": 0.6,
                "similarity_weight": 0.4,
                "min_score_threshold": 3.0,
                "max_group_size": 5,
                "min_group_size": 2
            },
            "audit_logs": [],
            "backups": {},
            "annotations": {},
            "user_roles": {}
        }
        _seed_data()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "current_role" not in st.session_state:
        st.session_state.current_role = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = {}
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

def _seed_data():
    db = st.session_state.db
    names = [
        ("Alice Chen", ["Python", "Machine Learning", "Statistics"]),
        ("Bob Patel", ["Java", "Agile", "Scrum"]),
        ("Carla Rivera", ["UI/UX", "Figma", "Prototyping"]),
        ("David Kim", ["SQL", "Power BI", "Data Engineering"]),
        ("Emma Stone", ["Leadership", "Planning", "Stakeholder Management"]),
        ("Frank Torres", ["C++", "Machine Learning", "Statistics"]),
        ("Grace Liu", ["Technical Writing", "Presentation", "Figma"]),
        ("Henry Park", ["Python", "SQL", "Tableau"]),
        ("Irene Mehta", ["Agile", "Leadership", "Scrum"]),
        ("James Wu", ["Graphic Design", "UI/UX", "Prototyping"]),
        ("Kara Jones", ["Machine Learning", "Python", "Data Engineering"]),
        ("Leo Diaz", ["Java", "C++", "SQL"])
    ]
    interests = ["AI Research", "Data Visualization", "Team Collaboration", "Open Source", "Cloud Computing", "Process Optimization"]
    for i, (name, skills) in enumerate(names):
        uid = f"IND{i+1:03d}"
        db["individuals"][uid] = {
            "id": uid,
            "name": name,
            "skills": skills,
            "interests": random.sample(interests, k=random.randint(1, 3)),
            "email": name.replace(" ", ".").lower() + "@collabtech.com",
            "department": random.choice(["Engineering", "Design", "Analytics", "Management"]),
            "created": str(datetime.datetime.now() - datetime.timedelta(days=random.randint(10, 200)))
        }
    ids = list(db["individuals"].keys())
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            if random.random() < 0.55:
                key = f"{ids[i]}_{ids[j]}"
                db["collaborations"][key] = {
                    "i1": ids[i], "i2": ids[j],
                    "score": round(random.uniform(1.0, 10.0), 2),
                    "projects": random.randint(1, 8),
                    "last_collab": str(datetime.datetime.now() - datetime.timedelta(days=random.randint(5, 365)))
                }
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            if random.random() < 0.65:
                key = f"{ids[i]}_{ids[j]}"
                s1 = set(db["individuals"][ids[i]]["skills"])
                s2 = set(db["individuals"][ids[j]]["skills"])
                auto = round(len(s1 & s2) / max(len(s1 | s2), 1) * 10, 2)
                db["skill_similarities"][key] = {
                    "i1": ids[i], "i2": ids[j],
                    "score": round(max(auto + random.uniform(-1, 1), 0.1), 2)
                }
    db["scenarios"]["SCN001"] = {
        "id": "SCN001",
        "name": "Alpha Team Formation",
        "individuals": ids[:8],
        "collab_weight": 0.65,
        "similarity_weight": 0.35,
        "description": "Primary scenario for Q1 team building",
        "created_by": "analyst",
        "created": str(datetime.datetime.now() - datetime.timedelta(days=5)),
        "status": "Analyzed"
    }
    db["scenarios"]["SCN002"] = {
        "id": "SCN002",
        "name": "Research Cluster Beta",
        "individuals": ids[4:],
        "collab_weight": 0.4,
        "similarity_weight": 0.6,
        "description": "Research-focused grouping with skill similarity bias",
        "created_by": "analyst",
        "created": str(datetime.datetime.now() - datetime.timedelta(days=2)),
        "status": "Pending"
    }
    _log_action("system", "System initialized with seed data", db)

def _log_action(user, action, db=None):
    if db is None:
        db = st.session_state.db
    db["audit_logs"].append({
        "timestamp": str(datetime.datetime.now()),
        "user": user,
        "action": action
    })
    if len(db["audit_logs"]) > 500:
        db["audit_logs"] = db["audit_logs"][-500:]

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def authenticate(username, password):
    db = st.session_state.db
    if username in db["users"]:
        if db["users"][username]["password"] == hash_pw(password):
            return db["users"][username]["role"]
    return None

def compute_compatibility(i1_id, i2_id, collab_w, sim_w):
    db = st.session_state.db
    key1 = f"{i1_id}_{i2_id}"
    key2 = f"{i2_id}_{i1_id}"
    collab_score = 0
    sim_score = 0
    if key1 in db["collaborations"]:
        collab_score = db["collaborations"][key1]["score"]
    elif key2 in db["collaborations"]:
        collab_score = db["collaborations"][key2]["score"]
    if key1 in db["skill_similarities"]:
        sim_score = db["skill_similarities"][key1]["score"]
    elif key2 in db["skill_similarities"]:
        sim_score = db["skill_similarities"][key2]["score"]
    return round(collab_w * collab_score + sim_w * sim_score, 3)

def run_analysis(scenario_id):
    db = st.session_state.db
    if scenario_id not in db["scenarios"]:
        return None
    scn = db["scenarios"][scenario_id]
    inds = scn["individuals"]
    cw = scn["collab_weight"]
    sw = scn["similarity_weight"]
    matrix = {}
    for i in range(len(inds)):
        for j in range(i+1, len(inds)):
            score = compute_compatibility(inds[i], inds[j], cw, sw)
            matrix[(inds[i], inds[j])] = score
            matrix[(inds[j], inds[i])] = score
    min_score = db["rules"]["min_score_threshold"]
    max_grp = int(db["rules"]["max_group_size"])
    min_grp = int(db["rules"]["min_group_size"])
    adjacency = defaultdict(list)
    for (i1, i2), sc in matrix.items():
        if sc >= min_score:
            adjacency[i1].append((i2, sc))
    visited = set()
    groups = []
    def bfs(start):
        queue = [start]
        cluster = []
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            cluster.append(node)
            for nb, _ in adjacency[node]:
                if nb not in visited and nb in inds:
                    queue.append(nb)
        return cluster
    for ind in inds:
        if ind not in visited:
            grp = bfs(ind)
            if min_grp <= len(grp) <= max_grp:
                groups.append(grp)
            elif len(grp) > max_grp:
                for chunk_start in range(0, len(grp), max_grp):
                    chunk = grp[chunk_start:chunk_start+max_grp]
                    if len(chunk) >= min_grp:
                        groups.append(chunk)
            else:
                groups.append(grp)
    ranked = []
    for grp in groups:
        if len(grp) < 2:
            continue
        total = 0
        count = 0
        for i in range(len(grp)):
            for j in range(i+1, len(grp)):
                total += matrix.get((grp[i], grp[j]), 0)
                count += 1
        avg = round(total / count, 3) if count > 0 else 0
        ranked.append({"members": grp, "avg_score": avg, "total_score": round(total, 3), "pair_count": count})
    ranked.sort(key=lambda x: x["avg_score"], reverse=True)
    for i, g in enumerate(ranked):
        g["rank"] = i + 1
    conflicts = []
    for i in range(len(inds)):
        for j in range(i+1, len(inds)):
            sc = matrix.get((inds[i], inds[j]), 0)
            if 0 < sc < min_score * 0.5:
                n1 = db["individuals"][inds[i]]["name"]
                n2 = db["individuals"][inds[j]]["name"]
                conflicts.append({"i1": inds[i], "i2": inds[j], "n1": n1, "n2": n2, "score": sc, "reason": "Very low compatibility score"})
    result = {
        "scenario_id": scenario_id,
        "groups": ranked,
        "matrix": {f"{k[0]}_{k[1]}": v for k, v in matrix.items()},
        "conflicts": conflicts,
        "individuals": inds,
        "timestamp": str(datetime.datetime.now())
    }
    db["scenarios"][scenario_id]["status"] = "Analyzed"
    _log_action(st.session_state.current_user, f"Ran analysis on scenario {scn['name']}")
    return result

def render_topbar():
    user = st.session_state.current_user
    role = st.session_state.current_role
    initials = "".join([p[0].upper() for p in user.split()[:2]]) if user else "?"
    nav_pages = ["Dashboard", "Individuals", "Relationships", "Scenarios", "Analysis", "Reports", "Admin"] if role == "Admin" else ["Dashboard", "Individuals", "Scenarios", "Analysis", "Reports"]
    st.markdown(f"""
    <div class="main-topbar">
        <div class="topbar-brand">
            <div class="topbar-title">DRAR<span>S</span></div>
        </div>
        <div class="topbar-nav">
            {''.join([f'<div class="topbar-nav-item {"topbar-nav-active" if st.session_state.page == p else ""}">{p}</div>' for p in nav_pages])}
        </div>
        <div class="topbar-user">
            <div class="user-badge">
                <div class="user-avatar">{initials}</div>
                <div class="user-info">
                    <div class="user-name">{user}</div>
                    <div class="user-role">{role}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    nav_pages_full = ["Dashboard", "Individuals", "Relationships", "Scenarios", "Analysis", "Reports", "Admin"] if role == "Admin" else ["Dashboard", "Individuals", "Scenarios", "Analysis", "Reports"]
    cols = st.columns(len(nav_pages_full) + 2)
    for i, p in enumerate(nav_pages_full):
        with cols[i]:
            if st.button(p, key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()
    with cols[-1]:
        if st.button("Logout", key="logout_btn", use_container_width=True):
            _log_action(st.session_state.current_user, "User logged out")
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.current_role = None
            st.session_state.page = "Dashboard"
            st.rerun()

def render_login():
    db = st.session_state.db
    st.markdown('<div style="height:80px"></div>', unsafe_allow_html=True)
    cols = st.columns([1, 1.3, 1])
    with cols[1]:
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:32px;">
            <div style="font-size:28px;font-weight:900;color:{TEXT_PRIMARY};text-transform:uppercase;letter-spacing:2px;">
                DRAR<span style="color:{ACCENT}">S</span>
            </div>
            <div style="font-size:11px;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:1.5px;margin-top:6px;">
                Dual-Relationship Analysis & Recommendation System
            </div>
        </div>
        """, unsafe_allow_html=True)
        mode = st.session_state.auth_mode
        tab_cols = st.columns(2)
        with tab_cols[0]:
            if st.button("Sign In", key="tab_login", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
        with tab_cols[1]:
            if st.button("Register", key="tab_register", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="background:{CARD_BG};border:1px solid {CARD_BORDER};border-top:3px solid {ACCENT};border-radius:8px;padding:36px 36px 28px;">""", unsafe_allow_html=True)
        if mode == "login":
            st.markdown(f'<div style="font-size:18px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:24px;">Welcome Back</div>', unsafe_allow_html=True)
            username = st.text_input("Username", key="login_user", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            if st.button("Access System", key="do_login", use_container_width=True):
                role = authenticate(username, password)
                if role:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.current_role = role
                    _log_action(username, f"User logged in as {role}")
                    st.rerun()
                else:
                    st.markdown(f'<div class="alert-card alert-error">Invalid credentials. Please try again.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:18px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:24px;">Create Account</div>', unsafe_allow_html=True)
            new_user = st.text_input("Username", key="reg_user", placeholder="Choose a username")
            new_email = st.text_input("Email", key="reg_email", placeholder="your@email.com")
            new_pass = st.text_input("Password", type="password", key="reg_pass", placeholder="Create password")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")
            new_role = st.selectbox("Access Role", ["Analyst", "Admin"], key="reg_role")
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            if st.button("Create Account", key="do_register", use_container_width=True):
                if not new_user or not new_pass:
                    st.markdown(f'<div class="alert-card alert-error">Username and password are required.</div>', unsafe_allow_html=True)
                elif new_user in db["users"]:
                    st.markdown(f'<div class="alert-card alert-error">Username already exists. Choose another.</div>', unsafe_allow_html=True)
                elif new_pass != confirm_pass:
                    st.markdown(f'<div class="alert-card alert-error">Passwords do not match.</div>', unsafe_allow_html=True)
                elif len(new_pass) < 6:
                    st.markdown(f'<div class="alert-card alert-error">Password must be at least 6 characters.</div>', unsafe_allow_html=True)
                else:
                    db["users"][new_user] = {
                        "password": hash_pw(new_pass),
                        "role": new_role,
                        "email": new_email,
                        "created": str(datetime.datetime.now())
                    }
                    _log_action("system", f"New user registered: {new_user} as {new_role}")
                    st.markdown(f'<div class="alert-card alert-success">Account created! You can now sign in.</div>', unsafe_allow_html=True)
                    st.session_state.auth_mode = "login"
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;margin-top:24px;font-size:11px;color:{TEXT_MUTED};">
            CollabTech Solutions &bull; DRARS v2.0 &bull; Spring 2026
        </div>
        """, unsafe_allow_html=True)

def render_dashboard():
    db = st.session_state.db
    inds = db["individuals"]
    scns = db["scenarios"]
    collabs = db["collaborations"]
    sims = db["skill_similarities"]
    analyzed = sum(1 for s in scns.values() if s.get("status") == "Analyzed")
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-badge"><span class="pulse-dot"></span> Live Analytics Platform</div>
        <div class="hero-title">Dual-Relationship<br><span>Analysis System</span></div>
        <div class="hero-subtitle">Advanced group formation intelligence powered by collaboration history and skill similarity analysis. Build optimal teams through data-driven insights.</div>
        <div class="hero-stats">
            <div class="hero-stat"><div class="hero-stat-value">{len(inds)}</div><div class="hero-stat-label">Individuals</div></div>
            <div class="hero-stat"><div class="hero-stat-value">{len(scns)}</div><div class="hero-stat-label">Scenarios</div></div>
            <div class="hero-stat"><div class="hero-stat-value">{len(collabs)}</div><div class="hero-stat-label">Collaborations</div></div>
            <div class="hero-stat"><div class="hero-stat-value">{analyzed}</div><div class="hero-stat-label">Analyzed</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    total_collab = sum(v["score"] for v in collabs.values())
    avg_collab = round(total_collab / max(len(collabs), 1), 2)
    total_sim = sum(v["score"] for v in sims.values())
    avg_sim = round(total_sim / max(len(sims), 1), 2)
    skill_set = set()
    for ind in inds.values():
        skill_set.update(ind.get("skills", []))
    with c1:
        st.metric("Total Individuals", len(inds), delta=f"+{min(len(inds), 3)} this week")
    with c2:
        st.metric("Avg Collaboration Score", f"{avg_collab}/10", delta="Active")
    with c3:
        st.metric("Avg Skill Similarity", f"{avg_sim}/10", delta="High")
    with c4:
        st.metric("Unique Skills Mapped", len(skill_set))
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Compatibility Score Distribution</div>
                <span class="tag tag-green">All Pairs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        all_scores = [v["score"] for v in collabs.values()]
        if all_scores:
            bins = [0, 2, 4, 6, 8, 10]
            counts = [0] * 5
            labels = ["0-2", "2-4", "4-6", "6-8", "8-10"]
            for sc in all_scores:
                for i, (lo, hi) in enumerate(zip(bins[:-1], bins[1:])):
                    if lo <= sc < hi or (i == 4 and sc == 10):
                        counts[i] += 1
                        break
            chart_df = pd.DataFrame({"Range": labels, "Pairs": counts})
            st.bar_chart(chart_df.set_index("Range"), color=ACCENT, height=260)
        st.markdown(f"""
        <div class="card card-accent" style="margin-top:0">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Skill Coverage Heatmap</div>
                <span class="tag tag-blue">By Department</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        departments = list(set(v.get("department","Other") for v in inds.values()))
        skills_sample = ["Python", "Machine Learning", "SQL", "Leadership", "UI/UX", "Agile"]
        heatmap_data = {}
        for dept in departments:
            dept_inds = [v for v in inds.values() if v.get("department") == dept]
            row = {}
            for sk in skills_sample:
                count = sum(1 for d in dept_inds if sk in d.get("skills", []))
                row[sk] = count
            heatmap_data[dept] = row
        hdf = pd.DataFrame(heatmap_data).T
        if not hdf.empty:
            st.dataframe(hdf.style.background_gradient(cmap="Greens"), use_container_width=True)
    with col_right:
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Recent Scenarios</div>
                <span class="tag tag-gray">{len(scns)} Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        for sid, scn in list(scns.items())[-4:]:
            status = scn.get("status", "Pending")
            tag_cls = "tag-green" if status == "Analyzed" else "tag-yellow"
            created = scn.get("created", "")[:10]
            st.markdown(f"""
            <div class="scenario-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};">{scn['name']}</div>
                    <span class="tag {tag_cls}">{status}</span>
                </div>
                <div style="font-size:11px;color:{TEXT_MUTED};">{len(scn['individuals'])} individuals &bull; {created} &bull; by {scn.get('created_by','?')}</div>
                <div style="margin-top:10px;">
                    <div class="score-bar-label"><span>Collaboration Weight</span><span>{int(scn['collab_weight']*100)}%</span></div>
                    <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(scn['collab_weight']*100)}%"></div></div>
                    <div class="score-bar-label"><span>Similarity Weight</span><span>{int(scn['similarity_weight']*100)}%</span></div>
                    <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(scn['similarity_weight']*100)}%"></div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card card-accent" style="margin-top:0">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Recent Activity</div>
            </div>
        """, unsafe_allow_html=True)
        logs = db["audit_logs"][-8:][::-1]
        for log in logs:
            ts = log["timestamp"][:16].replace("T", " ")
            st.markdown(f"""
            <div class="log-entry">
                <div class="log-time">{ts}</div>
                <div class="log-user">{log['user']}</div>
                <div class="log-action">{log['action']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card card-accent">
        <div class="card-header">
            <div class="card-title"><div class="card-title-dot"></div>Top Compatible Pairs</div>
            <span class="tag tag-green">By Score</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    pair_data = []
    for key, val in collabs.items():
        i1id = val["i1"]
        i2id = val["i2"]
        if i1id in inds and i2id in inds:
            n1 = inds[i1id]["name"]
            n2 = inds[i2id]["name"]
            sim_key1 = f"{i1id}_{i2id}"
            sim_key2 = f"{i2id}_{i1id}"
            sim_sc = sims.get(sim_key1, sims.get(sim_key2, {})).get("score", 0)
            combined = round(0.6 * val["score"] + 0.4 * sim_sc, 2)
            pair_data.append({
                "Individual A": n1, "Individual B": n2,
                "Collaboration": val["score"],
                "Skill Similarity": sim_sc,
                "Combined Score": combined,
                "Projects": val.get("projects", "-")
            })
    if pair_data:
        pair_df = pd.DataFrame(pair_data).sort_values("Combined Score", ascending=False).head(10)
        st.dataframe(pair_df, use_container_width=True, hide_index=True)

def render_individuals():
    db = st.session_state.db
    inds = db["individuals"]
    role = st.session_state.current_role
    st.markdown(f"""
    <div class="fullwidth-card">
        <div class="section-heading">Individual Profiles</div>
        <div class="section-sub">Manage all registered individuals, their skills, interests, and department affiliations</div>
    </div>
    """, unsafe_allow_html=True)
    search_col, filter_col, action_col = st.columns([3, 2, 2])
    with search_col:
        search = st.text_input("Search", placeholder="Search by name, skill, or interest...", key="ind_search", label_visibility="collapsed")
    with filter_col:
        dept_filter = st.selectbox("Department", ["All"] + list(set(v.get("department", "Other") for v in inds.values())), key="dept_filter", label_visibility="collapsed")
    filtered = {}
    for uid, ind in inds.items():
        match = True
        if search:
            q = search.lower()
            if q not in ind["name"].lower() and not any(q in s.lower() for s in ind.get("skills",[])) and not any(q in i.lower() for i in ind.get("interests",[])):
                match = False
        if dept_filter != "All" and ind.get("department") != dept_filter:
            match = False
        if match:
            filtered[uid] = ind
    st.markdown(f'<div style="font-size:12px;color:{TEXT_MUTED};margin-bottom:16px;">{len(filtered)} of {len(inds)} individuals shown</div>', unsafe_allow_html=True)
    if role == "Admin":
        with st.expander("Add New Individual", expanded=False):
            fc1, fc2 = st.columns(2)
            with fc1:
                new_name = st.text_input("Full Name", key="new_ind_name")
                new_email = st.text_input("Email", key="new_ind_email")
                new_dept = st.selectbox("Department", ["Engineering", "Design", "Analytics", "Management", "Other"], key="new_ind_dept")
            with fc2:
                all_skills = []
                for sk_list in db["skill_categories"].values():
                    all_skills.extend(sk_list)
                new_skills = st.multiselect("Skills", sorted(set(all_skills)), key="new_ind_skills")
                new_interests = st.multiselect("Interests", ["AI Research", "Data Visualization", "Team Collaboration", "Open Source", "Cloud Computing", "Process Optimization"], key="new_ind_interests")
            if st.button("Add Individual", key="add_ind_btn"):
                if not new_name:
                    st.error("Name is required.")
                else:
                    uid = f"IND{len(inds)+1:03d}"
                    db["individuals"][uid] = {
                        "id": uid, "name": new_name, "email": new_email,
                        "department": new_dept, "skills": new_skills,
                        "interests": new_interests, "created": str(datetime.datetime.now())
                    }
                    _log_action(st.session_state.current_user, f"Added individual: {new_name}")
                    st.success(f"Individual {new_name} added successfully.")
                    st.rerun()
    cols_per_row = 3
    ind_list = list(filtered.items())
    for row_start in range(0, len(ind_list), cols_per_row):
        row_items = ind_list[row_start:row_start+cols_per_row]
        cols = st.columns(cols_per_row)
        for col_idx, (uid, ind) in enumerate(row_items):
            with cols[col_idx]:
                skills_html = " ".join([f'<span class="tag tag-green" style="margin:1px;font-size:10px;">{s}</span>' for s in ind.get("skills", [])[:4]])
                if len(ind.get("skills", [])) > 4:
                    skills_html += f'<span class="tag tag-gray" style="margin:1px;font-size:10px;">+{len(ind["skills"])-4}</span>'
                interests_html = " ".join([f'<span class="tag tag-blue" style="margin:1px;font-size:10px;">{i}</span>' for i in ind.get("interests", [])[:2]])
                initials = "".join([p[0] for p in ind["name"].split()[:2]]).upper()
                st.markdown(f"""
                <div class="card" style="min-height:200px;">
                    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
                        <div style="width:44px;height:44px;background:linear-gradient(135deg,{ACCENT2},{ACCENT});border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:{DARK_BG};flex-shrink:0;">{initials}</div>
                        <div>
                            <div style="font-size:14px;font-weight:700;color:{TEXT_PRIMARY};">{ind['name']}</div>
                            <div style="font-size:11px;color:{TEXT_MUTED};">{ind.get('department','—')} &bull; {uid}</div>
                        </div>
                    </div>
                    <div style="font-size:11px;color:{TEXT_MUTED};margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Skills</div>
                    <div style="margin-bottom:10px;">{skills_html}</div>
                    <div style="font-size:11px;color:{TEXT_MUTED};margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Interests</div>
                    <div>{interests_html if interests_html else '<span style="font-size:11px;color:#555;">None listed</span>'}</div>
                    <div style="margin-top:12px;font-size:11px;color:{TEXT_MUTED};">{ind.get('email','')}</div>
                </div>
                """, unsafe_allow_html=True)
                if role == "Admin":
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        if st.button("Edit", key=f"edit_{uid}", use_container_width=True):
                            st.session_state[f"editing_{uid}"] = True
                    with ec2:
                        if st.button("Delete", key=f"del_{uid}", use_container_width=True):
                            del db["individuals"][uid]
                            _log_action(st.session_state.current_user, f"Deleted individual {ind['name']}")
                            st.rerun()
                    if st.session_state.get(f"editing_{uid}"):
                        with st.form(key=f"edit_form_{uid}"):
                            upd_name = st.text_input("Name", value=ind["name"])
                            upd_dept = st.selectbox("Department", ["Engineering","Design","Analytics","Management","Other"], index=["Engineering","Design","Analytics","Management","Other"].index(ind.get("department","Other")) if ind.get("department","Other") in ["Engineering","Design","Analytics","Management","Other"] else 0)
                            all_s = sorted(set(s for sl in db["skill_categories"].values() for s in sl))
                            upd_skills = st.multiselect("Skills", all_s, default=ind.get("skills",[]))
                            save_btn = st.form_submit_button("Save Changes")
                            if save_btn:
                                db["individuals"][uid]["name"] = upd_name
                                db["individuals"][uid]["department"] = upd_dept
                                db["individuals"][uid]["skills"] = upd_skills
                                _log_action(st.session_state.current_user, f"Updated profile: {upd_name}")
                                st.session_state[f"editing_{uid}"] = False
                                st.rerun()

def render_relationships():
    db = st.session_state.db
    inds = db["individuals"]
    collabs = db["collaborations"]
    sims = db["skill_similarities"]
    role = st.session_state.current_role
    st.markdown(f"""
    <div class="fullwidth-card">
        <div class="section-heading">Relationship Management</div>
        <div class="section-sub">Manage collaboration history and skill similarity data between individuals</div>
    </div>
    """, unsafe_allow_html=True)
    tab = st.radio("View", ["Collaboration Data", "Skill Similarity", "Relationship Matrix", "Network View"], horizontal=True, key="rel_tab")
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    if tab == "Collaboration Data":
        if role == "Admin":
            with st.expander("Add / Update Collaboration Record"):
                ac1, ac2 = st.columns(2)
                with ac1:
                    ind_names = {uid: v["name"] for uid, v in inds.items()}
                    sel_i1 = st.selectbox("Individual A", list(ind_names.keys()), format_func=lambda x: ind_names.get(x, x), key="collab_i1")
                    sel_i2 = st.selectbox("Individual B", [k for k in ind_names if k != sel_i1], format_func=lambda x: ind_names.get(x, x), key="collab_i2")
                with ac2:
                    collab_score = st.slider("Collaboration Score", 0.0, 10.0, 5.0, 0.1, key="collab_score_inp")
                    collab_projects = st.number_input("Number of Projects", 1, 50, 2, key="collab_proj_inp")
                if st.button("Save Collaboration", key="save_collab_btn"):
                    if sel_i1 and sel_i2 and sel_i1 != sel_i2:
                        key = f"{sel_i1}_{sel_i2}"
                        db["collaborations"][key] = {
                            "i1": sel_i1, "i2": sel_i2,
                            "score": collab_score, "projects": collab_projects,
                            "last_collab": str(datetime.datetime.now())
                        }
                        _log_action(st.session_state.current_user, f"Added collaboration: {ind_names[sel_i1]} & {ind_names[sel_i2]}")
                        st.success("Collaboration saved.")
                        st.rerun()
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Collaboration Records</div>
                <span class="tag tag-green">{len(collabs)} Records</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        rows = []
        for key, val in collabs.items():
            if val["i1"] in inds and val["i2"] in inds:
                rows.append({
                    "ID": key, "Individual A": inds[val["i1"]]["name"],
                    "Individual B": inds[val["i2"]]["name"],
                    "Score": val["score"], "Projects": val.get("projects", "-"),
                    "Last Collaboration": str(val.get("last_collab",""))[:10]
                })
        if rows:
            cdf = pd.DataFrame(rows).sort_values("Score", ascending=False)
            st.dataframe(cdf.drop(columns=["ID"]), use_container_width=True, hide_index=True)
            if role == "Admin":
                del_key = st.text_input("Enter Collaboration ID to delete (from table above):", key="del_collab_key")
                if st.button("Delete Record", key="del_collab_btn"):
                    if del_key in db["collaborations"]:
                        del db["collaborations"][del_key]
                        _log_action(st.session_state.current_user, f"Deleted collaboration: {del_key}")
                        st.success("Deleted.")
                        st.rerun()
    elif tab == "Skill Similarity":
        if role == "Admin":
            with st.expander("Add / Update Skill Similarity"):
                sc1, sc2 = st.columns(2)
                with sc1:
                    ind_names = {uid: v["name"] for uid, v in inds.items()}
                    ss_i1 = st.selectbox("Individual A", list(ind_names.keys()), format_func=lambda x: ind_names.get(x,x), key="sim_i1")
                    ss_i2 = st.selectbox("Individual B", [k for k in ind_names if k != ss_i1], format_func=lambda x: ind_names.get(x,x), key="sim_i2")
                with sc2:
                    sim_score_inp = st.slider("Similarity Score (0-10)", 0.0, 10.0, 5.0, 0.1, key="sim_score_inp")
                    if st.button("Auto-Calculate from Skills", key="auto_calc_sim"):
                        s1 = set(inds.get(ss_i1,{}).get("skills",[]))
                        s2 = set(inds.get(ss_i2,{}).get("skills",[]))
                        auto = round(len(s1 & s2) / max(len(s1 | s2), 1) * 10, 2)
                        st.info(f"Calculated similarity: {auto}/10")
                if st.button("Save Similarity", key="save_sim_btn"):
                    key = f"{ss_i1}_{ss_i2}"
                    db["skill_similarities"][key] = {"i1": ss_i1, "i2": ss_i2, "score": sim_score_inp}
                    _log_action(st.session_state.current_user, f"Updated skill similarity: {ind_names.get(ss_i1,ss_i1)} & {ind_names.get(ss_i2,ss_i2)}")
                    st.success("Saved.")
                    st.rerun()
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Skill Similarity Records</div>
                <span class="tag tag-blue">{len(sims)} Pairs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        sim_rows = []
        for key, val in sims.items():
            if val["i1"] in inds and val["i2"] in inds:
                sim_rows.append({
                    "ID": key,
                    "Individual A": inds[val["i1"]]["name"],
                    "Individual B": inds[val["i2"]]["name"],
                    "Similarity Score": val["score"]
                })
        if sim_rows:
            sdf = pd.DataFrame(sim_rows).sort_values("Similarity Score", ascending=False)
            st.dataframe(sdf.drop(columns=["ID"]), use_container_width=True, hide_index=True)
    elif tab == "Relationship Matrix":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Combined Compatibility Matrix</div>
                <span class="tag tag-yellow">Interactive</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ind_ids = list(inds.keys())[:12]
        ind_names_short = [inds[i]["name"].split()[0] for i in ind_ids]
        matrix_data = []
        for i1 in ind_ids:
            row = []
            for i2 in ind_ids:
                if i1 == i2:
                    row.append(10.0)
                else:
                    sc = compute_compatibility(i1, i2, 0.6, 0.4)
                    row.append(sc)
            matrix_data.append(row)
        mdf = pd.DataFrame(matrix_data, index=ind_names_short, columns=ind_names_short)
        st.dataframe(mdf.style.background_gradient(cmap="Greens", vmin=0, vmax=10).format("{:.1f}"), use_container_width=True)
    elif tab == "Network View":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Relationship Network Visualization</div>
                <span class="tag tag-green">SVG Graph</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ind_ids = list(inds.keys())[:12]
        n = len(ind_ids)
        cx, cy, r = 400, 280, 220
        angles = [2 * math.pi * i / n for i in range(n)]
        positions = {uid: (cx + r * math.cos(a - math.pi/2), cy + r * math.sin(a - math.pi/2)) for uid, a in zip(ind_ids, angles)}
        edges_svg = ""
        threshold = 4.0
        for key, val in collabs.items():
            i1, i2 = val["i1"], val["i2"]
            if i1 in positions and i2 in positions and val["score"] >= threshold:
                x1, y1 = positions[i1]
                x2, y2 = positions[i2]
                opacity = min(val["score"] / 10.0, 0.9)
                width = 1 + val["score"] / 4
                edges_svg += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{ACCENT}" stroke-width="{width:.1f}" stroke-opacity="{opacity:.2f}"/>'
        nodes_svg = ""
        for uid, (x, y) in positions.items():
            name = inds[uid]["name"].split()[0]
            dept = inds[uid].get("department","")
            color = {"Engineering": ACCENT, "Design": INFO, "Analytics": WARNING, "Management": DANGER}.get(dept, "#888")
            nodes_svg += f'''
            <circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-width="2"/>
            <text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" dominant-baseline="middle" fill="{color}" font-size="10" font-weight="700" font-family="Inter">{name}</text>
            '''
        legend_svg = ""
        dept_colors = {"Engineering": ACCENT, "Design": INFO, "Analytics": WARNING, "Management": DANGER}
        for i, (dept, color) in enumerate(dept_colors.items()):
            legend_svg += f'<circle cx="20" cy="{i*18+10}" r="6" fill="{color}" fill-opacity="0.3" stroke="{color}" stroke-width="1.5"/>'
            legend_svg += f'<text x="32" y="{i*18+14}" fill="#888" font-size="10" font-family="Inter">{dept}</text>'
        svg_html = f"""
        <svg viewBox="0 0 800 560" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#0d0d0d;border-radius:6px;border:1px solid #1a1a1a;">
            <defs>
                <radialGradient id="bg_grad" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#0d1a00" stop-opacity="0.3"/>
                    <stop offset="100%" stop-color="#0a0a0a" stop-opacity="0"/>
                </radialGradient>
            </defs>
            <rect width="800" height="560" fill="url(#bg_grad)"/>
            {edges_svg}
            {nodes_svg}
            <g transform="translate(680, 20)">
                <rect x="-10" y="-10" width="130" height="100" rx="4" fill="#111" fill-opacity="0.9" stroke="#1a1a1a"/>
                <text x="0" y="0" fill="#76b900" font-size="10" font-weight="700" font-family="Inter">DEPARTMENTS</text>
                <g transform="translate(0,10)">{legend_svg}</g>
            </g>
            <text x="400" y="540" text-anchor="middle" fill="#333" font-size="10" font-family="Inter">Edges shown for score >= {threshold} | Node size = individual</text>
        </svg>
        """
        st.markdown(svg_html, unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:11px;color:{TEXT_MUTED};margin-top:8px;">Network displays top-strength collaboration edges. Stronger edges appear thicker and brighter.</div>', unsafe_allow_html=True)

def render_scenarios():
    db = st.session_state.db
    inds = db["individuals"]
    scns = db["scenarios"]
    st.markdown(f"""
    <div class="fullwidth-card">
        <div class="section-heading">Analysis Scenarios</div>
        <div class="section-sub">Create, configure, save, and compare multi-individual analysis scenarios</div>
    </div>
    """, unsafe_allow_html=True)
    scenario_tab = st.radio("", ["All Scenarios", "Create New", "Compare Scenarios"], horizontal=True, key="scn_tab")
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    if scenario_tab == "All Scenarios":
        if not scns:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:60px;">
                <div style="font-size:40px;opacity:0.2;margin-bottom:16px;">&#9635;</div>
                <div style="font-size:16px;color:{TEXT_SECONDARY};font-weight:600;">No scenarios created yet</div>
                <div style="font-size:12px;color:{TEXT_MUTED};margin-top:8px;">Switch to 'Create New' tab to get started</div>
            </div>
            """, unsafe_allow_html=True)
        for sid, scn in scns.items():
            status = scn.get("status", "Pending")
            tag_cls = "tag-green" if status == "Analyzed" else "tag-yellow"
            member_names = [inds[i]["name"] for i in scn["individuals"] if i in inds]
            names_preview = ", ".join(member_names[:4])
            if len(member_names) > 4:
                names_preview += f" +{len(member_names)-4} more"
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="flex:1;">
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                            <div style="font-size:16px;font-weight:800;color:{TEXT_PRIMARY};">{scn['name']}</div>
                            <span class="tag {tag_cls}">{status}</span>
                        </div>
                        <div style="font-size:12px;color:{TEXT_MUTED};margin-bottom:10px;">{scn.get('description','No description')}</div>
                        <div style="font-size:11px;color:{TEXT_SECONDARY};">Members: {names_preview}</div>
                        <div style="margin-top:12px;max-width:400px;">
                            <div class="score-bar-label"><span>Collaboration Weight</span><span>{int(scn['collab_weight']*100)}%</span></div>
                            <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(scn['collab_weight']*100)}%"></div></div>
                            <div class="score-bar-label"><span>Similarity Weight</span><span>{int(scn['similarity_weight']*100)}%</span></div>
                            <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(scn['similarity_weight']*100)}%"></div></div>
                        </div>
                    </div>
                    <div style="font-size:11px;color:{TEXT_MUTED};text-align:right;">
                        <div>{sid}</div>
                        <div>by {scn.get('created_by','?')}</div>
                        <div>{scn.get('created','')[:10]}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            bc1, bc2, bc3, bc4 = st.columns([2, 2, 2, 1])
            with bc1:
                if st.button("Run Analysis", key=f"run_scn_{sid}", use_container_width=True):
                    results = run_analysis(sid)
                    st.session_state.analysis_results[sid] = results
                    st.session_state.selected_scenario = sid
                    st.session_state.page = "Analysis"
                    st.rerun()
            with bc2:
                if st.button("Edit Scenario", key=f"edit_scn_{sid}", use_container_width=True):
                    st.session_state[f"edit_scn_open_{sid}"] = True
            with bc3:
                if st.button("Delete", key=f"del_scn_{sid}", use_container_width=True):
                    del db["scenarios"][sid]
                    _log_action(st.session_state.current_user, f"Deleted scenario: {scn['name']}")
                    st.rerun()
            if st.session_state.get(f"edit_scn_open_{sid}"):
                with st.form(key=f"edit_scn_form_{sid}"):
                    eu_name = st.text_input("Scenario Name", value=scn["name"])
                    eu_desc = st.text_area("Description", value=scn.get("description",""))
                    all_ind = {uid: v["name"] for uid, v in inds.items()}
                    eu_inds = st.multiselect("Individuals", list(all_ind.keys()), default=scn["individuals"], format_func=lambda x: all_ind.get(x,x))
                    eu_cw = st.slider("Collaboration Weight", 0.0, 1.0, scn["collab_weight"], 0.05)
                    eu_sw = round(1 - eu_cw, 2)
                    st.info(f"Similarity Weight: {eu_sw}")
                    save_edit = st.form_submit_button("Save Changes")
                    if save_edit:
                        db["scenarios"][sid]["name"] = eu_name
                        db["scenarios"][sid]["description"] = eu_desc
                        db["scenarios"][sid]["individuals"] = eu_inds
                        db["scenarios"][sid]["collab_weight"] = eu_cw
                        db["scenarios"][sid]["similarity_weight"] = eu_sw
                        db["scenarios"][sid]["status"] = "Pending"
                        _log_action(st.session_state.current_user, f"Updated scenario: {eu_name}")
                        st.session_state[f"edit_scn_open_{sid}"] = False
                        st.rerun()
    elif scenario_tab == "Create New":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>New Analysis Scenario</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.form("create_scenario_form"):
            cr1, cr2 = st.columns(2)
            with cr1:
                scn_name = st.text_input("Scenario Name", placeholder="e.g., Q2 Engineering Team")
                scn_desc = st.text_area("Description", placeholder="Describe the goal of this scenario...")
                all_ind = {uid: v["name"] for uid, v in inds.items()}
                scn_inds = st.multiselect("Select Individuals", list(all_ind.keys()), format_func=lambda x: all_ind.get(x,x))
            with cr2:
                scn_cw = st.slider("Collaboration Weight", 0.0, 1.0, 0.6, 0.05, help="Weight given to collaboration history")
                scn_sw = round(1 - scn_cw, 2)
                st.markdown(f'<div style="font-size:12px;color:{ACCENT};margin-top:4px;">Skill Similarity Weight: {scn_sw}</div>', unsafe_allow_html=True)
                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
                scn_preview = st.checkbox("Preview compatibility before saving", value=False)
            submitted = st.form_submit_button("Create Scenario")
            if submitted:
                if not scn_name:
                    st.error("Scenario name is required.")
                elif len(scn_inds) < 2:
                    st.error("Select at least 2 individuals.")
                else:
                    sid = f"SCN{len(scns)+1:03d}"
                    db["scenarios"][sid] = {
                        "id": sid, "name": scn_name, "description": scn_desc,
                        "individuals": scn_inds, "collab_weight": scn_cw,
                        "similarity_weight": scn_sw, "created_by": st.session_state.current_user,
                        "created": str(datetime.datetime.now()), "status": "Pending"
                    }
                    _log_action(st.session_state.current_user, f"Created scenario: {scn_name}")
                    st.success(f"Scenario '{scn_name}' created with ID {sid}.")
                    st.rerun()
    elif scenario_tab == "Compare Scenarios":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Scenario Comparison</div>
                <span class="tag tag-blue">Side by Side</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        scn_options = {sid: v["name"] for sid, v in scns.items()}
        comp_sel = st.multiselect("Select scenarios to compare (2-4)", list(scn_options.keys()), max_selections=4, format_func=lambda x: scn_options.get(x,x), key="comp_sel")
        if len(comp_sel) >= 2:
            comp_cols = st.columns(len(comp_sel))
            for i, sid in enumerate(comp_sel):
                scn = scns[sid]
                status = scn.get("status","Pending")
                tag_cls = "tag-green" if status == "Analyzed" else "tag-yellow"
                member_names = [inds[m]["name"] for m in scn["individuals"] if m in inds]
                with comp_cols[i]:
                    st.markdown(f"""
                    <div class="card">
                        <div style="font-size:13px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:8px;">{scn['name']}</div>
                        <span class="tag {tag_cls}">{status}</span>
                        <div style="margin-top:14px;">
                            <div class="score-bar-label"><span>Collab Weight</span><span>{int(scn['collab_weight']*100)}%</span></div>
                            <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(scn['collab_weight']*100)}%"></div></div>
                            <div class="score-bar-label"><span>Sim Weight</span><span>{int(scn['similarity_weight']*100)}%</span></div>
                            <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(scn['similarity_weight']*100)}%"></div></div>
                        </div>
                        <div style="margin-top:12px;">
                            <div style="font-size:11px;color:{TEXT_MUTED};margin-bottom:6px;">MEMBERS ({len(member_names)})</div>
                            {''.join([f'<div class="member-chip" style="margin-bottom:4px;display:inline-flex;"><div class="member-chip-dot"></div>{n}</div><br>' for n in member_names[:6]])}
                            {f'<div style="font-size:10px;color:#555;margin-top:4px;">+{len(member_names)-6} more</div>' if len(member_names) > 6 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Run Analysis", key=f"comp_run_{sid}", use_container_width=True):
                        results = run_analysis(sid)
                        st.session_state.analysis_results[sid] = results
                        st.success(f"Analysis complete for {scn['name']}")
        else:
            st.markdown(f'<div style="color:{TEXT_MUTED};font-size:13px;padding:20px 0;">Select at least 2 scenarios to compare them side by side.</div>', unsafe_allow_html=True)

def render_analysis():
    db = st.session_state.db
    inds = db["individuals"]
    scns = db["scenarios"]
    st.markdown(f"""
    <div class="fullwidth-card">
        <div class="section-heading">Relationship Analysis</div>
        <div class="section-sub">Run, view, and refine compatibility analysis and group recommendations</div>
    </div>
    """, unsafe_allow_html=True)
    scn_options = {sid: v["name"] for sid, v in scns.items()}
    if not scn_options:
        st.markdown(f'<div style="color:{TEXT_MUTED};padding:40px 0;text-align:center;">No scenarios found. Create a scenario first.</div>', unsafe_allow_html=True)
        return
    sel_sid = st.selectbox("Select Scenario", list(scn_options.keys()), format_func=lambda x: scn_options.get(x,x), key="analysis_scn_sel")
    scn = scns[sel_sid]
    sc1, sc2 = st.columns([3, 1])
    with sc1:
        st.markdown(f"""
        <div class="card">
            <div style="display:flex;gap:32px;align-items:center;">
                <div><div class="metric-value">{len(scn['individuals'])}</div><div class="metric-label">Individuals</div></div>
                <div><div class="metric-value">{int(scn['collab_weight']*100)}%</div><div class="metric-label">Collab Weight</div></div>
                <div><div class="metric-value">{int(scn['similarity_weight']*100)}%</div><div class="metric-label">Sim Weight</div></div>
                <div><div class="metric-value" style="font-size:20px;">{scn.get('status','Pending')}</div><div class="metric-label">Status</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with sc2:
        if st.button("Run Full Analysis", key="run_analysis_main", use_container_width=True):
            with st.spinner("Computing compatibility scores..."):
                results = run_analysis(sel_sid)
                st.session_state.analysis_results[sel_sid] = results
                st.session_state.selected_scenario = sel_sid
            st.rerun()
    if sel_sid in st.session_state.analysis_results:
        results = st.session_state.analysis_results[sel_sid]
        groups = results["groups"]
        conflicts = results["conflicts"]
        tabs = st.radio("", ["Recommended Groups", "Conflict Alerts", "Simulate & Filter", "Compatibility Scores", "Annotate Results"], horizontal=True, key="analysis_inner_tab")
        if tabs == "Recommended Groups":
            if not groups:
                st.markdown(f'<div style="color:{TEXT_MUTED};padding:40px 0;text-align:center;">No compatible groups found. Try lowering the minimum score threshold in Admin settings.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
                    <div class="metric-card" style="padding:14px 20px;flex:1;">
                        <div class="metric-value">{len(groups)}</div>
                        <div class="metric-label">Groups Identified</div>
                    </div>
                    <div class="metric-card" style="padding:14px 20px;flex:1;">
                        <div class="metric-value">{groups[0]['avg_score'] if groups else 0}</div>
                        <div class="metric-label">Top Group Score</div>
                    </div>
                    <div class="metric-card" style="padding:14px 20px;flex:1;">
                        <div class="metric-value">{round(sum(g['avg_score'] for g in groups)/len(groups),2)}</div>
                        <div class="metric-label">Average Group Score</div>
                    </div>
                    <div class="metric-card" style="padding:14px 20px;flex:1;">
                        <div class="metric-value">{len(conflicts)}</div>
                        <div class="metric-label">Conflicts Detected</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                score_data = {"Group": [f"Group {g['rank']}" for g in groups], "Score": [g["avg_score"] for g in groups]}
                st.bar_chart(pd.DataFrame(score_data).set_index("Group"), color=ACCENT, height=200)
                for grp in groups:
                    member_names = [inds[m]["name"] for m in grp["members"] if m in inds]
                    all_skills = []
                    for m in grp["members"]:
                        if m in inds:
                            all_skills.extend(inds[m].get("skills",[]))
                    unique_skills = list(set(all_skills))
                    score_pct = min(grp["avg_score"] / 10.0, 1.0)
                    score_color = ACCENT if grp["avg_score"] >= 6 else WARNING if grp["avg_score"] >= 4 else DANGER
                    skill_tags = " ".join([f'<span class="tag tag-green" style="margin:1px;font-size:10px;">{s}</span>' for s in unique_skills[:6]])
                    member_chips = " ".join([f'<span class="member-chip"><span class="member-chip-dot"></span>{n}</span>' for n in member_names])
                    st.markdown(f"""
                    <div class="group-card">
                        <div class="group-rank">
                            <div class="rank-badge">#{grp['rank']}</div>
                            <div>
                                <div style="font-size:15px;font-weight:700;color:{TEXT_PRIMARY};">Group {grp['rank']}</div>
                                <div style="font-size:11px;color:{TEXT_MUTED};">{len(grp['members'])} members &bull; {grp['pair_count']} relationship pairs</div>
                            </div>
                            <div style="margin-left:auto;text-align:right;">
                                <div style="font-size:26px;font-weight:900;color:{score_color};">{grp['avg_score']}</div>
                                <div style="font-size:10px;color:{TEXT_MUTED};">Avg Score</div>
                            </div>
                        </div>
                        <div class="group-members">{member_chips}</div>
                        <div class="score-bar-container">
                            <div class="score-bar-label"><span>Compatibility Rating</span><span>{grp['avg_score']}/10</span></div>
                            <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(score_pct*100)}%"></div></div>
                        </div>
                        <div style="margin-top:10px;">
                            <div style="font-size:10px;color:{TEXT_MUTED};margin-bottom:4px;text-transform:uppercase;">Combined Skills</div>
                            {skill_tags}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        elif tabs == "Conflict Alerts":
            if not conflicts:
                st.markdown(f'<div class="alert-card alert-success">No significant conflicts detected in this scenario.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-card alert-warning">{len(conflicts)} potential conflict(s) detected. Review pairs with low compatibility.</div>', unsafe_allow_html=True)
                for conf in conflicts:
                    st.markdown(f"""
                    <div class="conflict-card">
                        <div class="conflict-title">Low Compatibility: {conf['n1']} & {conf['n2']}</div>
                        <div style="display:flex;gap:20px;align-items:center;">
                            <div>Score: <span style="color:{DANGER};font-weight:700;">{conf['score']}</span>/10</div>
                            <div>Reason: {conf['reason']}</div>
                        </div>
                        <div style="margin-top:8px;">
                            <div class="score-bar-track"><div class="score-bar-fill" style="width:{int(conf['score']*10)}%;background:linear-gradient(90deg,#7f0000,{DANGER});"></div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        elif tabs == "Simulate & Filter":
            st.markdown(f"""
            <div class="card card-accent">
                <div class="card-header">
                    <div class="card-title"><div class="card-title-dot"></div>Simulation Controls</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            sim1, sim2 = st.columns(2)
            with sim1:
                sim_cw = st.slider("Collaboration Weight", 0.0, 1.0, scn["collab_weight"], 0.05, key="sim_cw")
                sim_sw = round(1 - sim_cw, 2)
                st.markdown(f'<div style="font-size:12px;color:{ACCENT};">Similarity Weight: {sim_sw}</div>', unsafe_allow_html=True)
                sim_thresh = st.slider("Min Compatibility Threshold", 1.0, 8.0, db["rules"]["min_score_threshold"], 0.5, key="sim_thresh")
            with sim2:
                filter_skill = st.multiselect("Filter by Skill", sorted(set(s for v in inds.values() for s in v.get("skills",[]))), key="sim_skill_filter")
                filter_dept = st.multiselect("Filter by Department", list(set(v.get("department","Other") for v in inds.values())), key="sim_dept_filter")
            if st.button("Run Simulation", key="run_sim_btn", use_container_width=True):
                sim_inds = scn["individuals"].copy()
                if filter_skill:
                    sim_inds = [i for i in sim_inds if i in inds and any(sk in inds[i].get("skills",[]) for sk in filter_skill)]
                if filter_dept:
                    sim_inds = [i for i in sim_inds if i in inds and inds[i].get("department") in filter_dept]
                if len(sim_inds) < 2:
                    st.warning("Fewer than 2 individuals match the filters.")
                else:
                    tmp_matrix = {}
                    for ii in range(len(sim_inds)):
                        for jj in range(ii+1, len(sim_inds)):
                            sc = compute_compatibility(sim_inds[ii], sim_inds[jj], sim_cw, sim_sw)
                            tmp_matrix[(sim_inds[ii], sim_inds[jj])] = sc
                    adjacency = defaultdict(list)
                    for (i1, i2), sc in tmp_matrix.items():
                        if sc >= sim_thresh:
                            adjacency[i1].append((i2, sc))
                            adjacency[i2].append((i1, sc))
                    visited = set()
                    sim_groups = []
                    for ind in sim_inds:
                        if ind not in visited:
                            queue = [ind]
                            cluster = []
                            while queue:
                                node = queue.pop(0)
                                if node in visited:
                                    continue
                                visited.add(node)
                                cluster.append(node)
                                for nb, _ in adjacency[node]:
                                    if nb not in visited:
                                        queue.append(nb)
                            if len(cluster) >= 2:
                                sim_groups.append(cluster)
                    st.markdown(f'<div style="color:{ACCENT};font-size:13px;font-weight:700;margin-bottom:12px;">{len(sim_groups)} simulated group(s) found</div>', unsafe_allow_html=True)
                    for gi, grp in enumerate(sim_groups):
                        names = [inds[m]["name"] for m in grp if m in inds]
                        scores = [tmp_matrix.get((grp[ii],grp[jj]),0) for ii in range(len(grp)) for jj in range(ii+1,len(grp))]
                        avg = round(sum(scores)/max(len(scores),1),2)
                        st.markdown(f"""
                        <div class="group-card">
                            <div style="font-weight:700;color:{TEXT_PRIMARY};margin-bottom:8px;">Simulated Group {gi+1} &mdash; Avg Score: <span style="color:{ACCENT};">{avg}</span></div>
                            <div class="group-members">{''.join([f'<span class="member-chip"><span class="member-chip-dot"></span>{n}</span>' for n in names])}</div>
                        </div>
                        """, unsafe_allow_html=True)
        elif tabs == "Compatibility Scores":
            st.markdown(f"""
            <div class="card card-accent">
                <div class="card-header">
                    <div class="card-title"><div class="card-title-dot"></div>Full Pairwise Compatibility Matrix</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            ind_ids = scn["individuals"]
            ind_names_map = {uid: inds[uid]["name"].split()[0] if uid in inds else uid for uid in ind_ids}
            rows = []
            for i1 in ind_ids:
                row = {}
                for i2 in ind_ids:
                    if i1 == i2:
                        row[ind_names_map[i2]] = 10.0
                    else:
                        row[ind_names_map[i2]] = compute_compatibility(i1, i2, scn["collab_weight"], scn["similarity_weight"])
                rows.append(row)
            df_mat = pd.DataFrame(rows, index=[ind_names_map[i] for i in ind_ids])
            st.dataframe(df_mat.style.background_gradient(cmap="Greens", vmin=0, vmax=10).format("{:.2f}"), use_container_width=True)
            pair_list = []
            for (i1, i2), sc in results["matrix"].items():
                i1_id, i2_id = i1.split("_")[0], "_".join(i1.split("_")[1:])
                if i1_id in inds and i2_id in inds and i1_id < i2_id:
                    pair_list.append({"Pair": f"{inds[i1_id]['name']} — {inds[i2_id]['name']}", "Score": sc})
            if pair_list:
                pair_df = pd.DataFrame(pair_list).sort_values("Score", ascending=False).head(15)
                st.markdown(f'<div style="margin-top:20px;font-size:13px;font-weight:700;color:{TEXT_PRIMARY};">Top Compatible Pairs</div>', unsafe_allow_html=True)
                st.bar_chart(pair_df.set_index("Pair"), color=ACCENT, height=280)
        elif tabs == "Annotate Results":
            st.markdown(f"""
            <div class="card card-accent">
                <div class="card-header">
                    <div class="card-title"><div class="card-title-dot"></div>Annotations & Notes</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            annot_key = f"annot_{sel_sid}"
            existing = db["annotations"].get(annot_key, [])
            for ann in existing:
                st.markdown(f"""
                <div class="annotation-chip">
                    <div class="annotation-author">{ann['user']}</div>
                    <div style="color:{TEXT_MUTED};font-size:10px;white-space:nowrap;">{ann['time'][:16]}</div>
                    <div>{ann['text']}</div>
                </div>
                """, unsafe_allow_html=True)
            ann_text = st.text_area("Add annotation or note", placeholder="Type your observation about this analysis...", key="ann_text_inp")
            if st.button("Add Annotation", key="add_ann_btn", use_container_width=True):
                if ann_text.strip():
                    if annot_key not in db["annotations"]:
                        db["annotations"][annot_key] = []
                    db["annotations"][annot_key].append({
                        "user": st.session_state.current_user,
                        "time": str(datetime.datetime.now()),
                        "text": ann_text.strip()
                    })
                    _log_action(st.session_state.current_user, f"Added annotation to scenario {sel_sid}")
                    st.success("Annotation added.")
                    st.rerun()
    else:
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:60px;">
            <div style="font-size:40px;opacity:0.15;margin-bottom:16px;">&#9635;</div>
            <div style="font-size:15px;color:{TEXT_SECONDARY};font-weight:600;margin-bottom:8px;">No analysis run yet</div>
            <div style="font-size:12px;color:{TEXT_MUTED};">Click 'Run Full Analysis' to generate compatibility scores and group recommendations</div>
        </div>
        """, unsafe_allow_html=True)

def render_reports():
    db = st.session_state.db
    inds = db["individuals"]
    scns = db["scenarios"]
    st.markdown(f"""
    <div class="fullwidth-card">
        <div class="section-heading">Reports & Exports</div>
        <div class="section-sub">Generate, export, and visualize analysis reports in multiple formats</div>
    </div>
    """, unsafe_allow_html=True)
    rpt_tab = st.radio("", ["Summary Report", "Export CSV", "Export PDF", "Visual Diagrams", "Search Individuals"], horizontal=True, key="rpt_tab")
    if rpt_tab == "Summary Report":
        sel_scn = st.selectbox("Select Scenario", list(scns.keys()), format_func=lambda x: scns[x]["name"], key="rpt_scn_sel") if scns else None
        if sel_scn and sel_scn in st.session_state.analysis_results:
            results = st.session_state.analysis_results[sel_scn]
            scn = scns[sel_scn]
            groups = results["groups"]
            st.markdown(f"""
            <div class="card card-accent">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                    <div>
                        <div style="font-size:20px;font-weight:900;color:{TEXT_PRIMARY};margin-bottom:4px;">{scn['name']}</div>
                        <div style="font-size:12px;color:{TEXT_MUTED};">{scn.get('description','')} | Generated: {str(datetime.datetime.now())[:16]}</div>
                    </div>
                    <div style="display:flex;gap:10px;">
                        <span class="tag tag-green">ANALYZED</span>
                    </div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px;">
                    <div class="metric-card">
                        <div class="metric-value">{len(scn['individuals'])}</div>
                        <div class="metric-label">Individuals</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(groups)}</div>
                        <div class="metric-label">Groups</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{groups[0]['avg_score'] if groups else 'N/A'}</div>
                        <div class="metric-label">Top Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(results['conflicts'])}</div>
                        <div class="metric-label">Conflicts</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            for grp in groups[:5]:
                member_names = [inds[m]["name"] for m in grp["members"] if m in inds]
                st.markdown(f"""
                <div class="card" style="padding:16px 20px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-weight:700;color:{TEXT_PRIMARY};">Group #{grp['rank']}: {', '.join(member_names)}</div>
                        <div style="font-size:18px;font-weight:800;color:{ACCENT};">{grp['avg_score']}/10</div>
                    </div>
                    <div style="margin-top:8px;"><div class="score-bar-track"><div class="score-bar-fill" style="width:{int(grp['avg_score']*10)}%"></div></div></div>
                    <div style="margin-top:8px;font-size:11px;color:{TEXT_MUTED};">{len(grp['members'])} members | {grp['pair_count']} relationship pairs | Total score: {grp['total_score']}</div>
                </div>
                """, unsafe_allow_html=True)
        elif sel_scn:
            st.info("Run the analysis for this scenario first to generate a report.")
    elif rpt_tab == "Export CSV":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>CSV Export</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        export_type = st.radio("Select data to export", ["Individuals", "Collaborations", "Skill Similarities", "Group Recommendations"], horizontal=True, key="csv_export_type")
        if export_type == "Individuals":
            rows = [{"ID": uid, "Name": v["name"], "Department": v.get("department",""), "Skills": ";".join(v.get("skills",[])), "Interests": ";".join(v.get("interests",[])), "Email": v.get("email","")} for uid, v in inds.items()]
            df = pd.DataFrame(rows)
        elif export_type == "Collaborations":
            rows = [{"I1": v["i1"], "I1_Name": inds.get(v["i1"],{}).get("name",""), "I2": v["i2"], "I2_Name": inds.get(v["i2"],{}).get("name",""), "Score": v["score"], "Projects": v.get("projects","")} for v in db["collaborations"].values()]
            df = pd.DataFrame(rows)
        elif export_type == "Skill Similarities":
            rows = [{"I1": v["i1"], "I1_Name": inds.get(v["i1"],{}).get("name",""), "I2": v["i2"], "I2_Name": inds.get(v["i2"],{}).get("name",""), "Score": v["score"]} for v in db["skill_similarities"].values()]
            df = pd.DataFrame(rows)
        else:
            rows = []
            for sid, results in st.session_state.analysis_results.items():
                for grp in results.get("groups",[]):
                    for m in grp["members"]:
                        rows.append({"Scenario": scns.get(sid,{}).get("name",""), "Group_Rank": grp["rank"], "Individual_ID": m, "Name": inds.get(m,{}).get("name",""), "Avg_Score": grp["avg_score"]})
            df = pd.DataFrame(rows)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(f"Download {export_type} CSV", csv_buf.getvalue(), f"drars_{export_type.lower().replace(' ','_')}.csv", "text/csv", key="dl_csv_btn", use_container_width=True)
            _log_action(st.session_state.current_user, f"Exported {export_type} as CSV")
        else:
            st.info("No data available for selected export type.")
    elif rpt_tab == "Export PDF":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>PDF Report Generation</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        sel_scn_pdf = st.selectbox("Select Scenario", list(scns.keys()), format_func=lambda x: scns.get(x,{}).get("name",x), key="pdf_scn_sel") if scns else None
        include_matrix = st.checkbox("Include compatibility matrix", value=True)
        include_conflicts = st.checkbox("Include conflict alerts", value=True)
        include_groups = st.checkbox("Include group recommendations", value=True)
        if st.button("Generate PDF Report", key="gen_pdf_btn", use_container_width=True):
            if sel_scn_pdf and sel_scn_pdf in st.session_state.analysis_results:
                results = st.session_state.analysis_results[sel_scn_pdf]
                scn = scns[sel_scn_pdf]
                lines = []
                lines.append("DUAL-RELATIONSHIP ANALYSIS AND RECOMMENDATION SYSTEM")
                lines.append("="*60)
                lines.append(f"Report for Scenario: {scn['name']}")
                lines.append(f"Generated: {str(datetime.datetime.now())[:19]}")
                lines.append(f"Individuals: {len(scn['individuals'])}")
                lines.append(f"Collaboration Weight: {scn['collab_weight']}")
                lines.append(f"Similarity Weight: {scn['similarity_weight']}")
                lines.append("")
                if include_groups:
                    lines.append("GROUP RECOMMENDATIONS")
                    lines.append("-"*40)
                    for grp in results["groups"]:
                        names = [inds.get(m,{}).get("name",m) for m in grp["members"]]
                        lines.append(f"Group #{grp['rank']}: {', '.join(names)}")
                        lines.append(f"  Average Score: {grp['avg_score']}")
                        lines.append(f"  Total Score: {grp['total_score']}")
                        lines.append("")
                if include_conflicts:
                    lines.append("CONFLICT ALERTS")
                    lines.append("-"*40)
                    for conf in results["conflicts"]:
                        lines.append(f"Conflict: {conf['n1']} & {conf['n2']} - Score: {conf['score']}")
                    lines.append("")
                pdf_text = "\n".join(lines)
                st.download_button("Download Report (TXT)", pdf_text, f"drars_report_{sel_scn_pdf}.txt", "text/plain", key="dl_pdf_btn", use_container_width=True)
                _log_action(st.session_state.current_user, f"Generated PDF report for {scn['name']}")
                st.success("Report ready for download.")
            else:
                st.warning("Run analysis on the selected scenario first.")
    elif rpt_tab == "Visual Diagrams":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Visual Analytics</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        with v1:
            skill_counts = {}
            for ind in inds.values():
                for sk in ind.get("skills",[]):
                    skill_counts[sk] = skill_counts.get(sk,0) + 1
            sk_df = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Count"]).sort_values("Count", ascending=False).head(12)
            st.markdown(f'<div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">Top Skills Distribution</div>', unsafe_allow_html=True)
            st.bar_chart(sk_df.set_index("Skill"), color=ACCENT, height=280)
        with v2:
            dept_counts = {}
            for ind in inds.values():
                d = ind.get("department","Other")
                dept_counts[d] = dept_counts.get(d,0) + 1
            dept_df = pd.DataFrame(list(dept_counts.items()), columns=["Department","Count"])
            st.markdown(f'<div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">Individuals by Department</div>', unsafe_allow_html=True)
            st.bar_chart(dept_df.set_index("Department"), color=ACCENT, height=280)
        v3, v4 = st.columns(2)
        with v3:
            collab_scores = [v["score"] for v in db["collaborations"].values()]
            if collab_scores:
                bins = list(range(0, 12, 2))
                hist_data = pd.cut(collab_scores, bins=bins).value_counts().sort_index()
                st.markdown(f'<div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">Collaboration Score Histogram</div>', unsafe_allow_html=True)
                hist_df = pd.DataFrame({"Range": [str(b) for b in hist_data.index], "Count": hist_data.values})
                st.bar_chart(hist_df.set_index("Range"), color=ACCENT, height=260)
        with v4:
            scn_statuses = {"Analyzed": sum(1 for s in scns.values() if s.get("status")=="Analyzed"), "Pending": sum(1 for s in scns.values() if s.get("status","Pending")=="Pending")}
            st.markdown(f'<div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">Scenario Status Overview</div>', unsafe_allow_html=True)
            status_df = pd.DataFrame(list(scn_statuses.items()), columns=["Status","Count"])
            st.bar_chart(status_df.set_index("Status"), color=ACCENT, height=260)
    elif rpt_tab == "Search Individuals":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Search Individuals</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        search_q = st.text_input("Search by name, skill, interest, or department", key="search_ind_rpt", placeholder="e.g., Python, Alice, AI Research")
        if search_q:
            q = search_q.lower()
            results_list = []
            for uid, ind in inds.items():
                if (q in ind["name"].lower() or
                    any(q in s.lower() for s in ind.get("skills",[])) or
                    any(q in i.lower() for i in ind.get("interests",[])) or
                    q in ind.get("department","").lower()):
                    results_list.append(ind)
            st.markdown(f'<div style="font-size:12px;color:{TEXT_MUTED};margin-bottom:16px;">{len(results_list)} result(s) found</div>', unsafe_allow_html=True)
            for ind in results_list:
                skill_tags = " ".join([f'<span class="tag tag-green" style="margin:1px;font-size:10px;">{s}</span>' for s in ind.get("skills",[])])
                st.markdown(f"""
                <div class="card" style="padding:14px 18px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                        <div>
                            <div style="font-size:14px;font-weight:700;color:{TEXT_PRIMARY};">{ind['name']}</div>
                            <div style="font-size:11px;color:{TEXT_MUTED};">{ind.get('department','')} | {ind.get('email','')}</div>
                            <div style="margin-top:8px;">{skill_tags}</div>
                        </div>
                        <span class="tag tag-gray">{ind['id']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_admin():
    db = st.session_state.db
    if st.session_state.current_role != "Admin":
        st.error("Access denied. Admin role required.")
        return
    st.markdown(f"""
    <div class="fullwidth-card">
        <div class="section-heading">Administration Panel</div>
        <div class="section-sub">Manage users, system rules, skill categories, audit logs, and backups</div>
    </div>
    """, unsafe_allow_html=True)
    admin_tab = st.radio("", ["User Management", "System Rules", "Skill Categories", "Audit Logs", "Backup & Restore"], horizontal=True, key="admin_inner_tab")
    if admin_tab == "User Management":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Registered Users</div>
                <span class="tag tag-green">{len(db['users'])} Users</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        for uname, udata in db["users"].items():
            role = udata["role"]
            tag_cls = "tag-blue" if role == "Admin" else "tag-green"
            st.markdown(f"""
            <div class="card" style="padding:14px 20px;">
                <div style="display:flex;align-items:center;justify-content:space-between;">
                    <div style="display:flex;align-items:center;gap:12px;">
                        <div style="width:36px;height:36px;background:linear-gradient(135deg,{ACCENT2},{ACCENT});border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:{DARK_BG};">{uname[0].upper()}</div>
                        <div>
                            <div style="font-size:14px;font-weight:700;color:{TEXT_PRIMARY};">{uname}</div>
                            <div style="font-size:11px;color:{TEXT_MUTED};">Created: {udata.get('created','')[:10]}</div>
                        </div>
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span class="tag {tag_cls}">{role}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if uname != st.session_state.current_user:
                uc1, uc2 = st.columns([1, 4])
                with uc1:
                    new_role_sel = st.selectbox("Change Role", ["Admin","Analyst"], key=f"role_sel_{uname}", index=0 if role=="Admin" else 1)
                    if st.button("Update Role", key=f"upd_role_{uname}", use_container_width=True):
                        db["users"][uname]["role"] = new_role_sel
                        _log_action(st.session_state.current_user, f"Changed role of {uname} to {new_role_sel}")
                        st.success(f"Role updated.")
                        st.rerun()
                with uc2:
                    if st.button(f"Revoke Access ({uname})", key=f"revoke_{uname}", use_container_width=True):
                        del db["users"][uname]
                        _log_action(st.session_state.current_user, f"Revoked access for user: {uname}")
                        st.success(f"Access revoked for {uname}.")
                        st.rerun()
    elif admin_tab == "System Rules":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Analysis Rules Configuration</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        rules = db["rules"]
        with st.form("rules_form"):
            r1, r2 = st.columns(2)
            with r1:
                new_cw = st.slider("Default Collaboration Weight", 0.0, 1.0, float(rules["collab_weight"]), 0.05)
                new_sw = round(1 - new_cw, 2)
                st.info(f"Default Similarity Weight: {new_sw}")
                new_thresh = st.slider("Min Compatibility Threshold", 0.5, 8.0, float(rules["min_score_threshold"]), 0.5)
            with r2:
                new_max_grp = st.number_input("Max Group Size", 2, 20, int(rules["max_group_size"]))
                new_min_grp = st.number_input("Min Group Size", 2, 10, int(rules["min_group_size"]))
            if st.form_submit_button("Save Rules"):
                db["rules"]["collab_weight"] = new_cw
                db["rules"]["similarity_weight"] = new_sw
                db["rules"]["min_score_threshold"] = new_thresh
                db["rules"]["max_group_size"] = new_max_grp
                db["rules"]["min_group_size"] = new_min_grp
                _log_action(st.session_state.current_user, "Updated system rules")
                st.success("Rules saved successfully.")
                st.rerun()
        st.markdown(f"""
        <div class="card" style="margin-top:0;">
            <div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:14px;">Current Rules Summary</div>
            <div class="strength-bar-wrap">
                <div class="strength-label">Collab Weight</div>
                <div class="strength-track"><div class="strength-fill" style="width:{int(rules['collab_weight']*100)}%"></div></div>
                <div class="strength-value">{rules['collab_weight']}</div>
            </div>
            <div class="strength-bar-wrap">
                <div class="strength-label">Min Threshold</div>
                <div class="strength-track"><div class="strength-fill" style="width:{int(rules['min_score_threshold']/10*100)}%"></div></div>
                <div class="strength-value">{rules['min_score_threshold']}</div>
            </div>
            <div class="strength-bar-wrap">
                <div class="strength-label">Max Grp Size</div>
                <div class="strength-track"><div class="strength-fill" style="width:{int(rules['max_group_size']/20*100)}%"></div></div>
                <div class="strength-value">{int(rules['max_group_size'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif admin_tab == "Skill Categories":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Skill Categories</div>
                <span class="tag tag-green">{len(db['skill_categories'])} Categories</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Add New Category"):
            cat_name = st.text_input("Category Name", key="new_cat_name")
            cat_skills = st.text_input("Skills (comma-separated)", key="new_cat_skills", placeholder="Python, Java, C++")
            if st.button("Add Category", key="add_cat_btn"):
                if cat_name and cat_skills:
                    db["skill_categories"][cat_name] = [s.strip() for s in cat_skills.split(",") if s.strip()]
                    _log_action(st.session_state.current_user, f"Added skill category: {cat_name}")
                    st.success(f"Category '{cat_name}' added.")
                    st.rerun()
        for cat, skills in db["skill_categories"].items():
            skill_tags = " ".join([f'<span class="tag tag-green" style="margin:1px;font-size:10px;">{s}</span>' for s in skills])
            st.markdown(f"""
            <div class="card" style="padding:14px 20px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};">{cat}</div>
                    <span class="tag tag-gray">{len(skills)} skills</span>
                </div>
                <div>{skill_tags}</div>
            </div>
            """, unsafe_allow_html=True)
            dc1, dc2 = st.columns([1, 4])
            with dc1:
                if st.button(f"Delete '{cat}'", key=f"del_cat_{cat}", use_container_width=True):
                    del db["skill_categories"][cat]
                    _log_action(st.session_state.current_user, f"Deleted skill category: {cat}")
                    st.rerun()
    elif admin_tab == "Audit Logs":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>System Audit Log</div>
                <span class="tag tag-yellow">{len(db['audit_logs'])} Entries</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            log_user_filter = st.text_input("Filter by User", key="log_user_filter", placeholder="Username...")
        with lc2:
            log_action_filter = st.text_input("Filter by Action", key="log_action_filter", placeholder="Keyword...")
        with lc3:
            log_limit = st.number_input("Show last N entries", 10, 500, 50, key="log_limit")
        logs = db["audit_logs"].copy()
        if log_user_filter:
            logs = [l for l in logs if log_user_filter.lower() in l["user"].lower()]
        if log_action_filter:
            logs = [l for l in logs if log_action_filter.lower() in l["action"].lower()]
        logs = logs[-int(log_limit):][::-1]
        log_df = pd.DataFrame(logs)
        if not log_df.empty:
            log_df.columns = ["Timestamp", "User", "Action"]
            log_df["Timestamp"] = log_df["Timestamp"].str[:19]
            st.dataframe(log_df, use_container_width=True, hide_index=True)
            csv_buf = io.StringIO()
            log_df.to_csv(csv_buf, index=False)
            st.download_button("Export Audit Logs CSV", csv_buf.getvalue(), "drars_audit_logs.csv", "text/csv", key="dl_logs_btn", use_container_width=True)
        else:
            st.info("No log entries match the selected filters.")
    elif admin_tab == "Backup & Restore":
        st.markdown(f"""
        <div class="card card-accent">
            <div class="card-header">
                <div class="card-title"><div class="card-title-dot"></div>Backup & Restore System Data</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        bk1, bk2 = st.columns(2)
        with bk1:
            st.markdown(f'<div style="font-size:14px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">Create Backup</div>', unsafe_allow_html=True)
            backup_label = st.text_input("Backup Label", key="backup_label_inp", placeholder="e.g., Pre-Analysis Backup")
            if st.button("Create Backup Now", key="create_backup_btn", use_container_width=True):
                bk_id = f"BK{len(db['backups'])+1:03d}"
                label = backup_label or f"Backup {bk_id}"
                bk_data = {
                    "id": bk_id,
                    "label": label,
                    "timestamp": str(datetime.datetime.now()),
                    "individuals_count": len(db["individuals"]),
                    "scenarios_count": len(db["scenarios"]),
                    "users_count": len(db["users"]),
                    "data": json.dumps({
                        "individuals": db["individuals"],
                        "skill_categories": db["skill_categories"],
                        "collaborations": db["collaborations"],
                        "skill_similarities": db["skill_similarities"],
                        "scenarios": {k: {kk: vv for kk, vv in v.items()} for k, v in db["scenarios"].items()},
                        "rules": db["rules"]
                    })
                }
                db["backups"][bk_id] = bk_data
                _log_action(st.session_state.current_user, f"Created backup: {label}")
                st.success(f"Backup '{label}' created successfully.")
                st.rerun()
            st.markdown(f'<div style="margin-top:20px;font-size:14px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">Saved Backups</div>', unsafe_allow_html=True)
            if db["backups"]:
                for bk_id, bk in list(db["backups"].items())[::-1]:
                    st.markdown(f"""
                    <div class="card" style="padding:12px 16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div>
                                <div style="font-size:13px;font-weight:700;color:{TEXT_PRIMARY};">{bk['label']}</div>
                                <div style="font-size:10px;color:{TEXT_MUTED};">{bk['timestamp'][:16]} | {bk['individuals_count']} individuals | {bk['scenarios_count']} scenarios</div>
                            </div>
                            <span class="tag tag-gray">{bk_id}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button(f"Restore {bk_id}", key=f"restore_{bk_id}", use_container_width=True):
                            try:
                                restored = json.loads(bk["data"])
                                db["individuals"] = restored["individuals"]
                                db["skill_categories"] = restored["skill_categories"]
                                db["collaborations"] = restored["collaborations"]
                                db["skill_similarities"] = restored["skill_similarities"]
                                db["scenarios"] = restored["scenarios"]
                                db["rules"] = restored["rules"]
                                _log_action(st.session_state.current_user, f"Restored backup: {bk['label']}")
                                st.success(f"Restored from backup {bk_id}.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Restore failed: {e}")
                    with bc2:
                        json_data = json.dumps(bk, indent=2)
                        st.download_button(f"Download {bk_id}", json_data, f"drars_backup_{bk_id}.json", "application/json", key=f"dl_bk_{bk_id}", use_container_width=True)
            else:
                st.info("No backups created yet.")
        with bk2:
            st.markdown(f'<div style="font-size:14px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:12px;">System Statistics</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:10px;">
                <div class="metric-value">{len(db['individuals'])}</div>
                <div class="metric-label">Total Individuals</div>
            </div>
            <div class="metric-card" style="margin-bottom:10px;">
                <div class="metric-value">{len(db['collaborations'])}</div>
                <div class="metric-label">Collaboration Records</div>
            </div>
            <div class="metric-card" style="margin-bottom:10px;">
                <div class="metric-value">{len(db['skill_similarities'])}</div>
                <div class="metric-label">Similarity Records</div>
            </div>
            <div class="metric-card" style="margin-bottom:10px;">
                <div class="metric-value">{len(db['scenarios'])}</div>
                <div class="metric-label">Scenarios</div>
            </div>
            <div class="metric-card" style="margin-bottom:10px;">
                <div class="metric-value">{len(db['audit_logs'])}</div>
                <div class="metric-label">Audit Log Entries</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(db['backups'])}</div>
                <div class="metric-label">Saved Backups</div>
            </div>
            """, unsafe_allow_html=True)

def main():
    init_state()
    if not st.session_state.logged_in:
        render_login()
        return
    render_topbar()
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    page = st.session_state.page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Individuals":
        render_individuals()
    elif page == "Relationships":
        render_relationships()
    elif page == "Scenarios":
        render_scenarios()
    elif page == "Analysis":
        render_analysis()
    elif page == "Reports":
        render_reports()
    elif page == "Admin":
        render_admin()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;padding:24px 0 12px;font-size:10px;color:{TEXT_MUTED};border-top:1px solid {CARD_BORDER};margin-top:32px;">
        DRARS v2.0 &bull; Dual-Relationship Analysis and Recommendation System &bull; CollabTech Solutions &bull; Spring 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()