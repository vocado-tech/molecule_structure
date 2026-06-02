import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
# [폰트 초기화] 한글 설정을 아예 제거하고 기본 영문 폰트(sans-serif) 사용
# ==========================================================
plt.rc('font', family='sans-serif')
plt.rcParams['axes.unicode_minus'] = False 
# ==========================================================

# 웹 앱 상단 제목 및 제작자 표기는 스트림릿 기본 텍스트라 한글이 잘 나옵니다!
st.title("🧪 분자 벡터 합성 시뮬레이터 (2D & 3D)")
st.subheader("👨‍💻 제작: 김도형")
st.write("대각선 평면벡터와 공간벡터의 성분 분해를 통한 분자의 극성 분석")

# 1. 시뮬레이션 모드 선택
mode = st.sidebar.selectbox("분석 모드 선택", ["2D 평면 분자 (H2O, CO2 등)", "3D 공간 분자 (CH4 메테인)"])

if mode == "2D 평면 분자 (H2O, CO2 등)":
    molecule = st.radio("분자를 선택하세요", ["이산화탄소 (CO₂)", "물 (H₂O)", "폼알데하이드 (CH₂O)", "삼플루오린화붕소 (BF₃)"])
    
    fig, ax = plt.subplots(figsize=(7, 7))
    # 그래프 안의 범례(Label)들을 영어로 변경
    ax.plot(0, 0, 'ko', markersize=20, label="Center Atom")
    
    f_vectors = []
    labels = []
    coords = []
    
    # 각 원자 이름(labels)을 영어로 변경
    if molecule == "이산화탄소 (CO₂)":
        coords = [(-2, 0), (2, 0)]; labels = ["Oxygen (O)", "Oxygen (O)"]
        f_vectors = [np.array([-3, 0]), np.array([3, 0])]
        title_name = "CO2 2D Geometric Vector Model"
    elif molecule == "물 (H₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2)]; labels = ["Hydrogen (H)", "Hydrogen (H)"]
        f_vectors = [np.array([2, 1.8]), np.array([-2, 1.8])]
        title_name = "H2O 2D Geometric Vector Model"
    elif molecule == "폼알데하이드 (CH₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2), (0, 2.5)]; labels = ["Hydrogen (H)", "Hydrogen (H)", "Oxygen (O)"]
        f_vectors = [np.array([1.5, 1.2]), np.array([-1.5, 1.2]), np.array([0, 3.0])]
        title_name = "CH2O 2D Geometric Vector Model"
    elif molecule == "삼플루오린화붕소 (BF₃)":
        coords = [(0, 2.5), (-2.16, -1.25), (2.16, -1.25)]; labels = ["Fluorine (F)", "Fluorine (F)", "Fluorine (F)"]
        f_vectors = [np.array([0, 3.0]), np.array([-2.6, -1.5]), np.array([2.6, -1.5])]
        title_name = "BF3 2D Geometric Vector Model"

    f_total = sum(f_vectors)
    colors = ['blue', 'green', 'purple']
    
    for i, (coord, f_vec, label) in enumerate(zip(coords, f_vectors, labels)):
        ax.plot(coord[0], coord[1], 'o', markersize=15, label=f"{label} {i+1}")
        ax.quiver(0, 0, f_vec[0], f_vec[1], angles='xy', scale_units='xy', scale=1, color=colors[i], alpha=0.7, label=f"Bond Vector {i+1}")
    
    if not np.allclose(f_total, [0, 0], atol=1e-2):
        ax.quiver(0, 0, f_total[0], f_total[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.015, label='Total Vector (Sum)')
    
    # 웹 화면의 결과 안내 박스는 노란색 한글로 유지
    if np.allclose(f_total, [0, 0], atol=1e-2):
        st.warning("💛 대칭 구조로 인해 극성 벡터의 합이 완벽히 0(영벡터)이 되며, 무극성 분자입니다.")
    else:
        st.error(f"⚡ 기하학적 상쇄 실패! 남은 합벡터 성분: (x: {f_total[0]:.1f}, y: {f_total[1]:.1f}) -> 극성 분자")
    
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True, alpha=0.2)
    ax.legend(loc='lower right')
    ax.set_title(title_name) # 영어 제목 주입
    st.pyplot(fig)

else:  # 3D 메테인 모드
    st.info("💡 메테인(CH₄): 정사면체 꼭짓점 방향으로 뻗은 4개의 공간벡터를 합하면 영벡터(0,0,0)가 됩니다.")
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    h_coords = np.array([[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    
    # 3D 그래프 범례 영어로 변경
    ax.scatter([0], [0], [0], color='black', s=300, label='Carbon (C)')
    
    for i, coord in enumerate(h_coords):
        ax.scatter(coord[0], coord[1], coord[2], s=200, label=f'Hydrogen (H) {i+1}')
        ax.quiver(0, 0, 0, coord[0], coord[1], coord[2], color='blue', alpha=0.6, arrow_length_ratio=0.1)
        ax.plot([0, coord[0]], [0, coord[1]], [0, coord[2]], color='gray', linestyle='--')

    v_sum = np.sum(h_coords, axis=0)
    st.write(f"📊 **공간벡터 합계 (Σv):** x={v_sum[0]}, y={v_sum[1]}, z={v_sum[2]}")
    
    if np.allclose(v_sum, [0, 0, 0]):
        st.warning("💛 대칭 구조로 인해 극성 벡터의 합이 완벽히 0(영벡터)이 되며, 무극성 분자입니다.")

    # 축 이름과 제목 영어로 변경
    ax.set_xlabel('X-axis'); ax.set_ylabel('Y-axis'); ax.set_zlabel('Z-axis')
    ax.set_title("Methane (CH4) 3D Vector Model")
    ax.legend(loc='upper left')
    st.pyplot(fig)
