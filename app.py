import streamlit as st
import matchering as mg

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #000000;
    opacity: 0.8;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
# st.header("Medium")
  
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Streamlit UI
st.title('Cosmic Tune Master')
st.write('Please upload your target and reference audio files.')

# Upload the audio files
target_file = st.file_uploader("Choose a Target Audio File", type=['wav'])
reference_file = st.file_uploader("Choose a Reference Audio File", type=['wav'])

# Check if the files are uploaded
if target_file and reference_file:
    # Button to run Matchering
    if st.button('Process Audio'):
        # Temporarily save files
        target_path = 'target.wav'
        reference_path = 'reference.wav'

        with open(target_path, 'wb') as f:
            f.write(target_file.getbuffer())
        with open(reference_path, 'wb') as f:
            f.write(reference_file.getbuffer())

        # Process the audio
        with st.spinner('Processing the audio...'):
            try:
                # Muting non-warning outputs
                mg.log(warning_handler=print)

                mg.process(
                    target=target_path,
                    reference=reference_path,
                    results=[
                        mg.pcm16("my_song_master_16bit.wav"),
                        mg.pcm24("my_song_master_24bit.wav"),
                    ],
                    preview_target=mg.pcm16("preview_my_song.flac"),
                    preview_result=mg.pcm16("preview_my_song_master.flac"),
                )

                # Provide download links
                st.success("Processing complete!")
                st.markdown('[Download Processed Audio (16-bit)](my_song_master_16bit.wav)')
                st.markdown('[Download Processed Audio (24-bit)](my_song_master_24bit.wav)')

                # Add audio players with labels
                st.markdown('### Preview Original Track')
                st.audio('preview_my_song.flac', format='audio/flac', start_time=0)

                st.markdown('### Preview Mastered Track')
                st.audio('preview_my_song_master.flac', format='audio/flac', start_time=0)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")



