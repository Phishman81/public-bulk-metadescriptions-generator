import streamlit as st
import pandas as pd
import openai
import base64
import sys

# Main page title
st.title("Auto Metadescriptions Generator")

#Description
st.markdown("""
#### This application is specifically designed to streamline the process of auto-generating meta descriptions for your website in bulk. Offering you a choice to either:
- Generate meta descriptions for all valid pages,
- Focus solely on SEO relevant pages (i.e., the indexable ones),
- Even better: target URLs missing descriptions.

###### How to Use:
- Upload a CSV file from Screaming Frog SEO Spider containing your site's URLs.
- Select the necessary parameters for processing.

###### Automatic Exclusion and Page Type Definition:
Automatically excluding irrelevant URLs like scripts and images.
By analyzing the url, current title - and if available, H1 and meta description - the application defines the page type for each URL to enhance the understanding of potential user intent.

###### Final Output:
Upon completion, auto-generates an improved CSV file populated with improved meta descriptions.
""")

# User inputs OpenAI Key
openai_key = st.text_input("Enter OpenAI Key", type="password")

# Proceed with processing only if OpenAI Key is provided
if openai_key:  
    # File upload
    file = st.file_uploader("Upload a CSV File", type=['csv'])

    if file is not None:
        st.write("Uploaded file is being processed...")
        st.write("Filtering for 'text/html' URLs and excluding image URLs...")
        df = pd.read_csv(file)

        try:
            required_columns = ['Address', 'Title 1', 'Meta Description 1', 'Content Type']
            valid_csv = all(col in df.columns for col in required_columns)

            if not valid_csv:
                missing_columns = [col for col in required_columns if col not in df.columns]
                missing_columns_str = ', '.join(missing_columns)
                st.error(f"Invalid CSV file. It is missing the following columns: {missing_columns_str}.")
                sys.exit()

            if 'Content Type' in df.columns:
                if df['Content Type'].str.contains('text/html').any():                
                    df = df[~df['Address'].str.contains('image/svg\+xml|\.jpeg|\.jpg|\.gif|\.png|\.svg|\.bmp|\.tiff|\.webp|\.heic|\.ico|\.psd|\.ai|\.eps$', regex=True)]

                    option_1 = st.selectbox('Choose URLs category:', ('All URLs', 'SEO Relevant URLs'))
                    option_2 = st.selectbox('Choose optimization category:', ('All Descriptions', 'Only Missing Descriptions'))

                    if option_1 == 'All URLs' and option_2 == 'All Descriptions':
                        pass

                    ...

                    if df.empty:
                        if option_2 == 'Optimize Only Missing Meta Descriptions':
                            st.warning("There are no missing Meta Descriptions in your selection.")
                        else:
                            st.warning("No URLs matching the conditions were found.")
                        sys.exit()

                else:
                    st.warning("No URLs with 'text/html' content type found in the CSV.")
                    sys.exit()

                st.write(f"Total URLs to be processed: {len(df)}")

                start_button = st.button(f"Start Processing {len(df)} URLs")

                if start_button:
                    df['pagetype'] = ''

                    openai.api_key = openai_key # Set OpenAI Key

                    page_types = ['Home Page', 'Product Detail Page', 'Category Page',
                                'About Us Page', 'Contact Us Page', 'Blog Article Page',
                                'Services Page', 'Landing Page', 'Privacy Policy Page',
                                'Terms and Conditions Page', 'FAQ Page', 'Testimonials Page',
                                'Portfolio Page', 'Case Study Page', 'Press Release Page',
                                'Events Page', 'Resources/Downloads Page', 'Team Members Page',
                                'Careers/Jobs Page', 'Login/Register Page', 'E-commerce shopping cart page',
                                'Forum/community page', 'News Page']

                    ...

                    st.write("Generating new metadescriptions for every URL... Please wait.")
                    df['new_metadescription'] = ''

                    for i in range(len(df)):
                        ...

                    st.write("Result - Processed URLs with their Pagetypes and New Metadescriptions:")
                    ...
                    st.success("Metadescriptions have been created successfully! You can download the updated CSV below.")
                    ...
                ...

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display Error if no OpenAI Key Provided
else: 
    st.error("Please provide an OpenAI key.")
