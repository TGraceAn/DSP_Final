import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time

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
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# Thiết lập giá trị trục x,y cho FFT
ax1.set_xlim(40, 5000)
ax1.set_ylim(0, 10)
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Magnitude (dB)")
line_fft, = ax1.plot(freqs, np.zeros(len(freqs)), color='blue')

# Thiết lập giá trị trục x,y cho HPS
ax2.set_xlim(0, 2000)
ax2.set_ylim(0, 10)
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
    y_frequency = abs(np.fft.rfft(filtered_data))
    y_hps = filtered_data

    # Tìm giá trị cực đại FFT
    max_index_fft = np.argmax(y_frequency)
    max_freq_fft = freqs[max_index_fft]
    max_magnitude_fft = y_frequency[max_index_fft]

    # Tính HPS bằng cách lấy tích chập của tín hiệu với các bản sao giảm dần
    # hps = np.copy(y_frequency)
    # for i in range(2, 5):
    #     decimated = signal.decimate(y_frequency, i)
    #     hps[:len(decimated)] *= decimated

    spectrum = abs(np.fft.rfft(y_hps))
    hps = np.copy(spectrum)
    for h in range(2, 6):
        decimated = np.copy(y)[::h]
        spectrum_h = np.fft.rfft(decimated)
        hps[:len(spectrum_h)] *= abs(spectrum_h)

    # Tìm giá trị cực đại HPS
    max_index_hps = np.argmax(hps)
    max_freq_hps = hps[max_index_hps]
    max_magnitude_hps = hps[max_index_hps]

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
    # text_fft = "FFT: Max: {:.2f} dB at {:.2f} Hz".format(max_magnitude_fft, max_freq_hps_fft)
    # text_hps = "HPS: Max: {:.2f} dB at {:.2f} Hz".format(max_magnitude_hps, max_freq_hps_hps)
    # ax1.text(380, 9, text_fft, ha='right', va='top', fontsize=10)
    # ax2.text(380, 9, text_hps, ha='right', va='top', fontsize=10)

    
    # print("FFT", max_freq_fft)

    print("HPS", max_freq_hps)
    if 81 <= max_freq_hps <= 83:
        line_hps.set_color('green')
    elif 109 <= max_freq_hps <= 111:
        line_hps.set_color('green')
    elif 146 <= max_freq_hps <= 148:
        line_hps.set_color('green')
    elif 195 <= max_freq_hps <= 197:
        line_hps.set_color('green')
    elif 246 <= max_freq_hps <= 248:
        line_hps.set_color('green')
    elif (max_freq_hps >= 328) and (max_freq_hps <= 330):
        line_hps.set_color('green')

    else:
        line_hps.set_color('red')


    plt.show()

#==============================================================================================================================================

# import pyaudio
# import numpy as np
# import matplotlib.pyplot as plt

# def record_audio(duration, sample_rate):
#     chunk_size = 1024
#     num_chunks = int(duration * sample_rate / chunk_size)

#     audio = np.zeros(num_chunks * chunk_size, dtype=np.float32)

#     p = pyaudio.PyAudio()
#     stream = p.open(format=pyaudio.paFloat32,
#                     channels=1,
#                     rate=sample_rate,
#                     input=True,
#                     frames_per_buffer=chunk_size)

#     print("Recording...")
#     for i in range(num_chunks):
#         data = stream.read(chunk_size)
#         audio[i * chunk_size: (i + 1) * chunk_size] = np.frombuffer(data, dtype=np.float32)

#     print("Finished recording.")

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     return audio

# def plot_spectrum(audio, sample_rate):
#     # Calculate the Harmonic Product Spectrum (HPS)
#     spectrum = np.fft.fft(audio)
#     hps = np.copy(spectrum)
#     for h in range(2, 4):
#         decimated = np.copy(audio)[::h]
#         spectrum_h = np.fft.fft(decimated)
#         hps[:len(spectrum_h)] *= abs(spectrum_h)

#     # Calculate the frequency axis
#     freq_axis = np.fft.fftfreq(len(audio), 1.0 / sample_rate)

#     # Plot the spectrum
#     plt.figure()
#     plt.plot(freq_axis[:len(hps) // 2], abs(hps[:len(hps) // 2]))
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Magnitude')
#     plt.title('Harmonic Product Spectrum')
#     plt.grid(True)
#     plt.show()

# # Thông số âm thanh ghi âm
# duration = 5  # Thời gian ghi âm (giây)
# sample_rate = 44100  # Tốc độ mẫu (samples per second)

# # Ghi âm
# audio = record_audio(duration, sample_rate)

# # Hiển thị biểu đồ tần số
# plot_spectrum(audio, sample_rate)