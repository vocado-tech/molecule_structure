import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import platform
import matplotlib.font_manager as fm
import os

# ==========================================================
# [철통 보안 한글 깨짐 방지] 폰트 파일 경로 직접 지정 알고리즘
# ==========================================================
font_name = "sans-serif"
try:
    if platform.system() == 'Windows':
        # 윈도우 시스템 폰트 폴더에서 맑은 고딕 파일을 직접 로드
        win_font_path = os.path.join(os.environ['SystemRoot'], 'Fonts', 'malgun.ttf')
        if os.path.exists(win_font_path):
            font_prop = fm.FontProperties(fname=win_font_path)
            font_name = font_prop.get_name()
            plt.rc('font', family=font_name)
    elif platform.system() == 'Darwin': # Mac
        mac_font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
        if os.path.exists(mac_font_path):
            font_prop = fm.FontProperties(fname=mac_font_path)
            font_name = font_prop.get_name()
            plt.rc('font', family=font_name)
except Exception as e:
    pass

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False 
# ==========================================================

# 웹 앱 상단 제목 및 제작자 표기 반영
st.title("🧪 분자 벡터 합성 시뮬레이터 (2D & 3D)")
st.subheader("👨‍💻 제작: 김도형")
st.write("대각선 평면벡터와 공간벡터의 성분 분해를 통한 분자의 극성 분석")

# 1. 시뮬레이션 모드 선택
mode = st.sidebar.selectbox("분석 모드 선택", ["2D 평면 분자 (H2O, CO2 등)", "3D 공간 분자 (CH4 메테인)"])

if mode == "2D 평면 분자 (H2O, CO2 등)":
    molecule = st.radio("분자를 선택하세요", ["이산화탄소 (CO₂)", "물 (H₂O)", "폼알데하이드 (CH₂O)", "삼플루오린화붕소 (BF₃)"])
    
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(0, 0, 'ko', markersize=20, label="중심 원자")
    
    f_vectors = []
    labels = []
    coords = []
    
    if molecule == "이산화탄소 (CO₂)":
        coords = [(-2, 0), (2, 0)]; labels = ["산소 (O)", "산소 (O)"]
        f_vectors = [np.array([-3, 0]), np.array([3, 0])]
    elif molecule == "물 (H₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2)]; labels = ["수소 (H)", "수소 (H)"]
        f_vectors = [np.array([2, 1.8]), np.array([-2, 1.8])]
    elif molecule == "폼알데하이드 (CH₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2), (0, 2.5)]; labels = ["수소 (H)", "수소 (H)", "산소 (O)"]
        f_vectors = [np.array([1.5, 1.2]), np.array([-1.5, 1.2]), np.array([0, 3.0])]
    elif molecule == "삼플루오린화붕소 (BF₃)":
        coords = [(0, 2.5), (-2.16, -1.25), (2.16, -1.25)]; labels = ["플루오린 (F)", "플루오린 (F)", "플루오린 (F)"]
        f_vectors = [np.array([0, 3.0]), np.array([-2.6, -1.5]), np.array([2.6, -1.5])]

    f_total = sum(f_vectors)
    colors = ['blue', 'green', 'purple']
    
    for i, (coord, f_vec, label) in enumerate(zip(coords, f_vectors, labels)):
        ax.plot(coord[0], coord[1], 'o', markersize=15, label=f"{label}")
        ax.quiver(0, 0, f_vec[0], f_vec[1], angles='xy', scale_units='xy', scale=1, color=colors[i], alpha=0.7)
    
    if not np.allclose(f_total, [0, 0], atol=1e-2):
        ax.quiver(0, 0, f_total[0], f_total[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.015, label='총 합벡터')
    
    # 2D 결과 박스 처리 (노란색 박스 고정)
    if np.allclose(f_total, [0, 0], atol=1e-2):
        st.warning("💛 대칭 구조로 인해 극성 벡터의 합이 완벽히 0(영벡터)이 되며, 무극성 분자입니다.")
    else:
        st.error(f"⚡ 기하학적 상쇄 실패! 남은 합벡터 성분: (x: {f_total[0]:.1f}, y: {f_total[1]:.1f}) -> 극성 분자")
    
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True, alpha=0.2)
    ax.legend(loc='lower right')
    ax.set_title(f"{molecule} 2차원 기하학적 벡터 모델")
    st.pyplot(fig)

else:  # 3D 메테인 모드
    st.info("💡 메테인(CH₄): 정사면체 꼭짓점 방향으로 뻗은 4개의 공간벡터를 합하면 영벡터(0,0,0)가 됩니다.")
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 정사면체 기하학적 좌표 설정 (C: 원점, H: 각 꼭짓점)
    h_coords = np.array([[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    
    # 탄소(C) 원점 표시
    ax.scatter([0], [0], [0], color='black', s=300, label='탄소 (C)')
    
    # 4개의 공간벡터 그리기
    for i, coord in enumerate(h_coords):
        ax.scatter(coord[0], coord[1], coord[2], s=200, label=f'수소 (H){i+1}')
        ax.quiver(0, 0, 0, coord[0], coord[1], coord[2], color='blue', alpha=0.6, arrow_length_ratio=0.1)
        ax.plot([0, coord[0]], [0, coord[1]], [0, coord[2]], color='gray', linestyle='--')

    # 공간벡터 합 계산
    v_sum = np.sum(h_coords, axis=0)
    st.write(f"📊 **공간벡터 합계 (Σv):** x={v_sum[0]}, y={v_sum[1]}, z={v_sum[2]}")
    
    if np.allclose(v_sum, [0, 0, 0]):
        st.warning("💛 대칭 구조로 인해 극성 벡터의 합이 완벽히 0(영벡터)이 되며, 무극성 분자입니다.")

    ax.set_xlabel('X축'); ax.set_ylabel('Y축'); ax.set_zlabel('Z축')
    ax.set_title("메테인(CH₄)의 3차원 공간벡터 모델")
    st.pyplot(fig)
