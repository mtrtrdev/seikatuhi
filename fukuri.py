import streamlit as st
import altair as alt
import pandas as pd

'''
複利計算処理
@param r: 利率（％）
@param s: 預金額（万円）
@param n: 期間（年）
@param a: 預金追加額（万円）
returns ret: 結果（万円）
'''
def fukuri (r, s, n, a):
    r = float(r * 0.001)
    i = 0;
    ret = []
    years = []
    ss = []
    strs = []
    increase = []
    rate = []
    while i < n:
        s = s + a
        s = s * (1 + r)
        i = i + 1
        years.append(i)
        ss.append(int(s))

        incr_v = float(int(s) - int(ss[i - 2]))
        increase.append(incr_v)
        rate_v = int(s) / int(ss[0]) * 100
        rate.append("{}％".format(round(rate_v)))

        strs.append("{}年後：{}万円".format(i, int(s)))
    ret.insert(0, years)
    ret.insert(1, ss)
    ret.insert(2, strs)
    ret.insert(3, increase) # 増加額
    ret.insert(4, rate) # 当初預金額からの増加率

    print(ret)

    return ret


'''
複利計算アプリ
画面描画
'''
st.title('預金複利計算ツール')

st.sidebar.write("""
# 預金額の複利計算

以下より各種オプションを設定可能
""")

st.sidebar.write("""
## 利率選択
""")
r = st.sidebar.slider('利率', 1, 10, 5)
st.write(f"""
### 利率： **{r}％**
""")

st.sidebar.write("""
## 預金金額選択
""")
# s = st.sidebar.slider('預金額', 1, 2000, 50)
s = st.sidebar.number_input('預金額', 0, 2000, 50, 1)
st.write(f"""
### 預金額： **{s}万円**
""")

st.sidebar.write("""
## 預金期間選択
""")
n = st.sidebar.slider('年数', 1, 100, 100)
st.write(f"""
### 預金期間： **{n}年間** 
""")

st.sidebar.write("""
## 預金追加金額選択
""")
# a = st.sidebar.slider('年間追加金額', 1, 200, 0)
a = st.sidebar.number_input('年間追加金額', 0, 200, 0, 1)
st.write(f"""
### 預金追加金額： **{a}万円** 
""")

st.sidebar.write("""
## 表示範囲指定
""")
ymin, ymax = st.sidebar.slider(
    '範囲を指定してください。',
    0.0, 20000.0, (0.0, 20000.0)
)

st.write("### ---------------------------------------------")

try:
    ret = fukuri(r,s,n,a)

    index = pd.DataFrame({'term': ret[0],
                'deposit':ret[1],
                'increrate':ret[3],
                'rate':ret[4],
                })
    st.write("### 預金結果一覧", index.sort_index())

    data = pd.DataFrame({'預金期間': ret[0],
                    '預金額':ret[1],
                    '結果':ret[2]})
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x='預金期間',
            y=alt.Y("預金額", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )
    st.write("### 預金残高グラフ")
    st.altair_chart(chart, use_container_width=True)

except:
    st.error(
        "処理内でエラーが発生しました。"
    )

