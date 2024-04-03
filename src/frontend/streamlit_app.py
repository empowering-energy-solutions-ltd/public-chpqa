import streamlit as st
from streamlit_objs import logged_in_content, login_box

from src.frontend.utils import TextSchema


def main():
  """ Generates streamlit app, allows login then displays content.
  """
  st.set_page_config(page_title=TextSchema.page_header,
                     page_icon=TextSchema.emoji)
  st.header(TextSchema.page_header + TextSchema.emoji)

  if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
  login_box()
  if st.session_state['logged_in']:
    logged_in_content()


if __name__ == "__main__":
  main()
