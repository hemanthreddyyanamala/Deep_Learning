import streamlit as st
import cv2
from PIL import Image
import numpy as np
from streamlit_image_comparison import image_comparison
img=st.file_uploader(label="upload image", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, max_upload_size=None, disabled=False, label_visibility="visible", width="stretch")

if img:
    img = Image.open(img)
    npimg=np.array(img)
    eimg=img

    with st.sidebar:
        with st.expander('resize'):
            col1, col2 = st.columns(2)
            with col1:
                x=st.number_input(label='Width', min_value=1, max_value=None, value=700, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width=50, bind=None)
            with col2:
                y=st.number_input(label='Height', min_value=1, max_value=None, value=700, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width=50, bind=None)
        
        with st.expander('COLOR FILTERS'):
            ft=st.selectbox("Filter type",["Original", "Grayscale", "Blur"])
        with st.expander('COOL OR WORM'):
            r=st.slider(label='worm/cool', min_value=1, max_value=225, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible", width="stretch", bind=None)
            b=255-r
            #g=r-b
            btn_warm=st.button("apply_warm_levels")
        with st.expander('brightness/contrast'):
            cont=st.slider("contrast",min_value=0.0,max_value=3.0)
            brig=st.slider("Brightness",min_value=-127,max_value=127)
            btn_brig=st.button("apply_cont_brightness")
        with st.expander('blur'):
            bv=st.slider("blur_levels",min_value=1,max_value=x,step=2)
            blur_btn=st.button("apply_blur")
        with st.expander('portrait-style'):
           pass

        with st.expander('sharpen-effects'):
            strength = st.slider("Sharpen", 0, 200, 50)
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], dtype=np.float32)
            btn_sharpen=st.button("apply_sharpen")
        with st.expander('edge_detection'):
            laplacian = cv2.Laplacian(npimg, cv2.CV_64F)  # Detect edges
            edge_btn=st.button("apply_edge_detection")

        
        
    
    
    if ft=='Grayscale':
        eimg=cv2.cvtColor(np.array(img),cv2.COLOR_RGB2GRAY)
    elif ft=='Original':
        eimg=npimg
    
    #eimg=cv2.cvtColor(np.array(img))
    
    img=cv2.resize(npimg,(x,y))
    if btn_warm:
        rows, cols = img.shape[:2]
        eimg = cv2.addWeighted(img, 0.7, np.full((rows, cols, 3), (r, 100, b), dtype=np.uint8), 0.3, 0)
    if btn_brig:
        eimg = cv2.convertScaleAbs(npimg, alpha=cont, beta=brig)#beta=brightness,alpha=contrast
    if blur_btn:
        eimg=cv2.blur(npimg,(bv,bv))
    if btn_sharpen:
        eimg = cv2.filter2D(npimg, -1, kernel * (strength/100.0))
    if edge_btn:
        eimg = cv2.convertScaleAbs(laplacian)          # Convert to displayable image

    image_comparison(
    img1=img,
    img2=eimg,
    label1="original Image",
    label2="Edited Image",
    width=x,
    starting_position=50,
    show_labels=True,
    make_responsive=True,
    in_memory=True,
    )
    if st.button("Download Image"):
        cv2.imwrite('output.png',img)
    

