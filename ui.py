import streamlit as st
import requests
import time

# Replace with your Vercel domain
base_url = 'http://localhost:3000'

def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()

def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()

def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_clip(clip_id):
    url = f"{base_url}/api/clip?id={clip_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_whole_song(clip_id):
    payload = {"clip_id": clip_id}
    url = f"{base_url}/api/concat"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

st.title("Audio Generation with API")

# Audio generation by prompt
st.header("Generate Audio by Prompt")
prompt = st.text_area("Enter your prompt here:")
make_instrumental = st.checkbox("Make instrumental", value=False)
wait_audio = st.checkbox("Wait for audio", value=False)

if st.button("Generate Audio"):
    with st.spinner("Generating audio..."):
        try:
            response = generate_audio_by_prompt({
                "prompt": prompt,
                "make_instrumental": make_instrumental,
                "wait_audio": wait_audio
            })
            ids = ",".join([item['id'] for item in response])
            st.write(f"Audio IDs: {ids}")
            for _ in range(60):
                data = get_audio_information(ids)
                if all(item["status"] == 'streaming' for item in data):
                    for item in data:
                        st.audio(item['audio_url'], format="audio/mp3")
                    break
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

# Fetch quota information
st.header("Quota Information")
if st.button("Get Quota Information"):
    try:
        quota_info = get_quota_information()
        st.write(quota_info)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Fetch clip information
st.header("Get Clip Information")
clip_id = st.text_input("Enter Clip ID:")
if st.button("Get Clip"):
    try:
        clip_info = get_clip(clip_id)
        st.write(clip_info)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Generate whole song
st.header("Generate Whole Song")
concat_clip_id = st.text_input("Enter Clip ID for Concatenation:")
if st.button("Generate Whole Song"):
    try:
        song_info = generate_whole_song(concat_clip_id)
        st.write(song_info)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Running the Streamlit app
if __name__ == "__main__":
    st.run()
