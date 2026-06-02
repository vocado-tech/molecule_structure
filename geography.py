import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
# [폰트 초기화] 기본 영문 폰트(sans-serif) 사용하여 깨짐 방지
# ==========================================================
plt.rc('font', family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False 
# ==========================================================

# ==========================================================
# [말풍선 CSS] 테두리 없는 몽글몽글한 '생각 말풍선' 디자인
# ==========================================================
st.markdown("""
<style>
.floating-bubble {
    position: fixed;
    bottom: 70px;
    left: 40px;
    background-color: #ffffff;
    border: none; /* 테두리 제거 */
    border-radius: 20px;
    padding: 10px 16px; /* 크기 축소 */
    font-size: 13px; /* 글자 크기 축소 */
    font-weight: 700;
    color: #495057;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15); /* 부드러운 그림자 */
    z-index: 9999;
    animation: float 3s ease-in-out infinite;
}
/* 첫 번째 생각 동그라미 (중간 크기) */
.floating-bubble::before {
    content: '';
    position: absolute;
    bottom: -12px;
    left: 15px;
    width: 12px;
    height: 12px;
    background-color: #ffffff;
    border-radius: 50%;
    box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
}
/* 두 번째 생각 동그라미 (가장 작은 크기) */
.floating-bubble::after {
    content: '';
    position: absolute
