import streamlit as st
import altair as alt
import pandas as pd
from price_index_data import price_index # 各項目とその比率を定義

expense_items = [
    ('住居費', 0.12),
    ('食費', 0.08),
    ('水道光熱費', 0.04),
    ('通信費', 0.04),
    ('教育費', 0.04),
    ('生命保険料', 0.02),
    ('自動車関連費', 0.01),
    ('生活日用品費', 0.03),
    ('医療費', 0.02),
    ('交通費', 0.03),
    ('被服費', 0.03),
    ('交際費', 0.04),
    ('娯楽費', 0.03),
    ('小遣い', 0.03),
    ('その他', 0.02),
    ('預貯金', 0.05)
]


# 共通の生活費計算ロジックを外部関数として分離
def calculate_expenses(income, family_size, prefecture):
    # 物価比率の計算
    price_ratio = price_index.get(prefecture, 1.0)
    tokyo_price_ratio = price_index.get("東京")
    price_ratio_multiplier = tokyo_price_ratio / price_ratio
    
    # 各項目の計算
    def calculate_item_ratio(base_ratio, family_threshold=1):
        ratio = base_ratio
        ratio += family_size * 0.01  # 家族が1人増えるごとに0.01ずつ増加
        return round(income * ratio * price_ratio / 1, 1)
    
    # 各項目の金額を計算
    expenses_data = {
        '項目': [item[0] for item in expense_items],
        '金額 (万円)': [round(calculate_item_ratio(item[1]), 1) for item in expense_items]
    }

    expenses_df = pd.DataFrame(expenses_data)
    
    # 必要な生活費の合計を計算
    total_expenses = expenses_df['金額 (万円)'].sum()
    
    # 月収を比較してアラートを表示
    if total_expenses > income:
        st.warning("生活費がオーバーしました.")

    # Calculate and display the overall income ratio
    overall_income_ratio = (expenses_df['金額 (万円)'].sum() / income) * 100
    st.write(f"現在の収入比率は {overall_income_ratio:.1f} %")
    
    return expenses_df, price_ratio, price_ratio_multiplier


def format_as_wan_yen(value):
    return f'{value:.1f} 万円'

def format_as_percentage(value):
    return f'{value:.1f} %'

# Streamlitアプリのタイトル
st.title('生活費計算ツール')

# サイドバーの入力項目
income = st.sidebar.number_input('世帯月収（万円）', 0, 1000, 30, 1)  # 修正：30万円からスタート
family_size = st.sidebar.number_input('家族人数', 1, 10, 2, 1)  # 修正：デフォルトを2人に

# 都道府県のセレクトボックスを作成
# 都道府県名のリストは、あなたの`price_index`辞書のキーから取得します
prefecture = st.sidebar.selectbox('住んでいる都道府県', list(price_index.keys()))

# 選択された都道府県が`price_index`辞書に存在するか確認します
if prefecture in price_index:
    expenses_df, price_ratio, price_ratio_multiplier = calculate_expenses(income, family_size, prefecture)

    # Calculate ratio percentage for each expense
    expenses_df['比率（%）'] = (expenses_df['金額 (万円)'] / income) * 100

    # Display expenses and the updated data frame
    st.write("### 生活費の詳細")
    expenses_df_display = expenses_df.copy()
    expenses_df_display['金額 (万円)'] = expenses_df_display['金額 (万円)'].apply(format_as_wan_yen)
    expenses_df_display['比率（%）'] = expenses_df_display['比率（%）'].apply(format_as_percentage)
    st.table(expenses_df_display)

    chart = (
        alt.Chart(expenses_df)
        .mark_bar()
        .encode(
            x='項目',
            y='金額 (万円)',
            color='項目'
        )
    )
    st.write("### 生活費の内訳（棒グラフ）")
    st.altair_chart(chart, use_container_width=True)  # この行を修正

    # 選択した都道府県と東京都の比較情報を表示
    st.write(f"選択した都道府県（{prefecture}）の物価比率（東京対選択地域）: {price_ratio:.1f} 倍")
else:
    st.write("都道府県が見つかりません。正しい都道府県名を入力してください.")
