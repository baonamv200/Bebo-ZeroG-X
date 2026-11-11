import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors (NASA Mission Control Dark)
BG_COLOR = RGBColor(4, 8, 22)           # #040816 Deep space dark
CARD_BG = RGBColor(14, 27, 56)          # #0E1B38 Glass card
CARD_BG_ALT = RGBColor(18, 36, 74)      # #12244A Lighter navy
CARD_BORDER = RGBColor(30, 58, 110)     # #1E3A6E Border
CYAN_ACCENT = RGBColor(0, 242, 255)     # #00F2FF Bright cyan
CYAN_GLOW = RGBColor(56, 189, 248)      # #38BDF8 Sky glow
NASA_RED = RGBColor(224, 60, 49)        # #E03C31 NASA Red
NASA_BLUE = RGBColor(11, 61, 145)       # #0B3D91 NASA Blue
AMBER_WARN = RGBColor(245, 158, 11)     # #F59E0B Amber
GREEN_OK = RGBColor(16, 185, 129)       # #10B981 Emerald
TEXT_WHITE = RGBColor(248, 250, 252)    # #F8FAFC White
TEXT_MUTED = RGBColor(203, 213, 225)    # #CBD5E1 Light slate
TEXT_SUBTLE = RGBColor(148, 163, 184)   # #94A3B8

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"

def create_slide(notes=""):
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide

def add_header(slide, title, category="NASA SPACE APPS CHALLENGE 2026", slide_num=None):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = f"// {category.upper()}"
    p_c.font.name = FONT_MONO
    p_c.font.size = Pt(13)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN_ACCENT

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(10.5), Inches(0.75))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    if slide_num:
        num_box = slide.shapes.add_textbox(Inches(11.0), Inches(0.5), Inches(1.5), Inches(0.5))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"[{slide_num:02d}/08]"
        p_n.font.name = FONT_MONO
        p_n.font.size = Pt(14)
        p_n.font.bold = True
        p_n.font.color.rgb = CYAN_GLOW

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.025))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.fill.background()

def add_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER, border_width=1.5):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg
    card.line.color.rgb = border
    card.line.width = Pt(border_width)
    return card

# ==============================================================================
# SLIDE 1: TRANG BÌA
# ==============================================================================
s1_notes = """Kính chào ban giám khảo và các bạn, tôi là Vũ Bảo Nam. Hôm nay tôi xin giới thiệu dự án 'Flames in Freefall' – một nền tảng trí tuệ nhân tạo và mô phỏng vật lý chuyên sâu nhằm giải mã hành vi của ngọn lửa trong môi trường vi trọng lực, hướng tới bảo vệ an toàn tính mạng cho các phi hành gia trên trạm ISS và các sứ mệnh Artemis, Sao Hỏa tương lai."""
s1 = create_slide(s1_notes)

badge = add_card(s1, Inches(0.8), Inches(0.8), Inches(5.2), Inches(0.5), bg=RGBColor(11, 30, 68), border=CYAN_ACCENT)
tf_b = badge.text_frame
tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
p_b = tf_b.paragraphs[0]
p_b.alignment = PP_ALIGN.CENTER
p_b.text = "NASA SPACE APPS CHALLENGE 2026 // OFFICIAL ENTRY"
p_b.font.name = FONT_MONO
p_b.font.size = Pt(12)
p_b.font.bold = True
p_b.font.color.rgb = CYAN_ACCENT

t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(7.5), Inches(2.2))
tf = t_box.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "FLAMES IN FREEFALL"
p1.font.name = FONT_HEADING
p1.font.size = Pt(48)
p1.font.bold = True
p1.font.color.rgb = TEXT_WHITE

p2 = tf.add_paragraph()
p2.text = "Bảng điều khiển AI phân tích sự cháy trong vi trọng lực & An toàn hỏa hoạn tàu vũ trụ"
p2.font.name = FONT_HEADING
p2.font.size = Pt(22)
p2.font.color.rgb = CYAN_GLOW

# Flame concentric illustration
fx = Inches(10.5)
fy = Inches(3.2)
r1 = s1.shapes.add_shape(MSO_SHAPE.OVAL, fx - Inches(2.2), fy - Inches(2.2), Inches(4.4), Inches(4.4))
r1.fill.solid()
r1.fill.fore_color.rgb = RGBColor(6, 16, 40)
r1.line.color.rgb = RGBColor(30, 58, 110)
r1.line.width = Pt(2)

r2 = s1.shapes.add_shape(MSO_SHAPE.OVAL, fx - Inches(1.5), fy - Inches(1.5), Inches(3.0), Inches(3.0))
r2.fill.solid()
r2.fill.fore_color.rgb = RGBColor(11, 61, 145)
r2.line.color.rgb = CYAN_GLOW
r2.line.width = Pt(1.5)

core = s1.shapes.add_shape(MSO_SHAPE.OVAL, fx - Inches(0.8), fy - Inches(0.8), Inches(1.6), Inches(1.6))
core.fill.solid()
core.fill.fore_color.rgb = CYAN_ACCENT
core.line.color.rgb = TEXT_WHITE
core.line.width = Pt(2)

lbl_box = s1.shapes.add_textbox(fx - Inches(2.0), fy + Inches(2.3), Inches(4.0), Inches(0.5))
p_lbl = lbl_box.text_frame.paragraphs[0]
p_lbl.alignment = PP_ALIGN.CENTER
p_lbl.text = "0g Spherical Flame 3D Diffusion Field"
p_lbl.font.name = FONT_MONO
p_lbl.font.size = Pt(12)
p_lbl.font.color.rgb = CYAN_GLOW

card_w = Inches(5.65)
card_h = Inches(2.8)
card_y = Inches(4.0)

c1 = add_card(s1, Inches(0.8), card_y, card_w, card_h, bg=CARD_BG, border=CYAN_ACCENT)
tf1 = c1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_right = Inches(0.35)
tf1.margin_top = Inches(0.3)
p = tf1.paragraphs[0]
p.text = "BEBO IGNIS-0G COMBUSTION ENGINE"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf1.add_paragraph()
p.text = "Mô phỏng Động học Đốt cháy Vũ trụ"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tf1.add_paragraph()
p.text = "• Chuẩn hóa dữ liệu thực nghiệm NASA PSI (SoFIE, Saffire, BASS-II)\n• Đánh giá rủi ro hỏa hoạn tức thời qua chỉ số SFRS (0–100)\n• Trực quan hóa 3D hình thái ngọn lửa & trường nhiệt độ"
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

c2 = add_card(s1, Inches(6.88), card_y, card_w, card_h, bg=CARD_BG_ALT, border=CARD_BORDER)
tf2 = c2.text_frame
tf2.word_wrap = True
tf2.margin_left = tf2.margin_right = Inches(0.35)
tf2.margin_top = Inches(0.3)
p = tf2.paragraphs[0]
p.text = "TÁC GIẢ & THÔNG TIN DỰ ÁN"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf2.add_paragraph()
p.text = "Vũ Bảo Nam (Vu Bao Nam)"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tf2.add_paragraph()
p.text = "• Bebo ZeroG-X • VBN Lab | Trường THPT FPT\n• Nền tảng: Python 3.11 • Streamlit • Plotly 3D • AI RAG\n• Kho mã nguồn: github.com/baonamv200/nasa"
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 2: VẤN ĐỀ THỰC TIỄN
# ==============================================================================
s2_notes = """Trên Trái Đất, trọng lực sinh ra lực đẩy nổi giúp ngọn lửa bốc lên trên và tỏa nhiệt; nhưng trong vi trọng lực, lửa cuộn thành khối cầu xanh tĩnh lặng và cháy âm ỉ mà cảm biến quang học thông thường rất khó phát hiện. Nguy hiểm hơn, hệ thống thông gió bắt buộc trên tàu vũ trụ vô tình biến thành nguồn thổi oxy liên tục, kích hoạt đám cháy bùng phát dữ dội mà không có lối thoát hiểm."""
s2 = create_slide(s2_notes)
add_header(s2, "TẠI SAO LỬA NGOÀI KHÔNG GIAN LÀ CƠN ÁC MỘNG?", "PHYSICS PARADOX & THREATS", 2)

c_e = add_card(s2, Inches(0.8), Inches(1.7), Inches(5.65), Inches(3.6), bg=RGBColor(24, 20, 38), border=RGBColor(120, 60, 20))
tfe = c_e.text_frame
tfe.word_wrap = True
tfe.margin_left = tfe.margin_right = Inches(0.35)
tfe.margin_top = Inches(0.25)
p = tfe.paragraphs[0]
p.text = "TRÁI ĐẤT (1.0g) - ĐỐI LƯU TỰ NHIÊN"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = AMBER_WARN
p = tfe.add_paragraph()
p.text = "Ngọn lửa giọt nước thuôn nhọn (L/W ≈ 3.2)"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfe.add_paragraph()
p.text = "• Lực đẩy nổi kéo khí nóng lên trên, tạo đối lưu hút oxy mới vào đáy.\n• Nhiệt độ đỉnh ~1850 K, muội than phát sáng vàng cam rực rỡ.\n• Dễ phát hiện sớm qua cảm biến quang học và dập tắt bằng nước."
p.font.name = FONT_BODY
p.font.size = Pt(17)
p.font.color.rgb = TEXT_MUTED

# Flame Shape (Upward Triangle + Oval Base)
f_shape = s2.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(5.2), Inches(2.2), Inches(1.0), Inches(1.6))
f_shape.fill.solid()
f_shape.fill.fore_color.rgb = AMBER_WARN
f_shape.line.color.rgb = RGBColor(220, 80, 20)

c_s = add_card(s2, Inches(6.88), Inches(1.7), Inches(5.65), Inches(3.6), bg=RGBColor(10, 28, 64), border=CYAN_ACCENT)
tfs = c_s.text_frame
tfs.word_wrap = True
tfs.margin_left = tfs.margin_right = Inches(0.35)
tfs.margin_top = Inches(0.25)
p = tfs.paragraphs[0]
p.text = "VI TRỌNG LỰC (0.0g) - KHUẾCH TÁN 3D"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfs.add_paragraph()
p.text = "Khối cầu lửa xanh đối xứng (L/W ≈ 1.0)"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfs.add_paragraph()
p.text = "• Triệt tiêu hoàn toàn lực đẩy nổi; oxy cung cấp bằng khuếch tán phân tử.\n• Nhiệt độ ~1380 K, không có muội than, ngọn lửa xanh mờ vô hình.\n• Cháy âm ỉ cực kỳ bền bỉ và không có đối lưu tự làm mát."
p.font.name = FONT_BODY
p.font.size = Pt(17)
p.font.color.rgb = TEXT_MUTED

# Circle Sphere Shape
c_shape = s2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.3), Inches(2.3), Inches(1.4), Inches(1.4))
c_shape.fill.solid()
c_shape.fill.fore_color.rgb = RGBColor(11, 61, 145)
c_shape.line.color.rgb = CYAN_ACCENT
c_shape.line.width = Pt(2)

b_card = add_card(s2, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.5), bg=RGBColor(26, 16, 26), border=NASA_RED)
tf_b = b_card.text_frame
tf_b.word_wrap = True
tf_b.margin_left = tf_b.margin_right = Inches(0.35)
tf_b.margin_top = Inches(0.2)
p = tf_b.paragraphs[0]
p.text = "HAI HIỂM HỌA KHÔNG GIAN ĐẶC BIỆT: NGỌN LỬA LẠNH & NGHỊCH LÝ THÔNG GIÓ"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NASA_RED
p = tf_b.add_paragraph()
p.text = "1. Ngọn lửa lạnh (Cool Flames): Cháy âm ỉ ở 500–800 K không phát sáng quang học nhưng xả lượng lớn khí độc CO.\n2. Nghịch lý thông gió: Quạt gió cabin (5–20 cm/s) cấp oxy cưỡng bức, làm vật liệu bùng cháy ở mức oxy thấp hơn mặt đất."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 3: THÁCH THỨC DỮ LIỆU
# ==============================================================================
s3_notes = """Để có được vài giây dữ liệu đốt cháy ngoài vũ trụ, NASA đã phải phóng các phòng thí nghiệm triệu đô như SoFIE hay đốt cháy cả con tàu chở hàng Cygnus trong dự án Saffire. Tuy nhiên, khối dữ liệu khổng lồ này lại tồn tại dưới dạng các file thô rời rạc, khiến các kỹ sư hàng không vũ trụ và người học rất khó khai thác một cách trực quan và tức thời."""
s3 = create_slide(s3_notes)
add_header(s3, "THÁCH THỨC DỮ LIỆU: KHO TÀNG NASA PSI BỊ RỜI RẠC", "MISSION DATA GAP", 3)

c3_w = Inches(3.65)
c3_h = Inches(3.6)
gap3 = Inches(0.4)
top3 = Inches(1.7)

cs1 = add_card(s3, Inches(0.8), top3, c3_w, c3_h)
tfs1 = cs1.text_frame
tfs1.word_wrap = True
tfs1.margin_left = tfs1.margin_right = Inches(0.3)
tfs1.margin_top = Inches(0.25)
p = tfs1.paragraphs[0]
p.text = "EXPERIMENT 01 // ISS CIR"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfs1.add_paragraph()
p.text = "NASA SoFIE"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfs1.add_paragraph()
p.text = "sofie_pmma_burn_rates.csv\n\n• Đốt thanh polyme PMMA trong buồng CIR trên trạm ISS.\n• Biến thiên gió cưỡng bức 0–50 cm/s.\n• Thách thức: Đa kênh, phi tuyến tính."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

cs2 = add_card(s3, Inches(0.8) + c3_w + gap3, top3, c3_w, c3_h)
tfs2 = cs2.text_frame
tfs2.word_wrap = True
tfs2.margin_left = tfs2.margin_right = Inches(0.3)
tfs2.margin_top = Inches(0.25)
p = tfs2.paragraphs[0]
p.text = "EXPERIMENT 02 // CYGNUS"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfs2.add_paragraph()
p.text = "NASA Saffire"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfs2.add_paragraph()
p.text = "saffire_pressure_oxygen.csv\n\n• Đốt cháy tấm vải quy mô lớn 1.0 mét trên tàu chở hàng Cygnus.\n• Thử nghiệm suy giảm áp suất.\n• Thách thức: File thô rất lớn, khó bao quát."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

cs3 = add_card(s3, Inches(0.8) + (c3_w + gap3)*2, top3, c3_w, c3_h)
tfs3 = cs3.text_frame
tfs3.word_wrap = True
tfs3.margin_left = tfs3.margin_right = Inches(0.3)
tfs3.margin_top = Inches(0.25)
p = tfs3.paragraphs[0]
p.text = "EXPERIMENT 03 // EXTINCTION"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfs3.add_paragraph()
p.text = "BASS-II & FLEX"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfs3.add_paragraph()
p.text = "bass_extinction_limits.csv\n\n• Giới hạn oxy dập tắt tối thiểu (MOC/LOI) trên 15+ vật liệu phi hành.\n• Thách thức: Bảng số liệu tĩnh, thiếu mô hình động học 3D."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

bot3 = add_card(s3, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.5), bg=RGBColor(30, 18, 30), border=NASA_RED)
tf_bot = bot3.text_frame
tf_bot.word_wrap = True
tf_bot.margin_left = tf_bot.margin_right = Inches(0.35)
tf_bot.margin_top = Inches(0.2)
p = tf_bot.paragraphs[0]
p.text = "KHOẢNG CÁCH GIỮA DỮ LIỆU KHOA HỌC & AN TOÀN SINH MẠNG PHI HÀNH ĐOÀN"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NASA_RED
p = tf_bot.add_paragraph()
p.text = "• Kỹ sư mất nhiều tuần phân tích thủ công; phi hành đoàn không có hệ thống đánh giá tức thời trước chuyến bay.\n• Các tiêu chuẩn nghiêm ngặt NASA-STD-6001B nằm rải rác trong hàng trăm trang báo cáo PDF khó tiếp cận."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 4: GIẢI PHÁP "FLAMES IN FREEFALL"
# ==============================================================================
s4_notes = """Giải pháp của chúng tôi là 'Flames in Freefall' – một trung tâm chỉ huy số hóa biến dữ liệu thô của NASA thành bảng điều khiển trực quan sinh động. Chỉ bằng việc gạt các thanh trượt trọng lực, oxy hay áp suất, hệ thống sẽ tính toán ngay lập tức chỉ số rủi ro hỏa hoạn SFRS và tái hiện hành vi ngọn lửa trong từng môi trường cabin cụ thể từ trạm ISS tới Sao Hỏa."""
s4 = create_slide(s4_notes)
add_header(s4, "GIẢI PHÁP: TRẠM ĐIỀU HÀNH AN TOÀN HỎA HOẠN TÀU VŨ TRỤ", "OUR SOLUTION", 4)

# Left Column: Telemetry Simulator & Risk Dashboard
w_s4_l = Inches(6.8)
c_sim = add_card(s4, Inches(0.8), Inches(1.7), w_s4_l, Inches(5.3), bg=CARD_BG, border=CYAN_ACCENT)
tf_sim = c_sim.text_frame
tf_sim.word_wrap = True
tf_sim.margin_left = tf_sim.margin_right = Inches(0.35)
tf_sim.margin_top = Inches(0.25)
p = tf_sim.paragraphs[0]
p.text = "MISSION CONTROL // LIVE TELEMETRY SIMULATOR"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_sim.add_paragraph()
p.text = "Bảng Điều Khiển Vật Lý & Đánh Giá Rủi Ro Tức Thời"
p.font.name = FONT_HEADING
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

# 4 Non-overlapping Parameter Tiles
g_configs = [
    ("TRỌNG LỰC (GRAVITY)", "0.16 g", "Mặt Trăng (Moon)", CYAN_ACCENT, Inches(1.1), Inches(2.7)),
    ("NỒNG ĐỘ OXY (O₂)", "34.0 %", "Giàu dưỡng khí cabin", AMBER_WARN, Inches(4.3), Inches(2.7)),
    ("ÁP SUẤT KHOANG", "56.5 kPa", "0.56 atm tiêu chuẩn", TEXT_WHITE, Inches(1.1), Inches(3.85)),
    ("TỐC ĐỘ GIÓ QUẠT", "15.0 cm/s", "Gió cưỡng bức HVAC", CYAN_GLOW, Inches(4.3), Inches(3.85)),
]
for param, val, sub, col, gx, gy in g_configs:
    g_card = add_card(s4, gx, gy, Inches(3.0), Inches(1.0), bg=RGBColor(6, 14, 34), border=RGBColor(38, 72, 130))
    tf_g = g_card.text_frame
    tf_g.margin_left = tf_g.margin_top = Inches(0.12)
    p = tf_g.paragraphs[0]
    p.text = param
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_SUBTLE
    p = tf_g.add_paragraph()
    p.text = f"{val} ({sub})"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = col

# Big Risk Meter Card (Bottom Left)
r_card = add_card(s4, Inches(1.1), Inches(5.05), Inches(6.2), Inches(1.65), bg=RGBColor(30, 10, 20), border=NASA_RED)
tf_r = r_card.text_frame
tf_r.margin_left = tf_r.margin_top = Inches(0.2)
p = tf_r.paragraphs[0]
p.text = "SPACE FIRE RISK SCORE (SFRS): 78.5 / 100"
p.font.name = FONT_MONO
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NASA_RED
p = tf_r.add_paragraph()
p.text = "CẢNH BÁO NGUY HIỂM CAO [CRITICAL] - NGUY CƠ BÙNG PHÁT"
p.font.name = FONT_HEADING
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tf_r.add_paragraph()
p.text = "• Luồng thông gió cưỡng bức 15 cm/s kích hoạt đối lưu nhân tạo.\n• Bebo Ignis-0G chỉ định ngắt quạt hút cabin (HVAC Isolation) tại T+0s."
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.color.rgb = TEXT_MUTED

# Right Column: 6 Mission Presets
w_s4_r = Inches(4.5)
c_pre = add_card(s4, Inches(7.9), Inches(1.7), w_s4_r, Inches(5.3), bg=CARD_BG_ALT, border=CARD_BORDER)
tf_pre = c_pre.text_frame
tf_pre.word_wrap = True
tf_pre.margin_left = tf_pre.margin_right = Inches(0.35)
tf_pre.margin_top = Inches(0.25)
p = tf_pre.paragraphs[0]
p.text = "6 CẤU HÌNH BAY CHUẨN ĐỊNH"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

presets = [
    ("1. ISS Standard", "0.0g • 21% O2 • 101.3 kPa"),
    ("2. Artemis Lunar Cabin", "0.16g • 34% O2 • 56.5 kPa"),
    ("3. Moon Rover Habitat", "0.16g • 30% O2 • 70.3 kPa"),
    ("4. EVA Spacesuit Pre-breathe", "0.16g • 100% O2 • 29.6 kPa"),
    ("5. Mars Transit Flight", "0.38g • 26% O2 • 70.0 kPa"),
    ("6. Earth Ground Baseline", "1.0g • 21% O2 • 101.3 kPa")
]
for name, spec in presets:
    p = tf_pre.add_paragraph()
    p.text = f"\n{name}"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_pre.add_paragraph()
    p.text = f"  {spec}"
    p.font.name = FONT_MONO
    p.font.size = Pt(12)
    p.font.color.rgb = CYAN_GLOW

# ==============================================================================
# SLIDE 5: TÍNH NĂNG CỐT LÕI & CÔNG NGHỆ
# ==============================================================================
s5_notes = """Sức mạnh của hệ thống nằm ở 3 trụ cột: Khả năng mô phỏng 3D tương tác với Plotly; Thuật toán phân hạng an toàn cho hàng loạt vật liệu tàu vũ trụ; và đặc biệt là hệ thống AI RAG được huấn luyện từ chính các tài liệu kỹ thuật của NASA, giúp kỹ sư tra cứu phương án phản ứng khẩn cấp chỉ trong vài mili-giây."""
s5 = create_slide(s5_notes)
add_header(s5, "TÍNH NĂNG CỐT LÕI & NGĂN XẾP CÔNG NGHỆ", "ENGINEERING CAPABILITIES", 5)

p_w = Inches(3.65)
p_gap = Inches(0.4)
p_h = Inches(4.0)

# Pillar 1: Physics 3D
cp1 = add_card(s5, Inches(0.8), Inches(1.7), p_w, p_h)
tf_cp1 = cp1.text_frame
tf_cp1.word_wrap = True
tf_cp1.margin_left = tf_cp1.margin_right = Inches(0.3)
tf_cp1.margin_top = Inches(0.25)
p = tf_cp1.paragraphs[0]
p.text = "01 // VẬT LÝ & PLOTLY 3D"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_cp1.add_paragraph()
p.text = "Mô Phỏng Động Học 3D"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tf_cp1.add_paragraph()
p.text = "• Đường cong dập tắt U-Curve: Tách bạch Quenching bức xạ vs Thổi tắt đối lưu.\n• Tính trường nhiệt độ 3D theo dòng gió quạt.\n• Tính MOC hiệu dụng theo thời gian thực."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# Pillar 2: Materials
cp2 = add_card(s5, Inches(0.8) + p_w + p_gap, Inches(1.7), p_w, p_h)
tf_cp2 = cp2.text_frame
tf_cp2.word_wrap = True
tf_cp2.margin_left = tf_cp2.margin_right = Inches(0.3)
tf_cp2.margin_top = Inches(0.25)
p = tf_cp2.paragraphs[0]
p.text = "02 // NASA PSI DATA PIPELINE"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_cp2.add_paragraph()
p.text = "Xếp Hạng Vật Liệu"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tf_cp2.add_paragraph()
p.text = "• Đánh giá an toàn 15+ vật liệu phi hành (PMMA, Nomex, Kapton, Delrin, Kydex...).\n• Tuân thủ nghiêm ngặt NASA-STD-6001B.\n• Cảnh báo sớm polyme dễ bùng cháy."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# Pillar 3: AI RAG
cp3 = add_card(s5, Inches(0.8) + (p_w + p_gap)*2, Inches(1.7), p_w, p_h)
tf_cp3 = cp3.text_frame
tf_cp3.word_wrap = True
tf_cp3.margin_left = tf_cp3.margin_right = Inches(0.3)
tf_cp3.margin_top = Inches(0.25)
p = tf_cp3.paragraphs[0]
p.text = "03 // AI RAG VECTOR SEARCH"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_cp3.add_paragraph()
p.text = "Trợ Lý Cứu Hỏa Vũ Trụ"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tf_cp3.add_paragraph()
p.text = "• Vector TF-IDF Cosine Similarity siêu nhẹ, thời gian phản hồi < 4ms.\n• Lập chỉ mục 14 báo cáo kỹ thuật NASA.\n• Trích dẫn trang, tác giả & hướng dẫn dập lửa."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# Bottom Tech Stack Ribbon
ts_ribbon = add_card(s5, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.1), bg=CARD_BG_ALT, border=CARD_BORDER)
tf_ts = ts_ribbon.text_frame
tf_ts.margin_left = Inches(0.35)
tf_ts.margin_top = Inches(0.15)
p = tf_ts.paragraphs[0]
p.text = "NGĂN XẾP CÔNG NGHỆ CHÍNH // TECH STACK:"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_ts.add_paragraph()
p.text = "Python 3.11  •  Streamlit Core  •  Plotly Interactive 3D  •  NumPy & Pandas  •  Scikit-Learn TF-IDF  •  NASA WDS UI"
p.font.name = FONT_HEADING
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 6: KIẾN TRÚC HỆ THỐNG
# ==============================================================================
s6_notes = """Về mặt kiến trúc, dự án vận hành theo một luồng xử lý 4 tầng khép kín: Dữ liệu thô từ NASA được đưa vào động cơ Bebo Ignis-0G để giải các phương trình nhiệt động học; kết quả được đối chiếu qua Vector Database tài liệu và hiển thị trực quan lên giao diện Streamlit Cloud, sẵn sàng xuất báo cáo nhiệm vụ cho phi hành đoàn."""
s6 = create_slide(s6_notes)
add_header(s6, "KIẾN TRÚC HỆ THỐNG: LUỒNG DỮ LIỆU ĐẾN PHẢN ỨNG KHẨN CẤP", "HOW IT WORKS", 6)

st_w = Inches(2.7)
st_gap = Inches(0.31)
stages = [
    ("TẦNG 01", "INGESTION LAYER", "Dữ liệu NASA PSI", "• Ingest CSV thô (SoFIE, Saffire, BASS-II)\n• Cache dữ liệu hàng không dự phòng\n• Chuẩn hóa đơn vị đo đạc SI vũ trụ"),
    ("TẦNG 02", "PHYSICS ENGINE", "Bebo Ignis-0G", "• Giải phương trình khuếch tán MOC\n• Tỷ số Grashof & Richardson\n• Tính điểm nguy cơ SFRS (0–100)\n• Phát hiện ngọn lửa lạnh Cool Flames"),
    ("TẦNG 03", "AI VECTOR RAG", "NASA Vector DB", "• Vector TF-IDF 14 báo cáo kỹ thuật\n• Tìm kiếm đối sánh Cosine Similarity\n• Cầu nối Gemini 2.5 Flash / OpenAI\n• Tạo hướng dẫn phản ứng khẩn cấp"),
    ("TẦNG 04", "MISSION CONTROL", "Giao diện & Xuất bản", "• Dashboard Streamlit Cloud\n• Biểu đồ Plotly 3D nhiệt độ\n• Ma trận phản ứng dập lửa tức thời\n• Xuất Dossier JSON/Markdown có chữ ký")
]

for i, (t_num, t_name, t_sub, t_desc) in enumerate(stages):
    st_card = add_card(s6, Inches(0.8) + i * (st_w + st_gap), Inches(1.7), st_w, Inches(3.5), bg=CARD_BG, border=CYAN_ACCENT if i==1 else CARD_BORDER)
    tf_s = st_card.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = Inches(0.2)
    tf_s.margin_top = Inches(0.2)
    p = tf_s.paragraphs[0]
    p.text = t_num
    p.font.name = FONT_MONO
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf_s.add_paragraph()
    p.text = t_name
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_s.add_paragraph()
    p.text = t_sub
    p.font.name = FONT_MONO
    p.font.size = Pt(12)
    p.font.color.rgb = CYAN_GLOW
    p = tf_s.add_paragraph()
    p.text = f"\n{t_desc}"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

# Bottom Protocol
bot_p = add_card(s6, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.6), bg=RGBColor(30, 12, 20), border=NASA_RED)
tf_bp = bot_p.text_frame
tf_bp.word_wrap = True
tf_bp.margin_left = tf_bp.margin_right = Inches(0.35)
tf_bp.margin_top = Inches(0.2)
p = tf_bp.paragraphs[0]
p.text = "QUY CHUẨN CỨU HỎA KHẨN CẤP ĐƯỢC TỰ ĐỘNG HÓA // EMERGENCY SUPPRESSION MATRIX"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NASA_RED
p = tf_bp.add_paragraph()
p.text = "1. T+0s: Ngắt quạt gió (HVAC Isolation) nhằm triệt tiêu đối lưu cưỡng bức.\n2. Cấm tuyệt đối: Tia nước áp lực cao (High-velocity jets) tránh làm văng polyme nóng chảy.\n3. Chỉ định phương án chuẩn: Phun sương nước siêu mịn (Fine Water Mist < 50 µm) hoặc xả ngập khí CO2."
p.font.name = FONT_BODY
p.font.size = Pt(15)
p.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 7: Ý NGHĨA & TÁC ĐỘNG
# ==============================================================================
s7_notes = """Flames in Freefall không chỉ là một công cụ phân tích dữ liệu, mà là cẩm nang an toàn sống còn. Dự án giúp các nhà thiết kế tàu vũ trụ ngăn chặn nguy cơ cháy từ khâu chọn vật liệu, cung cấp quy trình dập lửa chuẩn xác để bảo vệ các căn cứ tương lai trên Mặt Trăng và Sao Hỏa, đồng thời truyền cảm hứng khoa học dữ liệu tới cộng đồng STEM."""
s7 = create_slide(s7_notes)
add_header(s7, "Ý NGHĨA & TÁC ĐỘNG CHIẾN LƯỢC", "IMPACT & VALUE", 7)

i_w = Inches(3.65)
i_gap = Inches(0.4)
i_h = Inches(5.2)

# Card 1: Science
ci1 = add_card(s7, Inches(0.8), Inches(1.7), i_w, i_h)
tfi1 = ci1.text_frame
tfi1.word_wrap = True
tfi1.margin_left = tfi1.margin_right = Inches(0.3)
tfi1.margin_top = Inches(0.3)
p = tfi1.paragraphs[0]
p.text = "GIÁ TRỊ 01 // KHOA HỌC"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfi1.add_paragraph()
p.text = "Hiểu Sâu Cơ Chế Cháy Vi Trọng Lực"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfi1.add_paragraph()
p.text = "\n• Giải mã nghịch lý thông gió và hành vi phi tuyến tính khi triệt tiêu lực đẩy nổi.\n\n• Xác định chính xác vùng dập tắt bức xạ (Radiative Quenching) khi dòng gió < 3 cm/s.\n\n• Mô hình hóa ngọn lửa lạnh (Cool Flames 500–800 K) bổ sung nhiệt động học vũ trụ hiện đại."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# Card 2: Spacecraft Safety
ci2 = add_card(s7, Inches(0.8) + i_w + i_gap, Inches(1.7), i_w, i_h, bg=CARD_BG, border=CYAN_ACCENT)
tfi2 = ci2.text_frame
tfi2.word_wrap = True
tfi2.margin_left = tfi2.margin_right = Inches(0.3)
tfi2.margin_top = Inches(0.3)
p = tfi2.paragraphs[0]
p.text = "GIÁ TRỊ 02 // THỰC TIỄN VŨ TRỤ"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfi2.add_paragraph()
p.text = "Thiết Kế Tàu Vũ Trụ An Toàn Hơn"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfi2.add_paragraph()
p.text = "\n• Hỗ trợ trực tiếp cho sứ mệnh Artemis (Mặt Trăng) và Chuyến bay có người lái lên Sao Hỏa.\n\n• Giúp các tập đoàn hàng không lựa chọn vật liệu tối ưu theo tiêu chuẩn NASA-STD-6001B.\n\n• Cung cấp cẩm nang dập lửa khẩn cấp và thiết kế luồng gió cabin an toàn cho phi hành đoàn."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# Card 3: STEM Education
ci3 = add_card(s7, Inches(0.8) + (i_w + i_gap)*2, Inches(1.7), i_w, i_h)
tfi3 = ci3.text_frame
tfi3.word_wrap = True
tfi3.margin_left = tfi3.margin_right = Inches(0.3)
tfi3.margin_top = Inches(0.3)
p = tfi3.paragraphs[0]
p.text = "GIÁ TRỊ 03 // GIÁO DỤC STEM"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tfi3.add_paragraph()
p.text = "Mở Hóa Tri Thức Khoa Học Vũ Trụ"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p = tfi3.add_paragraph()
p.text = "\n• Dân chủ hóa dữ liệu nghiên cứu của NASA tới học sinh, sinh viên và lập trình viên toàn cầu.\n\n• Trải nghiệm học tập trực quan qua mô hình 3D thay vì các trang lý thuyết khô khan.\n\n• Truyền cảm hứng theo đuổi đam mê khám phá không gian và công nghệ AI phụng sự nhân loại."
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 8: ĐỊNH HƯỚNG PHÁT TRIỂN & KẾT LUẬN
# ==============================================================================
s8_notes = """Trong tương lai, chúng tôi sẽ tích hợp mạng nơ-ron vật lý PINNs và kết nối trực tiếp với cảm biến viễn thám trên trạm không gian để phát hiện cháy tự động. Mời quý vị quét mã QR để trải nghiệm sản phẩm trực tiếp và đóng góp vào kho mã nguồn mở của chúng tôi tại github.com/baonamv200/nasa. Xin chân thành cảm ơn!"""
s8 = create_slide(s8_notes)
add_header(s8, "ĐỊNH HƯỚNG PHÁT TRIỂN & KHO MÃ NGUỒN", "FUTURE ROADMAP & CONCLUSION", 8)

# Left: 3 Milestones
w8_l = Inches(6.8)
c_rd = add_card(s8, Inches(0.8), Inches(1.7), w8_l, Inches(5.3), bg=CARD_BG, border=CYAN_GLOW)
tf_rd = c_rd.text_frame
tf_rd.word_wrap = True
tf_rd.margin_left = tf_rd.margin_right = Inches(0.35)
tf_rd.margin_top = Inches(0.3)
p = tf_rd.paragraphs[0]
p.text = "LỘ TRÌNH PHÁT TRIỂN CHIẾN LƯỢC 2026–2027"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_rd.add_paragraph()
p.text = "Hướng Đi Nâng Tầm Hệ Thống"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

r_steps = [
    ("Giai đoạn 1: Mở rộng Dữ liệu Thực nghiệm từ ISS", "Tích hợp thêm SoFIE-GEL, SoFIE-MIST và cảm biến ảnh nhiệt đa phổ hồng ngoại."),
    ("Giai đoạn 2: Tối ưu Mô hình Machine Learning (PINNs)", "Huấn luyện mạng nơ-ron vật lý (Physics-Informed Neural Networks) dự đoán cháy theo mili-giây."),
    ("Giai đoạn 3: Kết nối Trực tiếp Cảm biến IoT Cabin", "Nhận luồng viễn thám trực tiếp từ trạm không gian để tự động phát hiện và cô lập khoang cháy.")
]
for st_t, st_d in r_steps:
    p = tf_rd.add_paragraph()
    p.text = f"\n• {st_t}"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_rd.add_paragraph()
    p.text = f"  {st_d}"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

# Right: Source Code CTA
w8_r = Inches(4.5)
c_gt = add_card(s8, Inches(7.9), Inches(1.7), w8_r, Inches(5.3), bg=RGBColor(11, 28, 64), border=CYAN_ACCENT)
tf_gt = c_gt.text_frame
tf_gt.word_wrap = True
tf_gt.margin_left = tf_gt.margin_right = Inches(0.35)
tf_gt.margin_top = Inches(0.3)
p = tf_gt.paragraphs[0]
p.text = "KHO MÃ NGUỒN CÔNG KHAI // OPEN SOURCE"
p.font.name = FONT_MONO
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p = tf_gt.add_paragraph()
p.text = "github.com/baonamv200/nasa"
p.font.name = FONT_MONO
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = CYAN_GLOW
p = tf_gt.add_paragraph()
p.text = "\nTHÔNG TIN TÁC GIẢ & BẢN QUYỀN:\n• Vũ Bảo Nam (Vu Bao Nam)\n• Bebo ZeroG-X • VBN Lab | THPT FPT\n• NASA Space Apps Challenge 2026"
p.font.name = FONT_BODY
p.font.size = Pt(14)
p.font.color.rgb = TEXT_WHITE
p = tf_gt.add_paragraph()
p.text = "\nTRẢI NGHIỆM TRỰC TUYẾN:\n• flames-in-freefall.streamlit.app\n• Giấy phép mã nguồn mở MIT"
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.color.rgb = TEXT_MUTED
p = tf_gt.add_paragraph()
p.text = "\nCẢM ƠN QUÝ BAN GIÁM KHẢO!"
p.font.name = FONT_HEADING
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

# Safe file saving
out_name = "Flames_in_Freefall_Presentation_v3.pptx"
prs.save(out_name)
print(f"SUCCESS: Saved {out_name}")
