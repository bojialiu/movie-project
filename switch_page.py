import streamlit as st

def page_switcher(page):
    st.session_state.runpage = page

def main():
    st.title('main')
    st.write('this is the main page rararararararara')
    st.text_input('text input')
    btn1 = st.button('goto page1',on_click=page_switcher,args=(page1,))
    btn2 = st.button('goto page2',on_click=page_switcher,args=(page2,))
    if btn1 or btn2:
        st.experimental_rerun() # rerun is needed to clear the page

def page1():
    st.title('page1')
    btn3 = st.button('go back')
    if btn3 :
        st.session_state.runpage = main
        st.experimental_rerun()

def page2():
    st.title('page2')
    btn4 = st.button('go back')
    if btn4 :
        st.session_state.runpage = main
        st.experimental_rerun()


if __name__ == '__main__':
    st.write("asdafasdf")
    if 'runpage' not in st.session_state :
        st.session_state.runpage = main
    st.session_state.runpage()
