import speech_recognition as sr

def get_working_mic():
    mics = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for i, mic_name in enumerate(mics):
        print(f"{i}: {mic_name}")

    for i in range(len(mics)):
        try:
            with sr.Microphone(device_index=i) as source:
                print(f"Using microphone {i}: {mics[i]}")
                return sr.Microphone(device_index=i)
        except Exception:
            continue
    raise RuntimeError("No working microphone found!")

def main():
    recognizer = sr.Recognizer()
    mic = get_working_mic()

    while True:
        try:
            with mic as source:
                print("🎙️ Listening... Speak now!")
                # Optional: You can adjust this or comment out if unstable
                # recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                # Manually set energy threshold to avoid instability
                recognizer.energy_threshold = 300

                audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
                print("📡 Audio captured, processing...")

            # Recognize speech using Google API
            text = recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")

            # Save to file
            with open("transcript.txt", "a", encoding="utf-8") as f:
                f.write(text + "\n")
                print("📝 Transcription saved.\n")

        except sr.WaitTimeoutError:
            print("⏱️ Timeout: No speech detected. Please speak louder or closer to the mic.")
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.RequestError as e:
            print(f"🔌 API error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")

if __name__ == "__main__":
    main()
