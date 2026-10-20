# 🎵 KHO NHẠC TỰ ĐỘNG CHO ESP32 XIAOZHI AI

Kho lưu trữ và phát nhạc Việt trực tuyến cho Robot Trợ lý ảo ESP32 Xiaozhi.

## 🚀 Hướng dẫn thêm bài hát mới vào kho:

1. **Bước 1:** Tải bất kỳ bài hát yêu thích nào định dạng `.mp3` (từ Zing MP3, YouTube, NhacCuaTui...).
2. **Bước 2:** Chép các file `.mp3` đó vào thư mục:
   `Kho_nhac/nhac_mp3_goc/`
3. **Bước 3:** Nhấp đúp chuột chạy file:
   `chuyen_doi_va_day_len_github.bat`

Công cụ sẽ tự động:
- Nén file MP3 sang chuẩn **OGG Opus 16kHz** tối ưu hóa 100% cho loa robot Xiaozhi (chỉ nặng ~1MB/bài, tải cực nhanh không giật lag).
- Cập nhật danh sách từ khóa bài hát vào `playlist.json`.
- Tự động đẩy lên GitHub.

---

## 🗣️ Cách ra lệnh cho Xiaozhi:
- *"Xiaozhi ơi, mở bài [tên bài hát]"*
- *"Xiaozhi ơi, phát nhạc Lofi chill"*
- *"Mở một bài nhạc ngẫu nhiên"*
- **Dừng nhạc:** Chạm nhẹ vào cảm ứng trên đỉnh đầu robot!
