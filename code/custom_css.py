# Custom CSS to enforce dark theme with white text
DARK_THEME_CSS = """
* {
    color: #ffffff !important;
    background-color: #05191B !important;
}
img {
    filter: brightness(0.8) !important;  /* Ensure images are not too bright */
}
a {
    color: #bb86fc !important;
}
"""

LIGHT_THEME_CSS = """
* {
    color: #000000 !important;
    background-color: #FCDCEB !important;
}
img {
    filter: brightness(1) !important;  /* Ensure images are not too bright */
}
a {
    color: #6200ee !important;
}
"""

HIGHLIGHT_CSS = """

    .highlight-old {
        background-color: #ffcccc; 
        text-decoration: line-through;
    }
    .highlight-new {
        background-color: #ccffcc; 
        font-weight: bold;
    }

"""