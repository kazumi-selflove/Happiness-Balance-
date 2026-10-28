# -*- coding: utf-8 -*-
"""
『男性性女性性の幸せバランス診断』(joy_checker_app-v3.py)

（ひとり恋愛メソッド）で明かされた深層ロジックを反映した最新バージョン。
・女性性の喜び：五感・身体感覚・受容・没頭（マインドフルネス）・感情の解放・受け取って味わう喜び
・男性性の喜び：行動・意志・目標達成・リスク/挑戦・決断・論理・与える喜び
・統合エネルギー：自ら行動・突破（男性性）し、その成果やプロセスを五感でじっくり受容・感謝（女性性）する調和の巡り

【使い方】
1. CLI実行: python joy_checker_app-v3.py
2. Streamlit Web実行: streamlit run joy_checker_app-v3.py
"""

import sys
import re

# 女性性のキーフレーズ・概念（五感・身体感覚・受容・没頭・感謝・うっとり）
FEMININE_PATTERNS = [
    r"もらった", r"受け取った", r"ご馳走", r"プレゼント", r"ギフト", r"うっとり",
    r"五感", r"感動", r"味わ", r"まったり", r"浸る", r"美しさ", r"美しい", r"心地よ",
    r"感謝", r"身を委ね", r"没頭", r"癒やし", r"トキメキ", r"安心", r"リラックス",
    r"ほっとした", r"ぬくもり", r"愛され", r"大切にされ", r"誘われ", r"共感", r"受け入れ",
    r"試着", r"景色", r"空間", r"音", r"香り", r"美味", r"おいし", r"快感", r"温かい"
]

# 男性性のキーフレーズ・概念（行動・意志・目標達成・挑戦/リスク・決断・論理・与える・承認）
MASCULINE_PATTERNS = [
    r"達成", r"成功", r"完成", r"クリア", r"合格", r"勝つ", r"勝った", r"契約",
    r"成果", r"解決", r"やり切", r"やり遂げ", r"稼いだ", r"売り上げ", r"目標",
    r"挑戦", r"自分で", r"自ら", r"購入した", r"買った", r"決断", r"任され",
    r"頼られ", r"突破", r"計画", r"行動", r"プレゼントした", r"与えた", r"教えた",
    r"導いた", r"作った", r"走った", r"行っ", r"ランニング", r"運動", r"撮っ", r"撮影",
    r"やり遂げた", r"努力", r"頑張っ"
]

def analyze_joy(text: str) -> dict:
    if not text or not text.strip():
        return {"error": "出来事を入力してください。"}

    fem_score = 0.0
    masc_score = 0.0

    fem_found = []
    masc_found = []

    for pattern in FEMININE_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            fem_score += len(matches)
            fem_found.extend(matches)

    for pattern in MASCULINE_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            masc_score += len(matches)
            masc_found.extend(matches)

    # 構造的文脈分析（受け取る・感じる＝女性性、自ら動く・作る・達成＝男性性）
    has_receptive = bool(re.search(r"(してもらった|してくれた|受け取った|くれた|ご馳走になった|うっとり|味わった|浸った|感動|美しい|心地よ)", text))
    has_active = bool(re.search(r"(してあげた|やってやった|達成|自分で|やり切った|決断|挑戦|買っ|走っ|行っ|撮っ|作っ)", text))

    if has_receptive:
        fem_score += 1.5
    if has_active:
        masc_score += 1.5

    total = fem_score + masc_score

    if total == 0:
        ratio_fem = 50.0
        ratio_masc = 50.0
    else:
        ratio_fem = round((fem_score / total) * 100, 1)
        ratio_masc = round((masc_score / total) * 100, 1)

    if ratio_fem >= 65.0:
        category = "女性性の喜び（受容・五感・身体感覚の解放）"
        summary = (
            "「受け取ること」「五感や身体感覚で味わうこと」「今この瞬間に没頭すること」によってココロとカラダを満たした喜びです。\n"
            "思考や成果にとらわれず、身体の感覚や感情を素直に開いて受け容れられている豊かな状態です。"
        )
        advice = (
            "【幸せを引き寄せるワンポイントアドバイス】\n"
            "極上の「受容力と感性」が発揮されています！\n"
            "受け取った感動や心地よさを身体いっぱいに味わい、「ありがとう♡」と素直な感謝のエネルギーとして循環させることで、"
            "さらに大きな豊かさや幸運を引き寄せる巡りが生まれます。"
        )
    elif ratio_masc >= 65.0:
        category = "男性性の喜び（行動・意志・達成のパワー）"
        summary = (
            "「目標を達成すること」「自ら行動・決断すること」「課題をクリアし成果を生み出すこと」で得られた喜びです。\n"
            "自分の中の意志や行動力が能動的に発揮され、力強く現実を動かした瞬間です。"
        )
        advice = (
            "【幸せを引き寄せるワンポイントアドバイス】\n"
            "あなたの中の「行動力・決断力」が見事に発揮されました！\n"
            "外部の評価だけに頼らず、「自分、本当によく頑張った！」と自らの努力と挑戦をしっかりと承認し、自分で自分を労ってあげることがさらなるエネルギーを高める鍵になります。"
        )
    else:
        category = "女性性と男性性の統合エネルギー（幸せのバランス循環）"
        summary = (
            "自ら能動的に行動・挑戦した男性性のパワーと、その成果やプロセスの感動を五感でじっくり受け容れて味わった女性性の感性が見事に響き合った、最高のバランスの喜びです。"
        )
        advice = (
            "【幸せを引き寄せるワンポイントアドバイス】\n"
            "「与える力・動く力（男性性）」と「受け取る力・感じる力（女性性）」が非常に心地よいバランスで巡っています！\n"
            "自分自身の行動や努力を称えつつ、受け取った感動や環境への感謝を深く噛み締めることで、最高の自己統合状態（内なる調和）を維持できます。"
        )

    share_text = (
        f"【男性性女性性の幸せバランス診断結果】\n"
        f"今日の出来事: 「{text}」\n"
        f"判定: {category}\n"
        f"・女性性: {ratio_fem}%\n"
        f"・男性性: {ratio_masc}%\n\n"
        f"▼解説\n{summary}\n\n"
        f"{advice}\n"
        f"#男性性女性性診断 #幸せバランス"
    )

    return {
        "input_text": text,
        "category": category,
        "ratio_fem": ratio_fem,
        "ratio_masc": ratio_masc,
        "fem_found": list(set(fem_found)),
        "masc_found": list(set(masc_found)),
        "summary": summary,
        "advice": advice,
        "share_text": share_text
    }

def run_streamlit():
    try:
        import streamlit as st
    except ImportError:
        return False

    st.set_page_config(page_title="男性性女性性の幸せバランス診断", page_icon="✨", layout="centered")

    st.markdown("""
        <style>
        .stApp { background-color: #fdfbf7; }
        .main-header { text-align: center; color: #8b5b6e; font-weight: bold; margin-bottom: 5px; }
        .sub-header { text-align: center; color: #a27b8c; font-size: 14px; margin-bottom: 25px; }
        .result-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #f0e6ea; box-shadow: 0 4px 6px rgba(0,0,0,0.03); margin-top: 20px; }
        .badge-cat { font-size: 18px; font-weight: bold; color: #d87093; text-align: center; margin-bottom: 15px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>✨ 男性性と女性性の幸せバランス診断 ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>〜 今日あった嬉しかったことから、あなたの「男性性」と「女性性」の循環を判定 〜</p>", unsafe_allow_html=True)

    user_input = st.text_area("男性性は行動する力、挑戦する力、考える力、カタチにする力。女性性は感じる力、創造する力、共鳴する力、引き寄せる力。今日あった「嬉しかったこと」「心が動いた出来事」を教えてください♡", placeholder="例：ランニングに行って朝日の写真を撮ったら、虹色のフレアが映り美しくて感動した！", height=100)

    if st.button("🌸 幸せバランスを診断する", use_container_width=True):
        if not user_input.strip():
            st.warning("嬉しかったことを入力してくださいね！")
        else:
            res = analyze_joy(user_input)

            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='badge-cat'>【{res['category']}】</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("👩 女性性の喜び", f"{res['ratio_fem']}%")
            with col2:
                st.metric("👨 男性性の喜び", f"{res['ratio_masc']}%")

            st.progress(res['ratio_fem'] / 100.0)

            st.markdown("### 📖 解説")
            st.write(res['summary'])

            st.markdown("### 💡 ワンポイントアドバイス")
            st.info(res['advice'])

            st.markdown("### 📓 まとめ")
            st.code(res['share_text'], language="text")
            st.markdown("</div>", unsafe_allow_html=True)

    return True

def cli_run():
    print("=" * 60)
    print("      ✨ 男性性女性性の幸せバランス診断 v3 ✨")
    print("  〜 五感の受容力と行動の達成力から喜びの循環を判定 〜")
    print("=" * 60)

    test_input = "今朝、ランニングに行って朝日の写真を撮ったら、虹色のフレアが映り美しくて感動した！"
    print(f"■ テスト実行例: 「{test_input}」\n")
    res = analyze_joy(test_input)
    print(f"★ 判定結果: 【{res['category']}】")
    print(f"   ・女性性の喜び度 : {res['ratio_fem']}%")
    print(f"   ・男性性の喜び度 : {res['ratio_masc']}%")
    print("-" * 60)
    print(f"■ 解説:\n{res['summary']}\n")
    print(f"■ アドバイス:\n{res['advice']}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    if "streamlit" in sys.modules or len(sys.argv) > 1 and sys.argv[1] == "run":
        run_streamlit()
    else:
        cli_run()
