import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.header("Whatsapp Chat Analyzer")
st.sidebar.subheader("Created by [**Rohan Choudhary**](%s)" % 'https://www.linkedin.com/in/rohanchoudhary12/')
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if user_list.count('group_notification'):
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox('Show analysis WRT', user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        st.markdown("***")

        num_messages, total_words, num_media_messages, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        st.markdown("***")

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(total_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(len(links))

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("***")

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("***")

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("***")

        st.title("Hourly activity heatmap")
        activity_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':

            st.markdown("***")

            st.title('Most active users')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.markdown("***")

        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.markdown("***")

        st.title('Most Used Words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.markdown("***")

        st.title("Emoji analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
else:
    st.subheader("Please upload txt file by following below steps:")
    st.markdown("- Click on the chat and open it.")
    st.markdown("- Click 3 dots icon present at top right of chat screen.")
    st.markdown("- Click export chat.")
    st.markdown("- Choose without media and download txt file.")
    st.markdown("- Now upload it.")

st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)