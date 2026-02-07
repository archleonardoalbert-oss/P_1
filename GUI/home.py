import streamlit as st
from pathlib import Path


def Inicio():
    st.session_state.Critic = False
    st.header('Bienvenido a LuxAlbert Hotel')
    st.video(
        'Media/Luxury.mp4',
        autoplay= True,
        loop= True,
        muted= True,
        ) 
    albun = [f'Media/{entry.name}' for entry in Path('Media').iterdir() if entry.is_file() and entry.name != '360_F_381799100_YOZ0uoR7Wz3YIGZHRYhEjlqTkGn8EMMd.jpg' and entry.name != 'Luxury.mp4']

    
    with st.container():
        st.markdown('<div class = "horizontal-gallery">', unsafe_allow_html= True)
        col1, col2, col3 = st.columns([1, 1, 1])
        max_col = len(albun) // 3
        for i in range(len(albun)):
            image = albun[i]
            if i <= max_col:
                with col1:
                    st.image(image, width= 400)
            elif max_col < i <= 2 * max_col:
                with col2:
                    st.image(image, width= 400)
            else:
                with col3:
                    st.image(image, width= 400)


        st.markdown('</div>', unsafe_allow_html= True)