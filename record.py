import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Dùng để cập nhật lại bảng liên tục
plt.ion()

# Khởi tạo stream từ microphone
CHUNK = 1024  # số mẫu audio trong mỗi chunk
RATE = 44100  # số mẫu audio trên giây
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Tạo biến cho miền tần số
freqs = np.fft.rfftfreq(CHUNK, d=1./RATE)

# Khởi tạo figure cho matplotlib
fig, ax = plt.subplots(figsize=(8,6))
line, = ax.plot(freqs, np.zeros(len(freqs)))

# Thiết lập giá trị trục y
ax.set_ylim(0, 10)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")

while True:
    # Đọc data từ microphone và chuyển thành tín hiệu waveform
    data = stream.read(CHUNK)
    y = np.frombuffer(data, dtype=np.int16) / 32768.0

    # Chuyển đổi sang miền tần số
    yf = abs(np.fft.rfft(y))

    # Cập nhật spectrum trên đồ thị matplotlib
    line.set_ydata(yf)
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
    plt.show()