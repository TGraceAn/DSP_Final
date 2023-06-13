import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Dùng để cập nhật lại bảng liên tục
plt.ion()

# Khởi tạo stream từ microphone
CHUNK = 4096  # số mẫu audio trong mỗi chunk
RATE = 44100  # số mẫu audio trên giây
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Tạo biến cho miền tần số
freqs = np.fft.rfftfreq(CHUNK, d=1./RATE)

# Khởi tạo figure cho matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# Thiết lập giá trị trục x,y cho FFT
ax1.set_xlim(40, 400)
ax1.set_ylim(-20, 40)
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Magnitude (dB)")
line_fft, = ax1.plot(freqs, np.zeros(len(freqs)), color='blue')

# Thiết lập giá trị trục x,y cho HPS
ax2.set_xlim(0, 2000)
ax2.set_ylim(-20, 40)
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude (dB)")
line_hps, = ax2.plot(freqs, np.zeros(len(freqs)), color='green')

# Tạo bộ lọc bandpass
lowcut = 16  # Tần số cắt thấp
highcut = 20000  # Tần số cắt cao
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
    y_frequency = 20*np.log10(abs(np.fft.rfft(filtered_data)))
    spectrum = abs(np.fft.rfft(filtered_data))

    # Tìm giá trị cực đại FFT
    max_index_fft = np.argmax(y_frequency)
    max_freq_fft = freqs[max_index_fft]
    max_magnitude_fft = y_frequency[max_index_fft]

    #Cal HPS
    hps = np.copy(spectrum)
    for factor in range(2, 6):
        downsampled = signal.decimate(spectrum, factor, zero_phase=True)
        hps[:len(downsampled)] += downsampled
    fundamental_index = np.argmax(hps)
    
    #Cal HPS
    # hps = np.copy(spectrum)
    # for h in range(2, 6):
    #     decimated = np.copy(y)[::h]
    #     spectrum_h = np.fft.rfft(decimated)
    #     hps[:len(spectrum_h)] *= abs(spectrum_h)

    # Tìm fundamental frequency
    fundamental_frequency = 44100 * fundamental_index / len(filtered_data)

    # Cập nhật spectrum trên đồ thị matplotlib FFT
    line_fft.set_ydata(y_frequency)
    ax1.draw_artist(ax1.patch)
    ax1.draw_artist(line_fft)

    # Cập nhật spectrum trên đồ thị matplotlib HPS
    line_hps.set_ydata(hps)
    ax2.draw_artist(ax2.patch)
    ax2.draw_artist(line_hps)

    fig.canvas.blit(ax1.bbox)
    fig.canvas.blit(ax2.bbox)
    fig.canvas.flush_events()

    # Hiển thị giá trị cực đại trên đồ thị


    
    # print("FFT", max_freq_fft)

    print("HPS", fundamental_frequency)
    if 81 <= fundamental_frequency <= 83:
        line_hps.set_color('green')
    elif 109 <= fundamental_frequency <= 111:
        line_hps.set_color('green')
    elif 146 <= fundamental_frequency <= 148:
        line_hps.set_color('green')
    elif 195 <= fundamental_frequency <= 197:
        line_hps.set_color('green')
    elif 246 <= fundamental_frequency <= 248:
        line_hps.set_color('green')
    elif (fundamental_frequency >= 328) and (fundamental_frequency <= 330):
        line_hps.set_color('green')

    else:
        line_hps.set_color('red')


    plt.show()
