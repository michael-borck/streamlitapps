description = "QR Code"

# Your app goes in the function run()
def run():
    import segno
    import streamlit as st
    from PIL import Image

    st.title("QR Code")
    st.subheader('Enter text')

    input = st.text_input('','')
    if input != '':
        with st.spinner('Generating...'):
            qr = segno.make(input)
            qr.save('myqr.png', scale=9)
            img = Image.open('myqr.png')
            st.image(img)

# end of app

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
