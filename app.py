# -*- coding: utf-8 -*-
"""
『男性性と女性性の幸せバランス診断』 (joy_checker_app-v4.py)

今日あった嬉しかったことを入力すると、その出来事が「女性性の喜び」か「男性性の喜び」か、
あるいはその統合エネルギーかを多角的に分析し、深みのある解説と実践的なアドバイスを提供します。

【機能特徴】
- 7種類の詳細な診断パターン（受容・愛され型、五感・感性解放型、目標達成型、能動的提供型、内なる自己統合型、感謝循環型、日常の微細なトキメキ型）
- 多重分析ロジック＋コンテキスト解析
- Streamlit UI ＋ LINE/SNS共有テキスト生成対応
"""

import sys
import re

# ==========================================
# キーワード・パターン定義
# ==========================================
FEM_RECEIVE_PATTERNS = [
    r"もらった", r"された", r"奢して", r"ご馳走", r"プレゼント", r"ギフト", r"差し入れ",
    r"褒められ", r"カワイイ", r"可愛い", r"愛され", r"大切にされ", r"誘われ", r"受け入れ",
    r"手伝って", r"助けられ", r"庇われ", r"共感され", r"聴いてもらった", r"優しくされ"
]

FEM_SENSORY_PATTERNS = [
    r"美味しい", r"おいしい", r"気持ちよかっ", r"癒やされ", r"ほっとした", r"安心", r"リラックス",
    r"温泉", r"カフェ", r"マッサージ", r"甘え", r"味わう", r"まったり", r"共感", r"ぬくもり", r"幸せ",
    r"やさしく", r"抱きしめ", r"温かい", r"うっとり", r"トキメキ", r"ときめき", r"美しい", r"綺麗",
    r"キレイ", r"五感", r"感触", r"香り", r"音", r"空間", r"浸る", r"感動", r"景色", r"朝日", r"空"
]

MASC_ACHIEVE_PATTERNS = [
    r"達成", r"成功", r"完成", r"クリア", r"合格", r"勝つ", r"勝った", r"契約", r"成果", r"解決",
    r"やり切っ", r"やり遂げ", r"納品", r"稼いだ", r"売り上げ", r"昇進", r"目標", r"克服", r"突破",
    r"決断", r"克服した", r"やり遂げた", r"やりきった"
]

MASC_ACTION_PATTERNS = [
    r"あげた", r"プレゼントした", r"奢った", r"助けた", r"解決した", r"導いた", r"作っ", r"作った",
    r"挑戦", r"自分で", r"購入した", r"買った", r"任され", r"頼られ", r"ランニング", r"撮影",
    r"企画", r"提案", r"行動", r"選択", r"移動", r"走っ"
]

GRATITUDE_PATTERNS = [
    r"ありがとう", r"感謝", r"有難い", r"おかげ", r"恩恵", r"神様", r"宇宙"
]


def analyze_joy(text: str) -> dict:
    """入力された文章を解析し、喜びのカテゴリー、比率、深層解説、アドバイスを出力する関数"""
    if not text or not text.strip():
        return {"error": "嬉しかった出来事を文章で入力してください。"}

    fem_rec_score = sum(len(re.findall(p, text)) for p in FEM_RECEIVE_PATTERNS)
    fem_sens_score = sum(len(re.findall(p, text)) for p in FEM_SENSORY_PATTERNS)
    masc_ach_score = sum(len(re.findall(p, text)) for p in MASC_ACHIEVE_PATTERNS)
    masc_act_score = sum(len(re.findall(p, text)) for p in MASC_ACTION_PATTERNS)
    gratitude_score = sum(len(re.findall(p, text)) for p in GRATITUDE_PATTERNS)

    # 構造的構文解析（文脈の重み付け）
    if re.search(r"(してもらった|してくれた|受け取った|くれた|ご馳走になった|奢ってもらった|褒められた)", text):
        fem_rec_score += 2.0
    if re.search(r"(してあげた|やってやった|達成できた|自分でできた|やり切った|自分で買った|決めた)", text):
        masc_act_score += 2.0
    if re.search(r"(味わった|うっとり|感動した|美しかった|気持ちよかった|癒やされた)", text):
        fem_sens_score += 1.5

    total_fem = fem_rec_score + fem_sens_score
    total_masc = masc_ach_score + masc_act_score
    grand_total = total_fem + total_masc

    if grand_total == 0:
        ratio_fem = 50.0
        ratio_masc = 50.0
    else:
        ratio_fem = round((total_fem / grand_total) * 100, 1)
        ratio_masc = round((total_masc / grand_total) * 100, 1)

    # パターン分類（7タイプの詳細解説）
    if ratio_fem >= 60.0 and fem_rec_score >= fem_sens_score and fem_rec_score > 0:
        pattern_id = "fem_receive"
        title = "【女性性の喜び：受容・愛され・引き寄せ型】"
        summary = (
            "人や世界からの愛、好意、プレゼント、サポートを素直に「受け取る」ことで心が満たされた喜びです。\n"
            "「愛されること」「助けてもらうこと」に対して心をオープンに開き、世界からの優しさをそのまま受け容れられています。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "あなたは素晴らしい「受け取り上手」の才能を発揮しています！「お返しをしなきゃ」という頭の恐れや謙遜を手放し、\n"
            "「私は大切にされる価値がある♡」と純粋に受け取り切りましょう。\n"
            "弾けるような「嬉しい！」「ありがとう！」という感謝の感情を素直に外へ循環させることで、さらに大きな愛と豊かさが引き寄せられてきます。"
        )
        action_step = "💡 今日のアクション: 「ありがとう」の言葉とともに、その時感じた素直なトキメキや笑顔を相手や周りに伝えてみましょう。"

    elif ratio_fem >= 60.0 and fem_sens_score > fem_rec_score:
        pattern_id = "fem_sensory"
        title = "【女性性の喜び：五感・身体感覚・感性解放型】"
        summary = (
            "頭の思考（損得や正しさの判断）を静め、五感や身体感覚で「いまここ」の快・心地よさ・美しさに全身で没頭できた喜びです。\n"
            "身体の感覚が開いており、心の深い部分が温かい充足感で満たされている理想的な状態です。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "思考に邪魔されず、五感の感性をみずみずしく解放できています。\n"
            "「何が得か」「どう評価されるか」ではなく、「身体がどう感じているか（ほっとする、うっとりする、胸が高鳴る）」を人生の羅針盤にしてください。\n"
            "五感で味わった感動の余韻をじっくり身体に染み込ませることで、直感力と幸運体質が飛躍的に高まります。"
        )
        action_step = "💡 今日のアクション: その心地よかった感触や味わい、景色を目を閉じて思い出し、身体全体で3秒間浸ってみましょう。"

    elif ratio_masc >= 60.0 and masc_ach_score >= masc_act_score and masc_ach_score > 0:
        pattern_id = "masc_achieve"
        title = "【男性性の喜び：目標達成・自己突破型】"
        summary = (
            "自らの意志と集中力を結集し、難題や目標を力強くクリアした「自己効力感と突破力」の喜びです。\n"
            "自分の中の能動的なエネルギーがしっかりと現実を動かし、具体的な成果や成果物を生み出せた瞬間です。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "あなたの中の頼もしい「行動力・実現力」が見事に発揮されました！\n"
            "達成した直後にすぐ次の課題へ向かうのではなく、「自分、本当によく頑張った！」と自分の奮闘と成果をしっかり認め、称えてあげてください。\n"
            "内なる自分を誇りに思い、しっかりと労う承認の時間を挟むことで、次の挑戦へのエネルギーが無限湧きしてきます。"
        )
        action_step = "💡 今日のアクション: 自分の胸に手を当てて「よくやったね、最高の成果だよ」と自分自身をしっかり褒めてあげましょう。"

    elif ratio_masc >= 60.0 and masc_act_score > masc_ach_score:
        pattern_id = "masc_action"
        title = "【男性性の喜び：能動的提供・挑戦・リーダーシップ型】"
        summary = (
            "自らが主体となって決断・行動を起こし、誰かに価値を提供したり、新しい選択を切り拓いた喜びです。\n"
            "「自分の力で選択し、与え、創造する」という能動的なパワーが存分に回っています。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "周囲や自分自身に対して「与える力」「導く力」が力強く働いています。\n"
            "あなたが起点となって動いたことで、周囲に安心や歓びの波紋が広がっています。\n"
            "「自ら動いて価値を生み出せる自分」への信頼（自己信頼感）をさらに深め、自分の意志による選択を楽しんでいきましょう。"
        )
        action_step = "💡 今日のアクション: 自分が起こした行動や決断によって生まれたポジティブな変化を紙やノートに書き留めてみましょう。"

    elif gratitude_score > 0 and (40.0 <= ratio_fem <= 60.0):
        pattern_id = "gratitude_cycle"
        title = "【感謝と愛の響き合い：高次元エネルギー循環型】"
        summary = (
            "単なる出来事の成否を超えて、人や環境、目に見えない配慮や恩恵に対する「温かい感謝の波動」が溢れ出た喜びです。\n"
            "男性性の行動と女性性の受け取りが「感謝」という最高の波動で結ばれています。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "心からの感謝が湧き出ている状態は、すべての引き寄せの中で最も高いエネルギー状態です！\n"
            "その温かい感謝の気持ちを、言葉・表情・小さな贈り物などの形で外の世界へ循環させましょう。\n"
            "出された感謝のエネルギーは倍になってあなたのもとへ舞い戻り、さらなる奇跡的な循環を生み出します。"
        )
        action_step = "💡 今日のアクション: 感謝したい人や出来事に向けて、心の中で「ありがとう」と念じるか、メッセージで感謝を伝えてみましょう。"

    elif 40.0 <= ratio_fem <= 60.0:
        pattern_id = "integration"
        title = "【女性性と男性性の統合：内なる自己統合型（幸せのバランス循環）】"
        summary = (
            "自ら能動的に意志を持って行動・選択した男性性のパワーと、そのプロセスや成果を五感で素直に受け取り味わった女性性の感性が見事に協奏した喜びです。\n"
            "内なる「行動する自分」と「感じる自分」が完璧な相思相愛（両思い）で巡っています。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "「与える力・動く力」と「受け取る力・感じる力」が理想的な黄金バランスで循環しています！\n"
            "自ら行動を起こした自分の頑張りを称えつつ（男性性の承認）、そこで得られた感動や歓びを身体全体で味わい尽くす（女性性の受容）というセルフパートナーシップが完成しています。\n"
            "この内なる調和状態を維持することで、努力感なく自然体で豊かな現実を引き寄せ続けることができます。"
        )
        action_step = "💡 今日のアクション: 「自分を最高のスポットに連れて行ってくれてありがとう」「この感動を味わわせてくれて幸せ♡」と内なる自分と対話してみましょう。"

    else:
        pattern_id = "subtle_joy"
        title = "【日常の微細なトキメキ：感性感度アップ型】"
        summary = (
            "劇的な成果や大きな刺激に頼らず、日常の些細な一瞬（ほっとする時間、美しい風景、ちょっとした会話）に幸せを見出せた穏やかで深い喜びです。"
        )
        advice = (
            "【幸せを加速させるアドバイス】\n"
            "あなたの感性の感度がとても豊かに開いています。\n"
            "「何でもない日常」の中に小さなトキメキを見つけられること自体が、豊かな女性性と安定した男性性の土台がある証拠です。\n"
            "この日常の小さな幸せを大切にカウントしていくことで、あなたの幸福のベースライン（基礎の波動）が底上げされます。"
        )
        action_step = "💡 今日のアクション: 今日感じた小さな「ほっとした瞬間」や「キレイだなと思ったもの」を写真や手帳に残してみましょう。"

    return {
        "input_text": text,
        "pattern_id": pattern_id,
        "category": title,
        "ratio_fem": ratio_fem,
        "ratio_masc": ratio_masc,
        "summary": summary,
        "advice": advice,
        "action_step": action_step
    }


def cli_run():
    print("=" * 60)
    print("      ✨ 男性性と女性性の幸せバランス診断 (v4) ✨")
    print("  〜 今日あった嬉しかったことから内なるエネルギーを判定 〜")
    print("=" * 60)
    
    test_input = "今朝、ランニングに行って朝日の写真を撮ったら、虹色のフレアが映った超絶美しい写真が撮れて感動した"
    print(f"■ 入力例: {test_input}\n")
    res = analyze_joy(test_input)
    print(f"★ 判定結果: {res['category']}")
    print(f"   ・女性性の喜び度 : {res['ratio_fem']}%")
    print(f"   ・男性性の喜び度 : {res['ratio_masc']}%")
    print("-" * 60)
    print(f"■ 解説:\n{res['summary']}\n")
    print(f"■ ワンポイントアドバイス:\n{res['advice']}\n")
    print(f"{res['action_step']}")
    print("=" * 60 + "\n")


# ==========================================
# Streamlit Web UI サポート
# ==========================================
def main_streamlit():
    import streamlit as st

    st.set_page_config(
        page_title="男性性と女性性の幸せバランス診断",
        page_icon="✨",
        layout="centered"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fffafc;
        }
        .main-title {
            text-align: center;
            color: #d81b60;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .sub-title {
            text-align: center;
            color: #880e4f;
            font-size: 14px;
            margin-bottom: 25px;
        }
        .result-card {
            background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #f8bbd0;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        .badge-title {
            color: #c2185b;
            font-size: 18px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">✨ 男性性と女性性の幸せバランス診断 ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">〜 今日あった嬉しかったことから、あなたの「男性性」と「女性性」の循環を紐解く 〜</div>', unsafe_allow_html=True)

    st.write("今日あった「嬉しかったこと」「楽しかったこと」など自由に入力してください♡")

    st.write("👨男性性は行動する力、挑戦する力、考える力、カタチにする力")
    st.write("👩女性性は感じる力、創造する力、共鳴する力、引き寄せる力")


    user_input = st.text_area("▼ 今日の出来事を入力", value=default_val, height=100, placeholder="例: 欲しかった服を試着したらサイズもピッタリでワクワクした！")

    if st.button("💖 喜びのバランスを診断する", use_container_width=True):
        if not user_input.strip():
            st.warning("嬉しかった出来事を文章で入力してください。")
        else:
            res = analyze_joy(user_input)

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="badge-title">判定結果: {res["category"]}</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            col1.metric("👩 女性性の喜び度", f"{res['ratio_fem']}%")
            col2.metric("👨 男性性の喜び度", f"{res['ratio_masc']}%")

            st.progress(res['ratio_fem'] / 100.0)

            st.markdown("### 📖 喜びの深層解説")
            st.write(res["summary"])

            st.markdown("### 💖 幸せを引き寄せるアドバイス")
            st.info(res["advice"])

            st.success(res["action_step"])
            st.markdown('</div>', unsafe_allow_html=True)

            # LINE/SNSシェア用テキスト枠
            st.markdown("### 📓 まとめ")
            share_text = (
                f"【男性性と女性性の幸せバランス診断結果】\n"
                f"出来事: 「{user_input}」\n\n"
                f"★ 判定: {res['category']}\n"
                f"・女性性: {res['ratio_fem']}%\n"
                f"・男性性: {res['ratio_masc']}%\n\n"
                f"【アドバイス】\n{res['advice']}\n\n"
                f"{res['action_step']}"
            )
            st.code(share_text, language="text")

    with st.expander("❓ 男性性の喜びと女性性の喜びの違いとは？"):
        st.write(
            "・**女性性の喜び（受容・感覚・愛される喜び）**:\n"
            "  人からの愛やサポートを「受け取る」、五感で美しさや心地よさを「味わう」、感情をのびやかに解放する喜びです。\n\n"
            "・**男性性の喜び（達成・行動・与える喜び）**:\n"
            "  目標に向かって「行動する」、課題を「達成する」、誰かに価値や優しさを「与える」という能動的なパワーの喜びです。\n\n"
            "・**統合エネルギー（自己統合）**:\n"
            "  自らの意志で動き（男性性）、そのプロセスや成果を心身全体で受け取る（女性性）という、内なる自分が相思相愛で巡っている最高の状態です。"
        )


if __name__ == "__main__":
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            main_streamlit()
        else:
            cli_run()
    except Exception:
        cli_run()
