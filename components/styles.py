import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        footer {visibility: hidden;}

        /* Page Titles */
        .page-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #1E88E5;
        }
        .page-subtitle {
            font-size: 16px;
            color: #888;
            margin-bottom: 24px;
        }

        /* Chat Bubbles */
        .chat-user {
            background: linear-gradient(135deg, #1E88E522, #1E88E511);
            border-left: 4px solid #1E88E5;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 12px;
            text-align: right;
            color: #E3F2FD;
        }
        .chat-ai {
            background: linear-gradient(135deg, #43A04722, #43A04711);
            border-left: 4px solid #43A047;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #E8F5E9;
        }

        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #1E88E5 0%, #1565C0 50%, #0D47A1 100%);
            border-radius: 16px;
            padding: 48px 40px;
            margin-bottom: 32px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(30, 136, 229, 0.3);
        }
        .hero-title {
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 12px;
            color: white;
        }
        .hero-subtitle {
            font-size: 18px;
            opacity: 0.9;
            color: white;
        }

        /* Feature Cards */
        .feature-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }
        .feature-icon {
            font-size: 36px;
            margin-bottom: 12px;
        }
        .feature-title {
            font-size: 16px;
            font-weight: 700;
            color: #1E88E5;
            margin-bottom: 6px;
        }
        .feature-desc {
            font-size: 13px;
            color: #888;
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        .status-ready {
            background: #43A04722;
            color: #43A047;
            border: 1px solid #43A04744;
        }
        .status-not-ready {
            background: #FB8C0022;
            color: #FB8C00;
            border: 1px solid #FB8C0044;
        }

        /* Upload Zone */
        .upload-zone {
            border: 2px dashed #1E88E5;
            border-radius: 12px;
            padding: 32px;
            text-align: center;
            background: #1E88E508;
            margin-bottom: 20px;
        }

        /* Sidebar Navigation */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        }
        [data-testid="stSidebar"] .stButton button {
            border-radius: 8px;
            margin-bottom: 4px;
            padding: 8px 16px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background: #1E88E5;
            color: white;
            transform: translateX(4px);
        }
    </style>
    """, unsafe_allow_html=True)
