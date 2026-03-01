import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="Mô phỏng đầu tư", layout="wide")

st.title("📈 MÔ PHỎNG CHIẾN LƯỢC ĐẦU TƯ LÃI KÉP")

# ===== NHẬP DỮ LIỆU =====
st.sidebar.header("Nhập thông tin đầu tư")

von_ban_dau = st.sidebar.number_input("Vốn ban đầu (VND)", value=10000000)
lai_suat = st.sidebar.number_input("Lãi suất năm (%)", value=7.0) / 100
so_nam = st.sidebar.number_input("Số năm đầu tư", min_value=1, max_value=50, value=10)
gui_them_thang = st.sidebar.number_input("Gửi thêm mỗi tháng (VND)", value=2000000)
do_bien_dong = st.sidebar.slider("Độ biến động % mỗi tháng", 0.0, 50.0, 20.0) / 100
lam_phat = st.sidebar.number_input("Lạm phát năm (%)", value=3.0) / 100

# ===== TÍNH TOÁN =====
thang = int(so_nam * 12)
lai_suat_thang = lai_suat / 12
lai_suat_cao = (lai_suat + 0.02) / 12
lam_phat_thang = lam_phat / 12

tien_chien_luoc1 = []
tien_chien_luoc2 = []
tien_chien_luoc3 = []

tien1 = von_ban_dau
tien2 = von_ban_dau
tien3 = von_ban_dau

for i in range(thang):

    bien_dong1 = random.uniform(-do_bien_dong, do_bien_dong)
    bien_dong2 = random.uniform(-do_bien_dong, do_bien_dong)
    bien_dong3 = random.uniform(-do_bien_dong, do_bien_dong)

    # Chiến lược 1: đầu tư 1 lần
    tien1 *= (1 + lai_suat_thang + bien_dong1)

    # Chiến lược 2: đầu tư + gửi thêm
    tien2 = tien2 * (1 + lai_suat_thang + bien_dong2) + gui_them_thang

    # Chiến lược 3: lãi suất cao hơn 2%
    tien3 *= (1 + lai_suat_cao + bien_dong3)

    # Trừ lạm phát
    tien1 *= (1 - lam_phat_thang)
    tien2 *= (1 - lam_phat_thang)
    tien3 *= (1 - lam_phat_thang)

    tien_chien_luoc1.append(tien1)
    tien_chien_luoc2.append(tien2)
    tien_chien_luoc3.append(tien3)

# ===== TÍNH KỊCH BẢN =====
trung_binh = (tien1 + tien2 + tien3) / 3
tot_nhat = max(tien1, tien2, tien3)
xau_nhat = min(tien1, tien2, tien3)

# ===== HIỂN THỊ KẾT QUẢ =====
st.subheader("📊 Kết quả sau {} năm".format(so_nam))

col1, col2, col3 = st.columns(3)

col1.metric("💰 Lợi nhuận trung bình", f"{round(trung_binh,0):,.0f} VND")
col2.metric("🚀 Kịch bản tốt nhất", f"{round(tot_nhat,0):,.0f} VND")
col3.metric("⚠️ Kịch bản xấu nhất", f"{round(xau_nhat,0):,.0f} VND")

# ===== VẼ BIỂU ĐỒ =====
data1 = [x/1_000_000 for x in tien_chien_luoc1]
data2 = [x/1_000_000 for x in tien_chien_luoc2]
data3 = [x/1_000_000 for x in tien_chien_luoc3]

thang_list = list(range(1, len(data1)+1))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=thang_list,
    y=data1,
    mode='lines',
    name='Chiến lược 1: Đầu tư 1 lần',
))

fig.add_trace(go.Scatter(
    x=thang_list,
    y=data2,
    mode='lines',
    name='Chiến lược 2: Đầu tư + gửi thêm',
))

fig.add_trace(go.Scatter(
    x=thang_list,
    y=data3,
    mode='lines',
    name='Chiến lược 3: Lãi suất cao hơn',
))
fig.update_layout(
    title="Mô phỏng đầu tư (Đã tính lạm phát)",
    xaxis_title="Thời gian (Tháng)",
    yaxis_title="Số tiền (Triệu VND)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
