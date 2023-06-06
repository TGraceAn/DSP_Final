import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Dùng để cập nhật lại bảng liên tục
plt.ion()

# Khởi tạo stream từ microphone
CHUNK = 3024  # số mẫu audio trong mỗi chunk
RATE = 44100  # số mẫu audio trên giây
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Tạo biến cho miền tần số
freqs = np.fft.rfftfreq(CHUNK, d=1./RATE)

# Khởi tạo figure cho matplotlib
fig, ax = plt.subplots(figsize=(8,6))
line, = ax.plot(freqs, np.zeros(len(freqs)), color='red')

# Thiết lập giá trị trục x,y
ax.set_xlim(40, 400)
ax.set_ylim(0, 10)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")

# Vẽ văn bản
text_pos = (380, 9)  # Vị trí vẽ văn bản
text_template = "Max: {:.2f} dB at {:.2f} Hz"  # Mẫu văn bản

# Tạo bộ lọc bandpass
lowcut = 40  # Tần số cắt thấp
highcut = 400  # Tần số cắt cao
fs = RATE  # Tần số lấy mẫu
order = 2  # Bậc của bộ lọc
nyquist = 0.5 * fs
low = lowcut / nyquist
high = highcut / nyquist
b, a = signal.butter(order, [low, high], btype='band')

while True:
    # Đọc data từ microphone và chuyển thành tín hiệu waveform
    data = stream.read(CHUNK)
    y = np.frombuffer(data, dtype=np.int16) / 32768.0

    # Lọc dữ liệu âm thanh bằng bộ lọc bandpass
    filtered_data = signal.lfilter(b, a, y)

    # Chuyển đổi sang miền tần số
    y_frequency = abs(np.fft.rfft(filtered_data))

    # Tìm giá trị cực đại
    max_index = np.argmax(y_frequency)
    max_freq = freqs[max_index]
    max_magnitude = y_frequency[max_index]

    # Cập nhật spectrum trên đồ thị matplotlib
    line.set_ydata(y_frequency)
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()

    max_freq
    print(max_freq)
    # Hiển thị giá trị cực đại trên đồ thị (vì có quá nhiều giá trị max có thể hiển thị trong 1s nên đây chỉ để
    #   kiểm tra xem giá trị max khi thu âm có xuất hiện hay ko)
    # text = text_template.format(max_magnitude, max_freq)
    # ax.text(*text_pos, text, ha='right', va='top', fontsize=10)

    # Thiết lập màu sắc của đồ thị
    # if 100 <= max_freq <= 200:
    #     line.set_color('green')


    if 81 <= max_freq <= 83:
        line.set_color('green')
    elif 109 <= max_freq <= 111:
        line.set_color('green')
    elif 146 <= max_freq <= 148:
        line.set_color('green')
    elif 195 <= max_freq <= 197:
        line.set_color('green')
    elif 246 <= max_freq <= 248:
        line.set_color('green')
    elif (max_freq >= 328) and (max_freq <= 330):
        line.set_color('green')

    else:
        line.set_color('red')

    plt.show()


