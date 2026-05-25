import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import platform

# [한글 깨짐 방지] 운영체제별 및 리눅스(스트림릿 클라우드) 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    # 스트림릿 클라우드 서버 환경을 위한 나눔고딕 설정
    plt.rc('font', family='NanumGothic')

plt.rc('axes', unicode_minus=False)

st.title("🧪 분자 벡터 합성 시뮬레이터 (2D & 3D)")
st.write("평면벡터부터 공간벡터까지: 분자 구조의 기하학적 분석")

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
    
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True, alpha=0.2); ax.legend()
    st.pyplot(fig)

else:  # 3D 메테인 모드
    st.info("💡 메테인(CH₄): 정사면체 꼭짓점 방향으로 뻗은 4개의 공간벡터를 합하면 영벡터(0,0,0)가 됩니다.")
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 정사면체 기하학적 좌표 설정 (C: 원점, H: 각 꼭짓점)
    # 공간벡터 성분: (1,1,1), (-1,-1,1), (-1,1,-1), (1,-1,-1)
    h_coords = np.array([[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    
    # 탄소(C) 원점 표시
    ax.scatter([0], [0], [0], color='black', s=300, label='탄소 (C)')
    
    # 4개의 공간벡터 그리기
    for i, coord in enumerate(h_coords):
        ax.scatter(coord[0], coord[1], coord[2], s=200, label=f'수소 (H){i+1}')
        # 원점에서 각 수소로 향하는 화살표 (공간벡터)
        ax.quiver(0, 0, 0, coord[0], coord[1], coord[2], color='blue', alpha=0.6, arrow_length_ratio=0.1)
        # 결합선 그리기
        ax.plot([0, coord[0]], [0, coord[1]], [0, coord[2]], color='gray', linestyle='--')

    # 공간벡터 합 계산: (1-1-1+1, 1-1+1-1, 1+1-1-1) = (0, 0, 0)
    v_sum = np.sum(h_coords, axis=0)
    st.write(f"📊 **공간벡터 합계 (Σv):** x={v_sum[0]}, y={v_sum[1]}, z={v_sum[2]}")
    
    if np.allclose(v_sum, [0, 0, 0]):
        st.success("✨ 4개의 공간벡터가 3차원 상에서 완벽히 상쇄되어 무극성(영벡터)을 이룹니다.")

    ax.set_xlabel('X축'); ax.set_ylabel('Y축'); ax.set_zlabel('Z축')
    ax.set_title("메테인(CH₄)의 3차원 공간벡터 모델")
    ax.legend()
    st.pyplot(fig)
