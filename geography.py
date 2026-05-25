import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 복잡한 한글 폰트 설정 코드는 모두 삭제함 (영문 출력으로 폰트 깨짐 원천 차단)
plt.rc('axes', unicode_minus=False)

st.title("🧪 Molecular Vector Synthesis Simulator (2D & 3D)")
st.write("From Planar Vectors to Space Vectors: Geometric Analysis of Molecular Structures")

# 1. 시뮬레이션 모드 선택
mode = st.sidebar.selectbox("Select Analysis Mode", ["2D Planar Molecule (H2O, CO2, etc.)", "3D Space Molecule (CH4 Methane)"])

if mode == "2D Planar Molecule (H2O, CO2, etc.)":
    molecule = st.radio("Select a Molecule", ["Carbon Dioxide (CO₂)", "Water (H₂O)", "Formaldehyde (CH₂O)", "Boron Trifluoride (BF₃)"])
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(0, 0, 'ko', markersize=20, label="Central Atom")
    
    f_vectors = []
    labels = []
    coords = []
    
    if molecule == "Carbon Dioxide (CO₂)":
        coords = [(-2, 0), (2, 0)]; labels = ["Oxygen (O)", "Oxygen (O)"]
        f_vectors = [np.array([-3, 0]), np.array([3, 0])]
    elif molecule == "Water (H₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2)]; labels = ["Hydrogen (H)", "Hydrogen (H)"]
        f_vectors = [np.array([2, 1.8]), np.array([-2, 1.8])]
    elif molecule == "Formaldehyde (CH₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2), (0, 2.5)]; labels = ["Hydrogen (H)", "Hydrogen (H)", "Oxygen (O)"]
        f_vectors = [np.array([1.5, 1.2]), np.array([-1.5, 1.2]), np.array([0, 3.0])]
    elif molecule == "Boron Trifluoride (BF₃)":
        coords = [(0, 2.5), (-2.16, -1.25), (2.16, -1.25)]; labels = ["Fluorine (F)", "Fluorine (F)", "Fluorine (F)"]
        f_vectors = [np.array([0, 3.0]), np.array([-2.6, -1.5]), np.array([2.6, -1.5])]

    f_total = sum(f_vectors)
    colors = ['blue', 'green', 'purple']
    for i, (coord, f_vec, label) in enumerate(zip(coords, f_vectors, labels)):
        ax.plot(coord[0], coord[1], 'o', markersize=15, label=f"{label}")
        ax.quiver(0, 0, f_vec[0], f_vec[1], angles='xy', scale_units='xy', scale=1, color=colors[i], alpha=0.7)
    
    if not np.allclose(f_total, [0, 0], atol=1e-2):
        ax.quiver(0, 0, f_total[0], f_total[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.015, label='Net Vector')
    
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True, alpha=0.2); ax.legend()
    st.pyplot(fig)

else:  # 3D 메테인 모드
    st.info("💡 Methane (CH₄): The sum of the 4 space vectors pointing toward the vertices of a regular tetrahedron becomes a zero vector (0,0,0).")
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 정사면체 기하학적 좌표 설정 (C: 원점, H: 각 꼭짓점)
    h_coords = np.array([[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    
    # 탄소(C) 원점 표시
    ax.scatter([0], [0], [0], color='black', s=300, label='Carbon (C)')
    
    # 4개의 공간벡터 그리기
    for i, coord in enumerate(h_coords):
        ax.scatter(coord[0], coord[1], coord[2], s=200, label=f'Hydrogen (H){i+1}')
        ax.quiver(0, 0, 0, coord[0], coord[1], coord[2], color='blue', alpha=0.6, arrow_length_ratio=0.1)
        ax.plot([0, coord[0]], [0, coord[1]], [0, coord[2]], color='gray', linestyle='--')

    v_sum = np.sum(h_coords, axis=0)
    st.write(f"📊 **Space Vector Sum (Σv):** x={v_sum[0]}, y={v_sum[1]}, z={v_sum[2]}")
    
    if np.allclose(v_sum, [0, 0, 0]):
        st.success("✨ The 4 space vectors perfectly cancel out in 3D space, forming a non-polar molecule (zero vector).")

    ax.set_xlabel('X-axis'); ax.set_ylabel('Y-axis'); ax.set_zlabel('Z-axis')
    ax.set_title("3D Space Vector Model of Methane (CH₄)")
    ax.legend()
    st.pyplot(fig)
